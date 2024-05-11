from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# url = "https://www.linkedin.com/jobs/"
url = "https://www.linkedin.com/jobs/search"

def scrape_linkedin_jobs(job_name):
    # Set up Selenium webdriver
    driver =  webdriver.Firefox() 
    driver.get(url)
    driver.implicitly_wait(3)
    time.sleep(2)  # Let the page load

    # Find the search input field and input the job name
    search_input = driver.find_element(By.ID, "job-search-bar-keywords")
    search_input.send_keys(job_name)
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)  # Let the page load
    
    all_job_per_page = driver.find_element(By.CSS_SELECTOR, "#main-content > section > ul")
    
    print(all_job_per_page)
    
    jobList = all_job_per_page.find_elements(By.CLASS_NAME,'base-card__full-link')
    hrefList = []
    for e in jobList:
        link = e.get_attribute('href')
        hrefList.append(link)
        print(link)

    # Find and extract job listings
    # job_listings = driver.find_elements(By.CLASS_NAME, "job-card-container")
    # for job in job_listings:
    #     title = job.find_element(By.CLASS_NAME, "job-card-search__title").text
    #     company = job.find_element(By.CLASS_NAME, "job-card-search__company-name").text
    #     location = job.find_element(By.CLASS_NAME, "job-card-search__location").text
    #     print(f"Title: {title}\nCompany: {company}\nLocation: {location}\n")

    # Close the webdriver
    driver.quit()

# Ask user for job name input
job_name = input("Enter the job name: ")

# Scrape LinkedIn jobs based on the user input
scrape_linkedin_jobs(job_name)
