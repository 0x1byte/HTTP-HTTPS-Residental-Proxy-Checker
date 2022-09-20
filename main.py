import urllib.request
import socket
from threading import Thread
from lxml import html
import requests
import re
import json

socket.setdefaulttimeout(20)


def check_proxy_http(pip):
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
                with open("http_good_residental.txt", "a+") as f:
                    f.write(f"{pip} {flag} {country} {usage}\n")
            else:
                with open("http_good_other.txt", "a+") as f:
                    f.write(f"{pip} {flag} {country} {usage}\n")
            print(usage, pip)
    except urllib.error.HTTPError as e:
        return e
    except Exception as detail:
        return detail
    return 0
def check_proxy_socks5(pip):
    try:
        proxyDict = {
            "https": f"socks5://{pip}",
            "http": f"socks5://{pip}",
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
                with open("socks5_good_residental.txt", "a+") as f:
                    f.write(f"{pip} {flag} {country} {usage}\n")
            else:
                with open("socks5_good_other.txt", "a+") as f:
                    f.write(f"{pip} {flag} {country} {usage}\n")
            print(usage, pip)
    except urllib.error.HTTPError as e:
        return e
    except Exception as detail:
        return detail
    return 0
def check_proxy_socks4(pip):
    try:
        proxyDict = {
            "https": f"socks4://{pip}",
            "http": f"socks4://{pip}",
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
                with open("socks4_good_residental.txt", "a+") as f:
                    f.write(f"{pip} {flag} {country} {usage}\n")
            else:
                with open("socks4_good_other.txt", "a+") as f:
                    f.write(f"{pip} {flag} {country} {usage}\n")
            print(usage, pip)
    except urllib.error.HTTPError as e:
        return e
    except Exception as detail:
        return detail
    return 0


proxies = open("{}.txt".format(input("Enter Proxy Filename: "))).readlines()
threads = []

proxy_type = input("Enter Proxy Type(socks4/socks5/http): ")

if proxy_type.lower() == "http":
    for proxy in proxies:
        thread = Thread(target=check_proxy_http, args=(
            proxy.replace("\n", "").strip(), ),daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
if proxy_type.lower() == "socks5":
    for proxy in proxies:
        thread = Thread(target=check_proxy_socks5, args=(
            proxy.replace("\n", "").strip(), ),daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
if proxy_type.lower() == "socks4":
    for proxy in proxies:
        thread = Thread(target=check_proxy_socks4, args=(
            proxy.replace("\n", "").strip(), ),daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()