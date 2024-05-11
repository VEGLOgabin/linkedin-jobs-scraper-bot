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
    
    # Find the ul element containing all job listings
    job_list_ul = driver.find_element(By.CSS_SELECTOR, "ul.jobs-search__results-list")
    
    # Find all job list items within the ul element
    job_list_items = job_list_ul.find_elements(By.TAG_NAME, "li")
    
    # Loop through each job list item and extract details
    for job_item in job_list_items:
        try:
            # Extract job title
            job_title = job_item.find_element(By.CLASS_NAME, "base-search-card__title").text
            print("Job Title:", job_title)
        except Exception as e:
            job_title = None
        
        try:
            # Extract company name
            company_name = job_item.find_element(By.CLASS_NAME, "hidden-nested-link").text
            print("Company Name:", company_name)
        except Exception as e:
            company_name = None
        
        try:
            # Extract location
            location = job_item.find_element(By.CLASS_NAME, "job-search-card__location").text
            print("Location:", location)
        except Exception as e:
            location = None
        
        try:
            # Extract posted time
            posted_time = job_item.find_element(By.CLASS_NAME, "job-search-card__listdate--new").text
            print("Posted Time:", posted_time)
        except Exception as e:
            posted_time = None
        
        try:
            # Extract company page link
            company_page_link = job_item.find_element(By.CLASS_NAME, "hidden-nested-link").get_attribute("href")
            print("Company Page Link:", company_page_link)
        except Exception as e:
            company_page_link = None
        
        
        try:
            # Extract job URL
            job_url = job_item.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute("href")
            print("Job URL:", job_url)
        except Exception as e:
            job_url = None
        
        try:
            # Extract benefits
            benefits = job_item.find_element(By.CLASS_NAME, "job-posting-benefits__text").text
            print("Benefits:", benefits)
        except Exception as e:
            benefits = None
        #######
        print("\n")
    
    # Close the webdriver
    driver.quit()

# Ask user for job name input
job_name = input("Enter the job name: ")

# Scrape LinkedIn jobs based on the user input
scrape_linkedin_jobs(job_name)
