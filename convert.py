from bs4 import BeautifulSoup
from selenium import webdriver

URL = 'https://twitch.amazon.com/tp/loot'


def get_as_html():
    """Gets the true source of the URL."""
    # Choose your own webdriver if desired
    options = webdriver.firefox.options.Options()
    options.headless = True
    browser = webdriver.Firefox(options = options)
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    with open('example.html', 'w') as f:
        f.write(soup.prettify())

def get_loot(soup = None):
    """Gets loot from page.

    Args:
        soup (optional): the soup to use; defaults to None

    """

    if soup is None:
        with open('example.html', 'r') as example:
            soup = BeautifulSoup(example, 'html.parser')

    for offer in soup.find_all('div', 'offer'):
        offer_name = offer.find('span').text.strip()
        try:
            offer_link = offer.find('a')['href']
        except TypeError:
            offer_link = URL

    return soup

if __name__ == '__main__':
    #get_as_html()
    pass
