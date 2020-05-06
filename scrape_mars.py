from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

mars_var = {}

def NASA_Mars_News():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    #time.spleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find_all('div' , class_ = 'content_title')[1].text
    news_p = soup.find_all('div' , class_ = 'article_teaser_body')[0].text
    
    mars_var["news_title"] = news_title
    mars_var["news_p"] = news_p

    browser.quit()

    return mars_var

def Featured_Image():
    browser = init_browser()

    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)

    html1 = browser.html
    soup1 = bs(html1, 'html.parser')

    temp_url1 = soup1.find_all('article' , class_ = 'carousel_item')[0]['style']
    temp_url2 = soup1.find_all('div' , class_ = 'jpl_logo')[1]

    temp_url1 = temp_url1.replace("background-image: url('" , "").replace("');" , "")

    temp_url2= [a['href'] for a in temp_url2.find_all('a', href=True) if a.text]

    featured_image_url = temp_url2[0] + temp_url1

    mars_var["featured_image_url"] = featured_image_url

    browser.quit()

    return mars_var

def Mars_Weather():
    browser = init_browser()

    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)

    time.sleep(20)

    html2 = browser.html
    soup2 = bs(html2, 'html.parser')

    mars_weather = soup2.find_all('div' , class_ = 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')[0].span.text

    mars_var["mars_weather"] = mars_weather
    
    browser.quit()

    return mars_var

def Mars_Facts():
    browser = init_browser()

    url3 = "https://space-facts.com/mars/"
    
    tables = pd.read_html(url3)
    df = tables[0]
    df.columns = ['Description' , 'Value']
    df.set_index('Description', inplace = True)
    mars_table = df.to_html()

    mars_var["mars_table"] = mars_table

    browser.quit()

    return mars_var

def Mars_Hemispheres():
    browser = init_browser()

    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(url4)
    soup4 = bs(response.text, "lxml")

    temp_var = soup4.find_all('div' , class_ = 'description')

    title = [t.h3.text for t in temp_var] 

    tempar = []
    for link in soup4.findAll('a'):
        tempar.append(link.get('href'))

    main_url = [m for m in tempar if "http://astrogeology.usgs.gov/search" in m]
    main_url = [s.replace('/search', '') for s in main_url]

    sub_urls = [s for s in tempar if "/search/map" in s]
    sub_urls = [main_url[0] + i for i in sub_urls]

    temp_var_url = []
    for u in sub_urls:
        response1 = requests.get(u)
        soup5 = bs(response1.text, 'lxml')
        temp_var_url.append(main_url[0] + soup5.find('img' , class_ = 'wide-image')['src'])

    hemisphere_image_urls = []

    for l in range(len(title)):
        hemisphere_image_urls.append({"title": "" + title[l] + "", "img_url": "" + temp_var_url[l] + ""})

    mars_var["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return mars_var