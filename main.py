import urllib.request
import socket
from threading import Thread
from lxml import html
import requests
import re
import json

socket.setdefaulttimeout(20)


def check_proxy(pip):
    try:
        proxyDict = {
            "https": f"https://{pip}",
            "http": f"http://{pip}",
        }
        page = requests.get('https://ipx.ac', proxies=proxyDict, timeout=20)
        tree = html.fromstring(page.content)
        raw = tree.xpath('/html/body/script[9]/text()')
        match = re.match(r'.+ DATA = ({.+});.+', raw[0], re.S)
        if match:
            data = json.loads(match.group(1))
            usage = data['geo']['usage']
            flag = data['geo']['countryCode']
            country = data['geo']['countryName']
            if ("Non-Residential" not in usage and "Commercial" not in usage):
                with open("good.txt", "a+") as f:
                    f.write(f"{pip} {flag} {country}\n")

            print(usage, pip)
    except urllib.error.HTTPError as e:
        return e
    except Exception as detail:
        return detail
    return 0


proxies = open("proxy.txt").readlines()
threads = []

for proxy in proxies:
    thread = Thread(target=check_proxy, args=(
        proxy.replace("\n", "").strip(), ))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
