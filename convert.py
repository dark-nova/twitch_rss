from bs4 import BeautifulSoup
from selenium import webdriver

URL = 'https://twitch.amazon.com/tp/loot'


def get_as_html():
    # Choose your own webdriver if desired
    browser = webdriver.Firefox()
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    with open('example.html', 'w') as f:
        f.write(soup.prettify())

if __name__ == '__main__':
    get_as_html()
