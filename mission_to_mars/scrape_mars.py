from splinter import Browser, browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    data = {}
    output = mars_news()
    data['news_title'] = output[0]
    data['news_paragraph'] = output[1]
    data['mars_img']= mars_img()
    data['mars_facts'] = mars_fact()
    data['mars_hemisphere']= mars_hemisphere()
    return data

def mars_news():
    url = "https://redplanetscience.com/#"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    rp_article = soup.find('div', class_="list_text")
    rp_news_title = rp_article.find('div', class_="content_title").text
    rp_news_p = rp_article.find('div', class_="article_teaser_body").text
    output = [rp_news_title, rp_news_p]
    return output

def mars_img():
    url_mars_img = "https://spaceimages-mars.com/image/featured/mars1"
    browser.visit(url_mars_img)

    html = browser.html
    soup = bs(html, "html parser")
    img = soup.find('img', class_="thumb")['src']
    img_url = "https://spaceimages-mars.com/" + img
    return img_url

def mars_fact():
    import pandas as pd
    mars_facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(mars_facts_url)
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts = pd.DataFrame(mars_facts[0])
    mars_facts.columns = ["Description", "Value"]
    mars_facts = mars_facts.set_index("Description")
    mars_table = mars_facts.to_html(header= True, index= True)
    return mars_table

def mars_hemisphere():
    mars_hemi_images = []
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    
    browser.visit(hemi_url)
    html = browser.html
    soup = bs(html, "html.parser")
    list = soup.find_all('div', class_="item")
    for a in list:
        title = a.find('h3').text
        hem_url = "https://astrogeology.usgs.gov/" + a.find("a")["href"]
        browser.visit(hem_url)
        soup = bs(browser.html, 'html.parser')
        image_url = soup.find('li').find('a')['href']
        mars_hemi_images.append({"title": title, "img_url": image_url})
    return mars_hemi_images