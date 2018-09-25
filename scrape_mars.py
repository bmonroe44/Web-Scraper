
# Dependecies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import numpy as np
from selenium import webdriver

def scrape():
# Scrape NASA Mars News Site and collect news title and paragraph text
    url = 'https://mars.nasa.gov/news/'
    response =requests.get(url)

    soup = bs(response.text, 'lxml')

# Create variables for title and paragraph text
    news_title = soup.find('div', class_='content_title').text
    paragraph_text = soup.find('div', class_='rollover_description_inner').text

#Visit the URL for JPL's Space Images-Use splinter to navigate site
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

# Click the 'FULL IMAGE' button
    browser.click_link_by_partial_text('FULL IMAGE')

# Click the 'more info' button
    browser.click_link_by_partial_text('more info')

# Get feature image url from 'more info' page
    html_2 = browser.html
    soup_2 = bs(html_2, 'html.parser')
    img_url = soup_2.find('img', class_='main_image')
    end_img_url = img_url.get('src')

    feature_image_url = 'https://www.jpl.nasa.gov' + end_img_url

# Scrape latest Mars weather tweet from 'https://twitter.com/marswxreport?lang=en'
    url = 'https://twitter.com/marswxreport?lang=en'
    twitter_resp = requests.get(url)
    twitter_soup = (bs(twitter_resp.text, 'html.parser').find('div', class_='js-tweet-text-container')).text.strip()

# Create a pandas dataframe containing facts scraped from 'https://space-facts.com/mars/'
    mars_facts_request = requests.get('https://space-facts.com/mars/')
    mars_facts_table = pd.read_html(mars_facts_request.text)
    mars_facts_table
    mars_facts_df = mars_facts_table[0]
    mars_facts_df

# Visit USGS Astrology site, 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' to obtain 
#high reloution images of each of Mar's hemispheres
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

# Find image url for full resolution image
    links = browser.find_by_css("a.product-item h3")

# Save the image url string and hemisphere title containing hemisphere name in python dictionary
    hemisphere_img_urls = []
# Itterate through the links
    for link in range(len(links)):
        images = {}
        browser.find_by_css("a.product-item h3")[link].click()
    #print(browser.find_by_css("a.product-item h3")[link])
        image_url = browser.find_link_by_text('Sample')
        images['img_url'] = image_url['href']
    #print(image_url)
        browser.find_by_css('h2.title').text
        image_title = browser.find_by_css('h2.title').text
        images['title'] = image_title
        hemisphere_img_urls.append({"title": image_title, "image_url": image_url})
        browser.back()

    mars_dictionary = {"Nasa_Title": news_title, "Nasa_Paragraph": paragraph_text,
                       "Feature_Image": feature_image_url, "Mars_Weather": twitter_soup,
                       "Mars_Facts": mars_facts_df, "Hemispheres": hemisphere_img_urls}
    
    browser.quit()
    return mars_dictionary

if __name__ == "__main__":
  print(scrape())  
