import logging
from typing import Dict, Tuple

import pendulum
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import db


URL = 'https://twitch.amazon.com/tp/loot'

LOGGER = logging.getLogger('twitch_prime_feed')
LOGGER.setLevel(logging.DEBUG)

FH = logging.FileHandler('feed.log')
FH.setLevel(logging.DEBUG)

CH = logging.StreamHandler()
CH.setLevel(logging.WARNING)

FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

LOGGER.addHandler(FH)
LOGGER.addHandler(CH)


def get_as_html():
    """Gets the true source of the URL.

    Returns:
        BeautifulSoup of page

    """
    # Choose your own webdriver if desired
    options = webdriver.firefox.options.Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(URL)
    try:
        element = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'offer__body__titles')
                )
            )
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        # with open('example.html', 'w') as f:
        #     f.write(soup.prettify())
        return soup
    finally:
        browser.quit()


def get_all_loot(fg: FeedGenerator, soup = None) -> None:
    """Gets all loot from page.

    Loot can be categorized as either 'in-game' or 'games'.

    Args:
        fg (FeedGenerator): the feed to add entries
        soup (optional): the soup to use; defaults to None

    """

    if soup is None:
        with open('example.html', 'r') as example:
            soup = BeautifulSoup(example, 'html.parser')

    for loot in soup.find_all('div', 'offer-list__content'):
        category = loot.find('h3').text.strip()
        get_loot(fg, loot, category)

    return


def get_loot(
    loot, category: str
    ) -> Dict[str, Tuple[str, str, str, pendulum.datetime]]:
    """Gets loot for a given `loot` type.

    Called by `get_all_loot`.

    Args:
        fg (FeedGenerator): the feed to add entries
        loot: bs4 object; the loot to parse
        category (str): either 'In-Game Loot and More'
            or 'Games with Prime'

    Returns:
        dict: {title: (description, category, link, pub_date)}

    """
    today = pendulum.today(tz='UTC')

    entries = {}

    for offer in loot.find_all('div', 'offer'):
        description = []

        info = offer.find('div', 'offer__body__titles')
        title = info.find('p', 'tw-amazon-ember-bold').text.strip()
        
        offered_by = info.find('p', 'tw-c-text-alt-2').text.strip()
        description.append(f'Offered by: {offered_by}')

        claim_info = offer.find('div', 'claim-info')
        expires_by = claim_info.find('span', '').text.strip()
        if expires_by == 'Offer ends soon':
            expires_by = 'soon'
        description.append(f'Expires: {expires_by}')

        try:
            link = offer.find('a')['href']
        except TypeError:
            link = URL
            description.append('Visit main page to claim offer.')

        if db.check_if_entry_exists(entry.title()):
            pub_date = db.get_entry_time(entry.title())
        else:
            pub_date = today
            db.add_entry(
                entry.title(),
                today
                )
        
        entries[title] = (
            ' | '.join(description),
            category,
            link,
            pub_date
            )

    return entries


def generate_feed(
    fg: FeedGenerator,
    entries: Dict[str, Tuple[str, str, str, pendulum.datetime]]
    ) -> None:
    """Generates the feed in ascending order of intended publication date.

    Args:
        fg (FeedGenerator): the feed to add entries
        entries (dict): {title: (description, category, link, pub_date)}

    """
    # Sort results by pub_date, then by name alphabetically
    for title, (description, category, link, pub_date) in sorted(
        entries.items(), key=lambda entry: (entry[1][3], entry[0])
        ):
        entry = fg.add_entry()
        entry.title(title)
        entry.category(
            category={
                'term': category,
                'label': category
                }
            )
        entry.link(href=link)
        entry.guid(link)
        entry.description(description=description)
        entry.pubDate(pub_date)


if __name__ == '__main__':
    fg = FeedGenerator()
    fg.title('Twitch Prime Games and Loot')
    fg.author({'name': 'Twitch Prime'})
    fg.description('Twitch Prime Games and Loot')
    fg.link(
        href=URL,
        rel='alternate'
        )
    # Change the below URL when self-hosting.
    fg.link(
        href='https://dark-nova.me/twitch-prime.xml',
        rel='self'
        )
    # Change the below URL when self-hosting.
    fg.logo('https://dark-nova.me/twitch-prime.png')
    fg.language('en-US')
    entries = get_all_loot(get_as_html())
    generate_feed(fg, entries)
    if len(fg.entry()) > 0:
        fg.rss_file('twitch-prime.xml')
    else:
        LOGGER.error(
            f'Could not generate entries for feed'
            )
    db.purge_old()
