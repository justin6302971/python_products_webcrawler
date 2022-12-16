
from bs4 import BeautifulSoup
from py_mini_racer import MiniRacer
import requests

def generate_proxy_ip_config_list():
    ctx = MiniRacer()

    l = {}
    u = list()
    country_code = 'tw'
    url = f'https://www.proxynova.com/proxy-server-list/country-{country_code}/'
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'html5lib')
    allproxy = soup.find_all("tr", {"data-proxy-id": True})
    for proxy in allproxy:
        proxy_item = proxy.find_all("td")
        try:
            ipscript = proxy_item[0].find("script")
            processed_ipscript = ipscript.string.replace(
                "document.write(", "")[:-1]
            ip = ctx.eval(processed_ipscript)
            l["ip"] = ip
        except:
            l["ip"] = None
        try:
            l["port"] = proxy_item[1].text.replace("\n", "").replace(" ", "")
        except:
            l["port"] = None
        try:
            l["country"] = proxy_item[5].text.replace(
                "\n", "").replace(" ", "")
        except:
            l["country"] = None
        if (l["port"] is not None):
            u.append(l)
        l = {}
    result = [x for x in u if x['ip'] is not None]
    return result



