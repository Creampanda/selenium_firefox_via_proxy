from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
from random import choice

class Bot:
    def __init__(self, PROXY):
        #profile = webdriver.FirefoxProfile()
        #proxy_host = proxy.split(":")[0]
        #proxy_port = int(proxy.split(":")[1])
        #profile.set_preference('network.proxy_type',1)
        #profile.set_preference('network.proxy.http',proxy_host)
        #profile.set_preference('network.proxy.http_port', proxy_port)
        #profile.set_preference('network.proxy.https',proxy_host)
        #profile.set_preference('network.proxy.https_port', proxy_port)
        #profile.update_preferences()
        
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",

        }
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Firefox(firefox_profile=profile)


    def navigate(self, url):
        self.driver.get(url)


    def check_ip(self):
        self.driver.get('http://icanhazip.com')



def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, proxies=proxy)
    return r.text

def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    print(ip)
    print("---------------------")


def get_proxy_list():
    url = "https://www.proxynova.com/proxy-server-list/elite-proxies/"
    soup = BeautifulSoup(get_html(url),'lxml')
    trs = soup.find_all('tr')
    ip_list = []
    for tr in trs[1:]:
        #print(tr)
        try:
            ip_list.insert(0, str(tr.abbr.script)[24:-12]+ ':' + tr.td.next_sibling.next_sibling.text.strip())
            #print(str(tr.abbr.script)[24:-12])
            #print(tr.td.next_sibling.next_sibling.text.strip())
        except:
            continue
    return ip_list

def get_proxies_from_file():
    proxies = open('http_proxies.txt').read().split('\n')
    return proxies

def get_session(proxies):
    # construct an HTTP session
    session = requests.Session()
    # choose one random proxy
    proxy = choice(proxies)
    session.proxies = {"http": proxy, "https": proxy}
    return session

def main():
    #url = "http://sitespy.ru/my-ip"
    proxies = get_proxies_from_file()
    for proxy in proxies:
        session = requests.Session()
        session.proxies = {"http": proxy, "https": proxy}
        print(proxy)
        try:
            r = session.get("http://sitespy.ru/my-ip", timeout=1.5).text
            get_ip(r)
            bot = Bot(proxy)
            bot.check_ip()
        except Exception as e:
            continue
    
    return

if __name__ == "__main__":
    main()