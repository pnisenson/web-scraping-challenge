from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": r'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def soupify(url, browser):
    browser.visit(url)
    time.sleep(1)
    page = browser.html
    soup = bs(page, "html.parser")
    return soup

def scrape():
    # Navigate and Soupify to NASA Page
    browser = init_browser()
    soup = soupify('https://mars.nasa.gov/news/', browser)
    
    #bring results in
    results= soup.find('li', class_="slide")
    news_title = results.find_all('h3')[0].text
    news_p = results.find_all('a')[0].text
    # Store data in a dictionary
    scraped_data = {
        "news_title": news_title,
        "news_para": news_p
    }
    browser.quit()

    # Navigate to JPL page and Soupify 
    browser = init_browser()
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    soup = soupify(url, browser)
    image = soup.find('div', class_="floating_text_area")
    image_html = image.a['href']
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_html}'
    scraped_data['MarsImage'] = featured_image_url
    browser.quit()

    # Navigate to Mars Facts page
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    # Scrape the Mars facts table and convert to html
    table = pd.read_html(url)[0]
    table = table.rename(columns={0:"Description", 1:"Mars"})
    table = table.set_index("Description", drop = True)
    table = table.to_html(classes="table table-striped")
    scraped_data['table'] = table
    browser.quit()

    # Navigate to Mars astrology page and Soupify 
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
    soup = soupify(url, browser)

    # Get the Hemisphere names and append to list
    hemispheres = soup.find_all('div', class_="item")
    number = 1
    hemi_name = []
    hemi_label= 'hemi_name' + str(number)
    for hemi in hemispheres:
        hemi_name.append(hemi.find('h3').text)
        scraped_data[hemi_label] = hemi.find('h3').text
        number +=1
        hemi_label = 'hemi_name' + str(number)

    # Create loop to click each hemisphere link and grab the full image url
    number = 1
    hemi_link = 'hemi_link' + str(number)
    for hemi in hemi_name:
        #click the link of the image
        browser.find_by_text(hemi).click()
        #get image source
        scraped_data[hemi_link] = browser.links.find_by_text('Sample')['href']
        number +=1
        hemi_link = 'hemi_link' + str(number)
        #return to previous page
        browser.visit(url)

    # Close the browser after scraping
    browser.quit()

    # Return results
    return scraped_data


