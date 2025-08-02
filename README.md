# IBM Careers Job Scraper

This project is a Python-based web scraper designed to collect job listings from the [IBM Careers website](https://www.ibm.com/in-en/careers/search). It utilizes Selenium and BeautifulSoup to extract key job information from multiple pages and exports the data to a structured CSV file for further analysis or processing.

## Features

- Automates extraction of job listings from IBM's dynamic career portal.
- Captures the following job fields:
  - Job Title
  - Department
  - Location
  - Posting Date
  - Job ID
  - Job Link
- Supports pagination across multiple result pages.
- Saves the results to a CSV file (`ibm_jobs.csv`).
- Uses a headless browser to run in the background.

## Technologies Used

- Python 3.7+
- Selenium
- BeautifulSoup (bs4)
- pandas

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ibm-job-scraper.git
   cd ibm-job-scraper

2. **Install dependencies**
- It is recommended to use a virtual environment.
   
   ```bash
   pip install -r requirements.txt


## Usage 

- To run the scraper:

    ```bash
    python scraper.py


## Developed with 🫶
- Joel Biju || JB