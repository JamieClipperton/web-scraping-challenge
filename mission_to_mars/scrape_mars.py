from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser= Browser('chrome', **executable_path, headless=True)

    news_title, news_p = marsNews(browser)

    final_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": marsImage(browser),
        "facts": marsFact(browser),
        "hemispheres": marsHem(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return final_data
    

def marsNews(browser):
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html=browser.html
    sour = bs(html, 'html.parser')

    try:
        sour_elem = sour.select_one('div.list_text')
        news_title = sour_elem.find('div', class_='content_title').get_text()
        news_p = sour_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def marsImage(browser):
    image_url = "https://spaceimages-mars.com"
    browser.visit(image_url)

    big_img = browser.find_by_tag('button')[1]
    big_img.click()

    html = browser.html
    cur_img = bs(html, "html.parser")

    try:
        image = cur_img.find("img", class_='fancybox-image').get('src')
    except AttributeError:
        return None

    featured_image_url = f'https://spaceimages-mars.com/{image}'
    return featured_image_url

def marsFact():
    try:
        facts_df=pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    facts_df.columns=['description', 'Mars', 'Earth']
    facts_df.set_index('description', inplace=True)
    
    return facts_df.to_html()

def marsHem(browser):
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hems_image_urls = browser.find_by_css('a.product-item img')
    mars_hemisphere= []
    for i in range(len(hems_image_urls)):
        hemis ={}
        browser.find_by_css('a.product-item img')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemis['img_url'] = sample_elem['href']
        hemis['title'] = browser.find_by_css('h2.title').text
        mars_hemisphere.append(hemis)
        browser.back()
    return mars_hemisphere

def scrape_hemsiphere(html_text):
    hemi_soup=bs(html_text, "html.parser")

    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        title_elem = None
        sample_elem= None
    
    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres

if __name__ == "__main__":
    print(scrape_all())
