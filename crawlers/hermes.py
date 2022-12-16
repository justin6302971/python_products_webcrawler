import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import random
from helpers.proxyhelper import generate_proxy_ip_config_list


def set_proxy_ip():
    ip_config_list = generate_proxy_ip_config_list()
    ip_config = random.choice(ip_config_list)
    ip = ip_config['ip']
    port = ip_config['port']
    proxy = {
        # "https": f'http://{ip}:{port}',
        "http": f'http://{ip}:{port}'
    }
    return proxy


def set_header_user_agent():
    user_agent = UserAgent()
    return user_agent.random


def collect_product(url):
    user_agent = set_header_user_agent()
    print(f"collect_product,agent: {user_agent}")

    proxy = set_proxy_ip()
    print(f"collect_product,proxy: {proxy}")

    # test_url = 'https://httpbin.org/ip'

    # response = requests.get(test_url,proxies=proxy)
    # print(response.json())


    isResponseValid = True
    response = None
    try:
        response = requests.get(
            url, headers={'user-agent': user_agent}, proxies=proxy, timeout=5)
        print(f'collect_product, use useragent and proxy to get product data')
        
    except Exception as ex:
        isResponseValid = False
        print(f'collect_product, got issue when requesting with proxy: {ex}')
        pass

    if isResponseValid == False:
        try:
            response = requests.get(url, headers={'user-agent': user_agent}, timeout=5)
            print(f'collect_product, use useragent only to get product data')

            isResponseValid=False
        except Exception as ex: 
            print(f'collect_product, got issue when requesting: {ex}')
            pass
        
    products = []

    if response is None:
        print(f'collect_product, response is not valid, should check requests logic and params')
        return products

    
    soup = BeautifulSoup(response.content, 'html5lib')
    # print(soup)
    items = soup.findAll('div', attrs={'class': "product-item-meta"})

    if len(items)==0:
        print('collect_product, can\'t find any products, might be blocked by reCAPTCHA or url is not valid')
    
    # print("retrieved content:\n")
    # print(items)

    for item in items:
       # print("retrieved content item:\n")
       # print(item.prettify())
        product_meta = {}
        try:
            product_meta["code"] = item['id']
            product_desc = " ".join(item.text.split())
            product_meta["description"] = product_desc

            products.append(product_meta)
        except TypeError as tex:
            print(f'collect_product, type error:{str(tex)}')
            continue
        except Exception as ex:
            print(f'collect_product, error:{str(ex)}')
            continue

    print(f"collect_product, product counts: {len(products)}")

    return products
