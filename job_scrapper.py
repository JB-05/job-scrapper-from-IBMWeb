import time
import logging
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class JobScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.jobs = []
        self.driver = self._init_driver()

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")  # Reduce logs
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def get_page_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'bx--card'))
            )
            time.sleep(2)
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as e:
            logging.error(f"Error loading page {url}: {e}")
            return None

    def extract_job_details(self, job_element) -> Dict:
        job_data = {
            'title': None,
            'company': 'IBM',
            'department': None,
            'location': None,
            'posted_date': None,
            'job_link': None,
            'job_id': None
        }

        try:
            card = job_element.find('div', class_='bx--card')
            if not card:
                return job_data

            job_data['department'] = card.find('div', class_='bx--card__eyebrow').text.strip() if card.find('div', class_='bx--card__eyebrow') else 'Not specified'
            job_data['title'] = card.find('h4', class_='bx--card__heading').text.strip() if card.find('h4', class_='bx--card__heading') else 'Not specified'
            copy_element = card.find('div', class_='ibm--card__copy__inner')
            if copy_element:
                br_tag = copy_element.find('br')
                if br_tag and br_tag.next_sibling:
                    job_data['location'] = br_tag.next_sibling.strip()
            link_element = card.find('a', class_='bx--card__wrapper')
            if link_element:
                href = link_element.get('href', '')
                job_data['job_link'] = f"https://www.ibm.com{href}" if href.startswith('/') else href
                job_data['job_id'] = href.split('/')[-1]
            date_element = card.find('div', class_='ibm-card__date')
            job_data['posted_date'] = date_element.text.strip() if date_element else 'Not specified'

        except Exception as e:
            logging.warning(f"Error extracting job: {e}")
        return job_data

    def scrape_jobs(self, max_pages: int = 5) -> List[Dict]:
        page_num = 1
        current_url = self.base_url

        while page_num <= max_pages:
            logging.info(f"Scraping page {page_num}...")
            soup = self.get_page_soup(current_url)
            if not soup:
                break

            job_elements = soup.find_all('div', class_='bx--card-group__cards__col')
            if not job_elements:
                logging.info("No job listings found.")
                break

            for job_el in job_elements:
                job = self.extract_job_details(job_el)
                if job['title']:
                    self.jobs.append(job)

            # Check if next page exists using JS-based pagination
            try:
                next_button = self.driver.find_element(By.XPATH, '//button[@aria-label="Next Page"]')
                if next_button.get_attribute("disabled"):
                    break
                else:
                    next_button.click()
                    time.sleep(2)
                    page_num += 1
            except Exception:
                logging.info("No more pages found.")
                break

        return self.jobs

    def save_to_csv(self, filename: str):
        df = pd.DataFrame(self.jobs)
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(self.jobs)} jobs to {filename}")

    def close(self):
        self.driver.quit()

def main():
    career_page_url = "https://www.ibm.com/in-en/careers/search?job-search=jobs"
    scraper = JobScraper(career_page_url)
    
    try:
        jobs = scraper.scrape_jobs(max_pages=5)
        scraper.save_to_csv("ibm_jobs.csv")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
