# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.4] - 2019-10-08
### Added
- Forgot to call `db.purge_old()`; should now work and prune old entries from the db

### Fixed
- Titles are now using the `<p>` tag, not `<span>`

## [1.0.3] - 2019-09-09
### Added
- Basic logging to log when a feed is incorrectly generated

### Changed
- When entries could not be generated, don't overwrite the feed
- `twitchprime.xml` renamed to `twitch-prime.xml` for readability
- Internal `twitchprime.png` also renamed to `twitch-prime.png` for consistency

## [1.0.2] - 2019-09-07
### Changed
- Use ' | ' delim instead of non-working `<br/>`

### Fixed
- Check if entry exists using title, not GUID - #1

## [1.0.1] - 2019-09-04
### Added
- Waits added, because the page would otherwise take too long on Raspberry Pi 2B
- Helper utility [`class_count.py`](class_count.py) added to find HTML classes to wait to load
- [readme](README.md)

## [1.0] - 2019-09-04
### Added
- Initial version
