import os
import json
import requests
from collections import deque
from requests.exceptions import RequestException, ProxyError, Timeout, HTTPError
import time

###Webshare had a rotating proxy feature but i was getting rate limited, so this grabs all proxies and manages the functionality for rotating them 
class ProxyManager:
    def __init__(self):
        self.proxies = deque(self.get_all_proxies())

    def get_all_proxies(self):
        proxies_list = []
        next_page = "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25"

        while next_page:
            response = requests.get(
                next_page,
                headers={"Authorization": os.environ["WEBSHARE_TOKEN"]}
            )
            proxies_data = response.json()

            for proxy_data in proxies_data["results"]:
                if proxy_data["valid"]:
                    proxy_url = f'{proxy_data["username"]}:{proxy_data["password"]}@{proxy_data["proxy_address"]}:{proxy_data["port"]}'
                    proxy_dict = {'http:': f'http://{proxy_url}', "https": f'https://{proxy_url}'}
                    proxies_list.append(proxy_dict)

            next_page = proxies_data["next"]
        return proxies_list

    def rotate(self):
        self.proxies.rotate(-1)

    def remove(self, proxy):
        self.proxies.remove(proxy)




class HistogramFetcher:
    def __init__(self, proxy_manager):
        self.proxy_manager = proxy_manager
        self.success = 0
        self.failed = 0

    def fetch(self, item_name, item_id):
        baseurl = "https://steamcommunity.com/market/itemordershistogram"
        url = f'{baseurl}?norender=1&country=GB&language=english&currency=1&item_nameid={item_id}&two_factor=0'
        proxy = self.proxy_manager.proxies[0]

        try:
            histogram = requests.get(url, proxies=proxy, timeout=2)
            print(proxy)
            histogram.raise_for_status()
        except RequestException as err:
            self.handle_error(err, proxy)
            return None

        self.proxy_manager.rotate()
        self.success += 1
        return histogram.json()

    def handle_error(self, err, proxy):
        if isinstance(err, ProxyError):
            if self.proxy_manager.proxies:
                self.proxy_manager.remove(proxy)
                print('Proxy error: Removed proxy from the list')
            else:
                print('Proxy error: No more proxies available')
        elif isinstance(err, Timeout):
            print('Request has timed out')
        elif isinstance(err, HTTPError):
            print(f'HTTP error: {err.response.status_code}')
            self.proxy_manager.remove(proxy)
        else:
            print(f'An unexpected error occurred: {err}')
        self.failed += 1

def main():
    with open('csgo.json', 'r') as file:
        item_ids = json.load(file)

    proxy_manager = ProxyManager()
    fetcher = HistogramFetcher(proxy_manager)
    items = deque(item_ids.items())

    while items:
        if not proxy_manager.proxies:
            print('No more proxies available')
            break

        item_name, item_id = items.popleft()
        histogram = fetcher.fetch(item_name, item_id)

        if histogram:
            ask_prices = [item[0] for item in histogram["buy_order_graph"]]
            ask_volume = [item[1] for item in histogram["buy_order_graph"]]
            bid_prices = [item[0] for item in histogram["sell_order_graph"]]
            bid_volumes = [item[1] for item in histogram["sell_order_graph"]]

            print(f'Fetched: {item_name}, Running total:  [{fetcher.success} ✅]     [{fetcher.failed} 🚫]')
        else:
            print(f"Failed to get {item_name}  [{fetcher.success}✅]     [{fetcher.failed} 🚫]")
        #time.sleep(1)
if __name__ == "__main__":
    main()