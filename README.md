# *[Twitch][Twitch] Prime* RSS Project

## Overview

This project scrapes the [*Twitch Prime* rewards page](https://twitch.amazon.com/tp/loot) to generate a RSS feed of items.

## Usage

If you are having issues, you may run [`class_count.py`](class_count.py) to get an idea of which classes to scrape, although I find the script unnecessary now.

You may also run [`db.py`](db.py) before anything else to create the database, but that too is optional and redundant.

Run [`generate_feed.py`](generate_feed.py) to generate the feed.

## Requirements

This code is designed around the following:

- Python 3.6+
    - `bs4` for scraping
    - `selenium` because the page only loads on "actual" browsers
    - `feedgen` for the RSS feed itself
    - other [requirements](requirements.txt)

## Setup

Pick and install a `webdriver` of your choice for `selenium`. Your `webdriver` should also match the installed browser. If you have issues choosing, you may try [*Firefox*](https://github.com/mozilla/geckodriver) (`geckodriver`). They are tested for this project and run headless.

⚠️ Make sure your chosen `webdriver` and browser is in your `$PATH`.

## Live Version

See [here](https://dark-nova.me/twitch-prime.xml). This file is generated/updated every midnight Pacific Time via `cron`.

## Disclaimer

This project is not affiliated with or endorsed by [*Twitch*][Twitch] or [*Amazon*](https://www.amazon.com). See [`LICENSE`](LICENSE) for more detail.

[Twitch]: https://twitch.tv