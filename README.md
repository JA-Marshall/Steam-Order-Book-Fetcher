# Project Name

## Description
This project is designed to fetch a snapshot in time of a steam market items order book,
It employs a rotating proxy system, using WebShare's API to overcome rate limitations imposed by the Steam API.
It doesn't actually do anything with the data yet(WIP) but with this you could extend it out and run it with cron jobs over an extended period of time to collect historical market data.

![image](https://github.com/JA-Marshall/Steam-Order-Book-Fetcher/assets/9871373/c9c735ff-57ae-46b9-b58a-37ca3603729b)


Historical order book market data could provide a deeper insight into CSGOs market's dynamics by offering detailed information beyond just volume and price.
By aggregating this data over an extended period of time more detailed analysis can be done on the market 




### Configuration
1. Obtain a Webshare API key and set it as the `WEBSHARE_TOKEN` environment variable.
2. Populate the `csgo.json` file with the desired item IDs.

