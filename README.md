# Project Name

## Description
This project is designed to fetch a snapshot in time of a steam market items order book, using their item IDs. It employs a rotating proxy system, using proxies obtained from the Webshare API to overcome rate limitations imposed by the Steam API.
It doesn't actually do anything with the data yet(WIP) but with this you could extend it out and run it with cron jobs over an extended period of time to collect historical market data.

## Usage



### Configuration
1. Obtain a Webshare API key and set it as the `WEBSHARE_TOKEN` environment variable.
2. Populate the `csgo.json` file with the desired item IDs.

### Installation
```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
