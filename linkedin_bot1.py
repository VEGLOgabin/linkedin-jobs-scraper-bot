from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


url = "https://www.linkedin.com/jobs/search"

def scrape_linkedin_jobs(job_name):
   
    driver =  webdriver.Firefox() 
    driver.get(url)
    driver.implicitly_wait(3)
    time.sleep(2)  

    
    search_input = driver.find_element(By.ID, "job-search-bar-keywords")
    search_input.send_keys(job_name)
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)  
    
    
    job_list_ul = driver.find_element(By.CSS_SELECTOR, "ul.jobs-search__results-list")
    
   
    job_list_items = job_list_ul.find_elements(By.TAG_NAME, "li")
    
    
    for job_item in job_list_items:
        try:
           
            job_title = job_item.find_element(By.CLASS_NAME, "base-search-card__title").text
            print("Job Title:", job_title)
        except Exception as e:
            job_title = None
        
        try:
            
            company_name = job_item.find_element(By.CLASS_NAME, "hidden-nested-link").text
            print("Company Name:", company_name)
        except Exception as e:
            company_name = None
        
        try:
           
            location = job_item.find_element(By.CLASS_NAME, "job-search-card__location").text
            print("Location:", location)
        except Exception as e:
            location = None
        
        try:
          
            posted_time = job_item.find_element(By.CLASS_NAME, "job-search-card__listdate--new").text
            print("Posted Time:", posted_time)
        except Exception as e:
            posted_time = None
        
        try:
            
            company_page_link = job_item.find_element(By.CLASS_NAME, "hidden-nested-link").get_attribute("href")
            print("Company Page Link:", company_page_link)
        except Exception as e:
            company_page_link = None
        
        
        try:
            
            job_url = job_item.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute("href")
            print("Job URL:", job_url)
        except Exception as e:
            job_url = None
        
        try:
            
            benefits = job_item.find_element(By.CLASS_NAME, "job-posting-benefits__text").text
            print("Benefits:", benefits)
        except Exception as e:
            benefits = None
        #######
        print("\n")
        
    
   
    close_or_not = input("Enter 'yes' to close the driver or 'no' to keep it open : ")
    
    if  close_or_not == 'yes':
       
        driver.quit()
    elif  close_or_not == 'no':
       
        job_name = input("Enter the job name: ")
        
       
        driver.quit()

        
        scrape_linkedin_jobs(job_name)
    
    else:
        print("Bad input")
        
        driver.quit()
        
        
        
        

job_name = input("Enter the job name: ")


scrape_linkedin_jobs(job_name)
