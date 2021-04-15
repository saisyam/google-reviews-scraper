from bs4 import BeautifulSoup
from splinter import Browser
import time
import sys

def get_html(url, count):
    browser = Browser("chrome", headless=True)
    browser.visit(url)
    time.sleep(2)
    rlen = get_review_count(browser.html)
    while rlen < count:
        browser.execute_script('document.querySelector("div.section-layout.section-scrollbox.scrollable-y.scrollable-show").scrollTop = document.querySelector("div.section-layout.section-scrollbox.scrollable-y.scrollable-show").scrollHeight')
        time.sleep(2)
        rlen = get_review_count(browser.html)
    html = browser.html
    browser.quit()
    return html

def get_review_count(html):
    soup = BeautifulSoup(html, "html5lib")
    section_div = soup.find('div',{'class':'section-layout'})
    reviews = section_div.find_all('div', {'class':'section-review'})
    return len(reviews)

def get_reviews(html):
    soup = BeautifulSoup(html, "html5lib")
    section_div = soup.find('div',{'class':'section-layout'})
    reviews = section_div.find_all('div', {'class':'section-review'})
    for r in reviews:
        rsection = r.find_all('div', {'class':'section-review-line'})
        title_section = rsection[0].find('div',{'class':'section-review-title'})
        user = title_section.find('span').get_text().strip()
        stars = rsection[1].find('span', {'class':'section-review-stars'})['aria-label'].strip()
        review_text = rsection[1].find('div',{'class':'section-review-review-content'}).find('span',{'class':'section-review-text'}).get_text().strip()
        rating = int(stars.split(' ')[0])
        yield {
            "rating": rating,
            "user": user,
            "review": review_text.replace("\n",'')
        }


# python3 google-scraper.py <urls.txt> <count>
if len(sys.argv) == 3:
    f = open(sys.argv[1], "r")
    lines = f.readlines()
    f.close()
    for url in lines:
        html = get_html(url, int(sys.argv[2]))
        for r in get_reviews(html):
            print(r)
else:
    print("Usage: python3 google-scraper.py <urls.txt> <count>")
    exit()