# Twitch Prime RSS Project

## Overview

This project scrapes the [Twitch Prime rewards page](https://twitch.amazon.com/tp/loot) to generate a RSS feed of items.

## Usage

Run [`class_count.py`](class_count.py) to get an idea of which classes to scrape, although not necessary. Run [`generate_feed.py`](generate_feed.py) to generate the feed. You can run [`db.py`](db.py) before anything else to create the database, but that is optional and redundant.

## Requirements

This code is designed around the following:

- Python 3.6+
    - `bs4` and its dependencies, for scraping
    - `selenium` and its dependencies, because the page only loads on "actual" browsers
    - `feedgen` and its dependencies, for the RSS feed itself
    - other [requirements](requirements.txt)
- pick and install a `webdriver` of your choice for `selenium`
    - I chose [Firefox](https://github.com/mozilla/geckodriver) (`geckodriver`) for this project, to run headless

## Setup

Set up your environment for self-hosting. Read [Requirements](#Requirements) for dependencies.
Python `venv` is highly recommended for managing your files, including dependencies.
Like so:

```
$ git clone <url> && cd twitch_rss
$ # venv may be installable in package management.
$ # For Debian-like distros, `apt install python3-venv`
$ python -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ # See directly below for setting up your config.
```

⚠ You will also need to install an appropriate `webdriver` as mentioned in Requirements. Make sure your chosen `webdriver` is in your `$PATH`.

## Live Version

See [here](https://dark-nova.me/twitch-prime.xml). This file is generated/updated every midnight Pacific Time via `cron`.

## Disclaimer

This project is not affiliated with or endorsed by [Twitch](https://twitch.tv) or [Amazon](https://www.amazon.com). See [`LICENSE`](LICENSE) for more detail.
