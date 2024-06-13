from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import urllib.parse
import requests
import time
import os

def save_cookies(driver, path):
    with open(path, 'w') as file:
        for cookie in driver.get_cookies():
            name = cookie.get('name', 'N/A')
            value = cookie.get('value', 'N/A')
            domain = cookie.get('domain', 'N/A')
            path = cookie.get('path', 'N/A')
            secure = str(cookie.get('secure'))
            
            file.write(f"{name};{value};{domain};{path};{secure}\n")

def load_cookies(driver, path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            for line in file:
                try:
                    name, value, domain, path, secure = line.strip().split(';')
                    cookie = {
                        'name': name,
                        'value': value,
                        'domain': domain,
                        'path': path,
                        'secure': secure == 'True'
                    }
                    driver.add_cookie(cookie)
                except ValueError:
                    print(f"Error loading cookie from line: {line}")

def is_logged_in(driver, ignore_error=False):
    try:
        # More reliable element to check if logged in
        driver.find_element(By.CSS_SELECTOR, "div.feed-identity-module__actor-meta")  # This is an example; ensure it exists
        return True
    except NoSuchElementException:
        if not ignore_error:
            raise
        return False

# Creating a webdriver instance
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Opening LinkedIn's login page
driver.get("https://linkedin.com/uas/login")
time.sleep(2)

# Load cookies from file
cookie_file_path = "Cookies.data"
load_cookies(driver, cookie_file_path)

# Navigate to LinkedIn feed to check if cookies are valid
driver.get("https://www.linkedin.com/feed/")
time.sleep(2)

# Check if already logged in using stored cookies
if not is_logged_in(driver, ignore_error=True):
    # If not logged in, perform login
    driver.get("https://linkedin.com/uas/login")
    time.sleep(5)
    
    # Entering username. Make sure to enable this during 1st time login.
    #username = driver.find_element(By.ID, "username")
    #username.send_keys("ENTER YOUR EMAIL HERE")
    
    # Entering password
    pword = driver.find_element(By.ID, "password")
    pword.send_keys("ENTER YOUR PASSWORD HERE")
    
    # Clicking on the log in button
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(10)

    # Save fresh cookies to a file regardless of whether login was required
    save_cookies(driver, cookie_file_path)
else:
    print("Already logged in using stored cookies.")

#LOGIN FLOW IS COMPLETED
##################################################################################################

# Now you can proceed with your further actions
# For example, you can scrape the profile page or any other actions

print("Company Search Code Executed")

def main():
    # Hardcoded base URL
    base_url = "https://www.linkedin.com/search/results/people/"
    
    # Fixed URL parameters
    fixed_params = {
        "geoUrn": "[\"102713980\"]",
        "heroEntityKey": "urn:li:organization:1259",
        "origin": "FACETED_SEARCH",
        "position": "0",
        "sid": "(cp"
    }
    
    # Take input from the user
    user_input = input("Enter the comapany name to search: ")
    
    # Add the user input to the parameters
    fixed_params["keywords"] = user_input
    
    # Encode the parameters to make them URL safe
    encoded_params = urllib.parse.urlencode(fixed_params)
    
    # Construct the full URL with the user input as a parameter
    full_url = f"{base_url}?{encoded_params}"
    
    # Print the full URL
    print(f"Full URL: {full_url}")

#Visiting the URL    
    driver.get(full_url)
    
    # Wait for a few seconds to ensure the page loads
    time.sleep(2)
    
    # Print page title or part of the page content for verification
    print(f"Page title: {driver.title}")
    #print(f"Page content snippet: {driver.page_source[:500]}")

if __name__ == "__main__":
    main()