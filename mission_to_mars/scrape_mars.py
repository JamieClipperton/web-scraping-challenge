from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import os


def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser= Browser('chrome', **executable_path, headless=True)

    news_title, news_p = marsNews(browser)

    final_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": marsImage(browser),
        "facts": marsFact(),
        "hemispheres": marsHem(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return final_data
    

def marsNews(browser):
    news_url = "https://data-class-mars.s3.amazonaws.com/Mars/index.html"
    browser.visit(news_url)
    html = browser.html
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    sour = bs(html, 'html.parser')

    try:
        sour_elem = sour.select_one('div.list_text')
        news_title = sour_elem.find('div', class_="content_title").text
        news_p = sour_elem.find('div', class_="article_teaser_body").text
    except AttributeError:
        return None, None

    return news_title, news_p

def marsImage(browser):
    image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(image_url)
    big_img = browser.find_by_tag('button')[1]
    big_img.click()
    html = browser.html
    cur_img = bs(html, "html parser")

    try:
        image = cur_img.find("img", class_='fancybox-image').get('src')
    except AttributeError:
        return None

    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image}'
    return featured_image_url

def marsFact(browser):
    mars_facts_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(mars_facts_url)
    mars_data = pd.read_html(mars_facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(header= True, index= True)
    return mars_facts

def marsHem(browser):
    import time
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere= []

    products = soup.find("div", class_= "result-list")
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:  
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere

if __name__ == "__main__":
    print(scrape_all())
