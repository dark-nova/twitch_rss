from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
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


def get_all_loot(soup = None):
    """Gets all loot from page.

    Loot can be categorized as either 'in-game' or 'games'.

    Args:
        soup (optional): the soup to use; defaults to None

    """

    if soup is None:
        with open('example.html', 'r') as example:
            soup = BeautifulSoup(example, 'html.parser')

    for loot in soup.find_all('div', 'offer-list__content'):
        category = loot.find('h3').text.strip()
        get_loot(loot, category)

    return


def get_loot(loot, category):
    """Gets loot for a given `loot` type.

    Called by `get_all_loot`.

    Args:
        loot: the loot to parse

    """
    for offer in loot.find_all('div', 'offer'):
        offer_name = offer.find('span').text.strip()
        try:
            offer_link = offer.find('a')['href']
        except TypeError:
            offer_link = URL


if __name__ == '__main__':
    #get_as_html()
    pass
