from splinter import Browser, browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    final_data = {}
    output = marsNews()
    final_data['mars_news'] = output[0]
    final_data['mars_paragraph'] = output[1]
    final_data['mars_image']= marsImage()
    final_data['mars_facts'] = marsFact()
    final_data['mars_hemisphere']= marsHem()
    return final_data

def marsNews():
    news_url = "https://redplanetscience.com/#"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    article = soup.find('div', class_="list_text")
    news_title = article.find('div', class_="content_title").text
    news_p = article.find('div', class_="article_teaser_body").text
    output = [news_title, news_p]
    return output

def marsImage():
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html parser")
    image = soup.find('img',)['src']
    featured_image_url ="https://spaceimages-mars.com/image/featured/mars2.jpg"
    return featured_image_url

def marsFact():
    import pandas as pd
    mars_facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(mars_facts_url)
    mars_data = pd.read_html(mars_facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(header= True, index= True)
    return mars_facts

def marsHem():
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


