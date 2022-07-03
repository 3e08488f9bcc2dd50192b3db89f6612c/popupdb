from modules import *
import requests
import threading
import os

def clearFolders():
    for filename in os.listdir("./files/screenshots/"):
        if filename != "_DONT_DELETE_THIS_FOLDER":
            os.remove(os.path.join("./files/screenshots/", filename))
    print("[#] Screenshot folder successfull is cleaned.")
    for filename in os.listdir("./files/srcs/"):
        if filename != "_DONT_DELETE_THIS_FOLDER":
            os.remove(os.path.join("./files/srcs/", filename))
    print("[#] Page-Source folder successfull is cleaned.")

def ReloadModules():
    return True

def main():
    proxy = None#ProxyManager()
    #popup = PopUps(proxy)
    discord = DiscordBot(proxy)
    discord.init()
    print("o")
    #
    #exit()
    while True:
        pass
if __name__ == "__main__":
    main()
