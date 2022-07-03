import json
import requests
import re
import socket
import subprocess
import random
import discord
import phonenumbers
import zlib
import os
import urllib.request
import hashlib
import pytesseract
import numpy as np
import time, threading, io
from html_similarity import style_similarity
from datetime import datetime
from ipwhois import IPWhois
from urllib.parse import unquote, urlparse
from phonenumbers import carrier, geocoder
from modules import ProxyManager, Utils, Exceptions, screenshot
from phonenumbers.phonenumberutil import region_code_for_country_code, region_code_for_number
from bs4 import BeautifulSoup
from langdetect import detect_langs
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class PopUps():
    def __init__(this, proxy, lookupData, Exceptions):
        this.isHashesLoad = False
        this.isAgentsLoad = False
        this.hashes = this.loadHashes()
        this.userAgents = this.loadAgents()
        this.proxy = proxy
        this.mp3files = [".mp3", ".ogg"]
        this.messages = []
        this.files = []
        this.ex = Exceptions
        #this.tessdata_dir_config = '--tessdata-dir "C:/Users/believix/Desktop/Project/modules/Tesseract-OCR/tessdata"'
        this.lookupdata = lookupData
        this.dbs = os.listdir("files/sources")
        
        this.model = load_model('keras_model.h5')
        print("[#] AI model loaded")
        threading.Thread(target=this.importPopUps1).start()
        print("[#] Popup scan thread started")
        screenshot.startshotthread()
        print("[#] Screenshooter initialised")
        f=open("files/top10k.txt","r")
        this.top10k=f.read()
        f.close()
        print("[#] Top 10000 domains loaded")
    def __del__(this):
        this.isHashesLoad = False
        this.isAgentsLoad = False
    
    def getHashes(this):
        return this.hashes
        
    def getUserAgents(this):
        return this.userAgents
    def getrawnums(this,pagesource, raw):
        a=list(dict.fromkeys(re.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', pagesource)))
        if len(a)>0:
            return a #+031 528 25 45, 0808-143-3686, 022 548 36 69
        return list(dict.fromkeys(re.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', raw)))
    def aiurlscan(this,result):
        data = np.ndarray(shape=(1, 224, 224,3), dtype=np.float32)
        # Replace this with the path to your image
        fd = urllib.request.urlopen(result["screenshot"])
        image_file = io.BytesIO(fd.read())
        image = Image.open(image_file).convert('RGB')
        #image = Image.open(img).convert('RGB')
        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = this.model.predict(data)
        #print(prediction)
        prediction=list(prediction[0])
        #print(prediction)
        return prediction[0]*100
    def getNumber(this, pagesource):
        nums = list(dict.fromkeys(re.findall(r'[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]', pagesource))) #+031 528 25 45, 0808-143-3686, 022 548 36 69
        langs=[None]
        try:
            langs = detect_langs(pagesource)
        except:
            pass
        print(langs)
        print(nums)
        for x in range(0, len(nums)):
            if len(nums[x].split("(050)"))>1 or nums[x][0:3] == "050":
                if nums[x][0]!="+":
                    nums[x]="+81 "+nums[x]
            for y in list(langs):
                try:
                    if y!=None:
                        print(str(y).split(":")[0].upper())
                        parsednum = phonenumbers.parse(nums[x],Utils.lang2code(str(y).split(":")[0].upper()))
                        nn = phonenumbers.format_number(parsednum, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                        return nn
                    else:
                        parsednum = phonenumbers.parse(nums[x],None)
                        nn = phonenumbers.format_number(parsednum, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                        return nn
                except:
                    pass
            
            tnum = "-".join("-".join("-".join(nums[x].split(" ")).split("(")).split(")"))
            tnum = tnum.replace('+', '').replace('-', '')
            tnum = '+' + tnum[0:]
            tnum = "+81" + tnum[2:] if Utils.getPhoneCountry(tnum) == "Japan" else tnum # Japanese numbers
            tnum = "+1" + tnum[1:] if Utils.getPhoneCountry(tnum) == "US" else tnum # US numbers
            tnum = "+44" + tnum[2:] if Utils.getPhoneCountry(tnum) == "UK" else tnum # UK numbers
            
            try:
                nn = phonenumbers.parse(tnum, lang)
                if phonenumbers.is_valid_number(nn):
                    return tnum
            except:
                pass
        if len(nums) == 0:
            return "N/A"
        return nums[0]

    def getPhone(this, url):
        #pytesseract.tesseract_cmd = r"C:/Users/believix/Desktop/Project/modules/Tesseract-OCR/tesseract.exe"
        text = pytesseract.image_to_string("files/screenshots/{}.png".format(Utils.crc(url)))#, config=this.tessdata_dir_config)
        
        print(text)
        nums = list(dict.fromkeys(re.findall(r"[\+\(]?\d{1,4}[\s-]\d{1,4}\)?[\s-]?\d{2,4}[\s-]?\d{4,6}", text) + re.findall(r"[\+\(]?\d{0,4}[\s-]?\d{1,4}\)?[\s-]?\d{2,4}[\s-]?\d{4,6}", text) + re.findall(r"[\+\(]?\d{0,4}[\s-]?\d{1,4}\)?[\s-]?\d{2,4}[\s-]?\d{4,6}", text) + re.findall(r"\d{0,4}[\s]\d{1,4}[\s]\d{2,4}[\s]\d{4,6}", text)))
        if len(nums) == 0:
            return "N/A"
        return nums[0]
    def getIP(this, host):
        host = Utils.to_domain(host)
        try:
            return socket.gethostbyname(host)
        except:
            return "N/A"
        
    def loadHashes(this):
        if not this.isHashesLoad:
            hashes = []
            cnt = 0
            f = open("./files/hashes.txt", "r")
            for line in f.readlines():
                hashes.append(line.rstrip('\n'))
                cnt += 1
            f.close()
            print("[#] Total Loaded Hashes: "+ str(cnt))
            this.isHashesLoad = True
            return hashes
                
    def loadAgents(this):
        if not this.isAgentsLoad:
            agents = []
            cnt = 0
            f = open("./files/agents.txt", "r")
            for line in f.readlines():
                agents.append(line.rstrip('\n'))
                cnt += 1
            f.close()
            print("[#] Total Loaded User-Agents: "+ str(cnt))
            this.isAgentsLoad = True
            return agents
        
    def randomAgent(this):
        try:
            return random.choice(this.userAgents)
        except IndexError:
            return "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5"
            
    def sendMessage(this, url, phone, confidence, uri):
        isTollFree = ""
        countryinfo = "N/A"
        car = "N/A"
        ip = this.getIP(uri)
        if ip != "N/A":
            try:
                whois = IPWhois(this.getIP(uri))
                whois = whois.lookup_whois()
            except:
                whois = {}
        if phone != "N/A":
            try:
                phn = phonenumbers.parse(phone, None)
                countryinfo = geocoder.description_for_number(phn, 'en')
                car = carrier.name_for_number(phn, 'en')
            except:
                pass
        if len(phone) >= 5:
            if Utils.isTollFreePhone('+' + phone[2:5]):
                isTollFree = " (Toll Free)"
        embed = discord.Embed(title="(Microsoft Pop Up / Tech Support Scam)", color=0x00ff62)
        embed.set_thumbnail(url="https://img.icons8.com/color/344/list--v1.png")
        embed.add_field(name = "ID:", value = Utils.crc(url.url), inline = False)
        embed.add_field(name = "URL:", value = str(url.url), inline = False)
        if len(phone) > 0:
            print(phone[2:5])
            if Utils.isTollFreePhone('+' + phone[2:5]):
                isTollFree = " (Toll Free)"
        embed.add_field(name = "Telephone Number:", value = str(phone) + isTollFree, inline = False)
        embed.add_field(name = "Confidence:", value = str(round(confidence, 2)) + "%", inline = False)
        embed.set_image(url="attachment://"+Utils.crc(url.url)+".png")
        this.lookupdata["popups"].append({
        "id" : Utils.crc(uri), 
        "url" : str(url.url),
        "date" : str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')),
        "confidence" : str(confidence),
        "textconfidence" : '0',
        "ip" : str(ip),
        "asn" : whois["asn"],
        "asndescription" : str(whois["nets"][0]["description"]),
        "telephone_number" : str(phone).replace(' ', '-'),
        "isTollFree" : bool(isTollFree),
        "phone_country" : str(countryinfo),
        "phone_carrier" : str(car),
        "abuse_emails" : whois["nets"][0]["emails"]
        })
        
        embed.set_footer(text="Type "+Utils.configBot(str("bot.prefix"))+"lookup "+Utils.crc(uri) + " for see deep information about the pop up.")
        outembed=embed
        embed.set_image(url="attachment://"+Utils.crc(uri)+".png")
        this.messages.append([Utils.crc(uri),embed])
        print("posted")
        print(this.messages)
        Utils.saveLookup(this.lookupdata)
        return [Utils.crc(uri),outembed]
    
    def basicscan(this,result):
        url=result['task']['url']
        if Utils.to_domain(url) in this.top10k:
            return
        try:
            r1 = requests.get(url, timeout=5, allow_redirects = True, verify=False)
        except:
            return
        #r1 = this.proxy.requestProxy(url, timeout=4, allow_redirects = True, headers = {"user-agent":useragent})
        soup = BeautifulSoup(r1.text, 'html.parser')
        res = soup.get_text()
        r2 = this.getrawnums(res, r1.text)
        #
        if len(r2)>0:
            textsim=this.textAI(r1.text)
            if textsim>10:
                if this.aiurlscan(result)>40:
                    print("[#] URL --> "+Utils.to_domain(url)+" MAY BE A POP UP")
                    try:
                        this.isPopUp(url)
                    except:
                        pass
                else:
                    print("[#] URL --> "+Utils.to_domain(url)+" NOT A POP UP")
                    with open("./files/notpopups.txt", "a") as f:
                        f.write(url+'\n')
                        f.close()
        else:
            print("[#] URL --> "+Utils.to_domain(url)+" NOT A POP UP")
            with open("./files/notpopups.txt", "a") as f:
                f.write(url+'\n')
                f.close()
    def importPopUps1(this): # urlscan.io
        urls=[]
        while True:
            if len(urls)>201:
                urls=urls[-200:]
            while True:
                try:
                    r1 = requests.get("https://urlscan.io/json/live/")
                    j = json.loads(r1.text)
                except:
                    time.sleep(5)
                    continue
                break
            """
            fr=open("./files/notpopups.txt", "r")
            r=fr.read().split("\n")
            fr.close()
            fr=open("./files/domains.txt", "r")
            r=r+fr.read().split("\n")
            fr.close()
            """
            r=[]
            for result in j["results"]:
                if not result['task']['url'] in r:
                    if not result["task"]["url"] in urls:
                        
                        #
                        threading.Thread(target=this.basicscan, args=(result,)).start()
                        urls.append(result["task"]["url"])
                time.sleep(0.01)
            time.sleep(1)

    def isAlreadyNotPopup(this, domain):
        f = open("./files/notpopups.txt", "r")
        for line in f:
            if domain in line:
                f.close()
                return True
        f.close()
        return False
        
    def isAlreadyPopup(this, domain):
        f = open("./files/domains.txt", "r")
        for line in f:
            if domain in line:
                f.close()
                return True
        f.close()
        return False
    
    def checkHash(this, url):
        files = []
        cnt = 0
        soup = BeautifulSoup(url.text, 'html.parser')
        hashes1 = []
        r1 = url.url
        #r1 = r1.replace("index.html", "").replace("index.php", "")
        r1 = r1.rpartition('/')[0] + '/'
        if r1[-1] == "/":
            r1 = r1[:-1]
        for x, link in enumerate(soup.find_all('img')+soup.find_all('source')):
            files.append(link.get('src'))
            if files[x] != None and files[x] != "":
                if files[x][0:5] == "data:":
                    files[x] = None
                if files[x][0:4] != "http":
                    if files[x][0] != "/":
                        files[x] = "/" + files[x]
                    files[x] = r1 + files[x]
        files = Utils.removeListDuplicates(files)
        files = list(filter(None, files))
        #print(files)
        path = "files/srcs/"+Utils.crc(url.url)+"/"
        
        #os.chdir(path)
        downfiles=[]
        for fil in files:
            url = urlparse(fil)
            try:
                req=requests.get(fil, timeout=10, verify=False)
                if req.status_code == 200:
                    downfiles.append(req.content)
            except:
                pass
        downfiles = Utils.removeListDuplicates(downfiles)
        for filename in downfiles:
            hashes1.append(hashlib.sha256(filename).hexdigest())
        for h in hashes1:
            if h in this.hashes:
                cnt += 1
                hashes1.remove(h)
        hashes1=[] #free mem
        print(cnt)
        if cnt>0: #cnt >= len(files) // 2 and cnt > 1: #make it less aggressive. not all popups copy everything
            if not os.path.exists(path):
                os.makedirs(path)
            for fil in files:
                try:
                    urllib.request.urlretrieve(fil, path + os.path.basename(url.path))
                except:
                    pass
            f = open("./files/hashes.txt", "a")
            f.write("\n".join(hashes1))
            print(hashes1)
            print("[#] {} NEW HASHES ADDED".format(len(hashes1)))
            f.close()
            if cnt > len(hashes1):
                return 2
            return 1
        return 0
    
    def AIPopup(this, url):
        
        data = np.ndarray(shape=(1, 224, 224,3), dtype=np.float32)
        image = Image.open("./files/screenshots/"+Utils.crc(url)+".png").convert('RGB')
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = this.model.predict(data)
        prediction = list(prediction[0])
        return prediction[0] * 100
    def textAI(this,cnt):
        tot=0
        cnt=0
        for x in range(10):
            try:
                f=open("files/sources/"+random.choice(this.dbs),"r")
                r=f.read()
                f.close()
                tot += style_similarity(r,cnt)
                cnt+=1
            except:
                pass
        if cnt==0:
            tot=100
        else:
            tot=tot/cnt
        
        tot=round(tot*1000,2)
        if tot>100:
            tot=100
        
        return tot
    def isPopUp(this, url):
        domain = Utils.to_domain(url)
        """
        if this.isAlreadyNotPopup(url):
            raise this.ex.already_added("The url is already in the database.")
        if this.isAlreadyPopup(url):
            raise this.ex.already_added("The url is already in the database.")
        """
        try:
            if domain in this.top10k:
                raise this.ex.not_popup("The url is not popup")
                return
            useragent = this.randomAgent()
            r1 = requests.get(url, timeout=4, allow_redirects = True, headers = {"user-agent":useragent}, verify=False)
            #r1 = this.proxy.requestProxy(url, timeout=4, allow_redirects = True, headers = {"user-agent":useragent})
            hout=this.checkHash(r1)
            if(hout > 0):
                soup = BeautifulSoup(r1.text, 'html.parser')
                res = soup.get_text()
                r2 = this.getNumber(res)
                screenshot.getScreenshot(url)
                r3 = this.AIPopup(url)
                if (r3<20) and (hout == 1):
                    raise this.ex.not_popup("The url is not popup")
                if r2 == "N/A":
                    r2 = this.getPhone(url)
                output=this.sendMessage(r1, r2, r3, url)
                print("[#] URL --> "+url+" POP UP")
                with open("./files/domains.txt", "a") as f:
                    f.write(url+'\n')
                    f.close()
                return output
            else:
                with open("./files/notpopups.txt", "a") as f:
                    f.write(url+'\n')
                    f.close()
                print("[#] URL --> "+url+" NOT A POP UP")
                raise this.ex.not_popup("The url is not popup")
        except requests.exceptions.ConnectionError:
            print("[#] URL --> "+url+" CONNECTION ERROR")
            with open("./files/notpopups.txt", "a") as f:
                f.write(domain+'\n')
                f.close()
            raise this.ex.connection_error('The url is not valid')
        except requests.exceptions.ReadTimeout:
            print("timed out")
        except requests.exceptions.MissingSchema:
            return "url must be start with https:// or http://"
