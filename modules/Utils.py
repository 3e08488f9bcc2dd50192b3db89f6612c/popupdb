import configparser
import phonenumbers
import os
import json, zlib
config = configparser.ConfigParser()
config.read("config.properties")

def configBot(arg):
    return config.get("bot", arg)

def to_domain(url):
    if 'http://' in url:
        url = url.split('http://')[1].split('/')[0]
    elif 'https://' in url:
        url = url.split('https://')[1].split('/')[0]
    return url

def lang2code(lang):
    table={"JA":"JP"}
    if lang in table:
        return table[lang]
    return lang

def getPhoneCountry(phone):
    if phone[0] == "(" and phone[4] == ")" :
        phone = "+1" + phone
    try:
        x = phonenumbers.parse(phone, None)
        country = phonenumbers.geocoder.description_for_number(x, 'en')
    except:
        if isTollFreePhone(phone) or int(phone[1]) >= 2 and int(phone[4]) >= 2 and len(phone) == 10:
            country = 'US'
        #elif phone[1:3] == '08' or phone[1:3] == '07':
            #country = 'UK'
        elif (phone.startswith("+050") or phone.startswith("+052") or phone.startswith("+034") or phone.startswith("+090")):
            country = "Japan"
        else:
            country = "Unknown country"
    return country


def isTollFreePhone(phone):
    if phone.startswith("+844") or phone.startswith("+855") or phone.startswith("+866") or phone.startswith("+888") or phone.startswith("+800") or phone.startswith("+833") or phone.startswith("+877"):
        return True
    return False
    
def removeListDuplicates(a):
    return list(dict.fromkeys(a))

def loadLookup():
    with open('./files/db.json', 'r') as f:
      data = json.loads(f.read())
    f.close()
    return data
def record(url):
    os.system("bash -c \"DISPLAY=:2 chromium --app="+url+" --start-fullscreen --window-size=1366,768&\" && ffmpeg -f x11grab -y -r 10 -i :2.0 -y -t 00:00:15 files/recordings/"+to_domain(url)+".mp4 && killall chromium")
def saveLookup(T):
    with open("./files/db.json",'w') as f:
        f.write(json.dumps(T, indent = 5))
    f.close()
def crc(inpt):
    return str(zlib.crc32(str(inpt).encode()))
