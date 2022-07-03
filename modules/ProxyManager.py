import requests
import random
import os
import threading
import time
import math
from modules import Utils
class ProxyManager():
    def checkproxies(this,i):
        for y in i:
            if not (y in this.proxies):
                proxyDict = {
                              "http"  : 'socks4://'+y,
                              "https" : 'socks4://'+y
                            }
                try:
                    x=requests.get("https://api.ipify.org",proxies=proxyDict, timeout=2, allow_redirects=True)
                except:
                    continue
                else:
                    #print(y)
                    #print("http found")
                    
                    this.proxies.append(y)
    def getproxs(this):
        while True:
            if len(this.proxies) > 50:
                #this.proxies = this.proxies[0:50]
                time.sleep(10)
                continue
            while True:
                try:
                    x = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all', allow_redirects=True)
                except:
                    continue
                else:
                    break
            r = x.text
            thd = []
            z = r.split('\n')

            for y in range(0, len(z)):
                z[y] = z[y].split('\r')[0]

            for x in range(0, math.floor(len(z) / 5) - 1):
                thd.append(threading.Thread(target=this.checkproxies, args=(z[x * 5:(x + 1)
                           * 5], )))
                thd[-1].start()
            for x in range(0, len(thd)):
                thd[x].join()
            time.sleep(30)
    def requestProxy(this,*args,**kwargs):
        this.mutex.acquire()
        a=[]
        while True:
            if len(this.proxies)>5:
                rng=5
            else:
                rng=len(this.proxies)
            if rng != 0:
                break
            time.sleep(5)
        for x in range(rng):
            try:
                proxyDict = {
                      "http"  : 'socks4://'+this.proxies[0],
                      "https" : 'socks4://'+this.proxies[0]
                    }
                r=requests.get(*args,**kwargs,proxies=proxyDict)
            except requests.exceptions.ConnectionError:
                a.append(this.proxies.pop(0))
            else:
                this.mutex.release()
                return r
        try:
            r=requests.get(*args,**kwargs)
        except:
            this.proxies=a+this.proxies
            this.mutex.release()
            raise requests.exceptions.ConnectionError
            return
        else:
            this.mutex.release()
            return r
    def __init__(this):
        this.mutex=threading.Lock()
        this.proxies = []
        this.proxythread=threading.Thread(target=this.getproxs)
        this.proxythread.start()
    
