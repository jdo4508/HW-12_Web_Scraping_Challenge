# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time 

# Create Dictionary to collect all of the data
mars= {}

# Define Function Scrape
def scrape():
    
    # Define Function for opening browser
    executable_path = {"executable_path":"chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless = False)

    # # NASA Mars News
    #Open browser to NASA Mars News Site
    browser.visit('https://mars.nasa.gov/news/')

    
    html = browser.html
    soup = bs(html, 'html.parser')

    #Search for news titles and paragraph
    news_title = soup.find('div', class_='list_text').find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Add data to dictionary
    mars['news_title'] = news_title
    mars['news'] = news_p


    # # Featured Image

    #Open browser to JPL featured image
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    #Navigate to Full Image page'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.click_link_by_partial_text('FULL IMAGE')

    #Navigate with delay for full large image
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'html.parser')

    #Search for image source and save as variable
    results = soup.find_all('figure', class_='lede')
    relative_img_path = results[0].a['href']
    featured_img_url = 'https://www.jpl.nasa.gov' + relative_img_path

    #Add data to dictionary
    mars['featured_image_url'] = featured_img_url 

    # # Mars Weather

    #Specify url
    url = 'https://twitter.com/marswxreport?lang=en'

    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # Find all elements that contain tweets
    tweets = soup.find_all('div', class_='js-tweet-text-container')

    #Search through tweets
    for tweet in tweets: 
        mars_weather = tweet.find('p').text
    
        #select only weather related tweets that contain the word "pressure"
        if 'pressure' in mars_weather:
            weather = tweet.find('p')
            break
        else: 
            pass

    #Add data to dictionary
    mars['weather']= weather.text
    

    # # Mars Facts
    #Visit the mars facts site and parse
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    #Find Mars Facts DataFrame and assign comlumns
    df = tables[0]
    df.columns = ['Description', 'Value']

    #Save as html
    html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)
   
    #Add data to dictionary
    mars['table']=html_table

    # # Mars Hemispheres
    #Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    html= browser.html
    soup = bs(html, 'html.parser')

    #Retreive mars hemispheres information
    items = soup.find_all('div', class_='item')

    #Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    #Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    #Loop through the items previously stored
    for i in items: 
        title = i.find('h3').text
        
        #Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        #Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        img_html = browser.html
        soup = bs(img_html, 'html.parser')
        
        #Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})    

    # Store data in a dictionary
    mars['hemisphere_image_urls']= hemisphere_image_urls
    
    
    # #Return data and quit broswer
    return mars
    browser.quit()





