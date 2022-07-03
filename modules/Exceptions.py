import discord

class Exceptions():

    class connection_error(Exception):
        def __init__(this, message):
            super().__init__(message)
            
    class not_popup(Exception):
        def __init__(this, message):
            super().__init__(message)
            
    class already_added(Exception):
        def __init__(this, message):
            super().__init__(message)
            
    def getException(this, idex):
        if idex == 1:
            embed = discord.Embed(title="We could not detect a popup, please contact someone", description="```Not a pop up | ERROR #1```", color=0x00ff2a)
            embed.set_thumbnail(url = "https://img.icons8.com/color/344/minus--v1.png")
            return embed
        elif idex == 2:
            embed = discord.Embed(title="We could not detect a popup/phishing, please contact someone", description="```Website Timeout / Connection Error | ERROR #2```", color=0x00ff2a)
            embed.set_thumbnail(url = "https://img.icons8.com/color/344/minus--v1.png")
            return embed
        elif idex == 3:
            embed = discord.Embed(title="We could not detect a popup/phishing, please contact someone", description="```Unknown Error | ERROR #3```", color=0x00ff2a)
            embed.set_thumbnail(url = "https://img.icons8.com/color/344/minus--v1.png")
            return embed
        elif idex == 4:
            embed = discord.Embed(title="We could not detect a popup/phishing, please contact someone", description="```DNS Looksup Failed | ERROR #4```", color=0x00ff2a)
            embed.set_thumbnail(url = "https://img.icons8.com/color/344/minus--v1.png")
            return embed
        elif idex == 5:
            embed = discord.Embed(title="We could not detect a popup/phishing, please contact someone", description="```The url is already in the database | ERROR #5```", color=0x00ff2a)
            embed.set_thumbnail(url = "https://img.icons8.com/color/344/minus--v1.png")
            return embed
        elif idex == 6:
            embed = discord.Embed(title="We could not detect a phishing, please contact someone", description="```Not a phishing | ERROR #6```", color=0x00ff2a)
            embed.set_thumbnail(url = "https://img.icons8.com/color/344/minus--v1.png")
            return embed
        elif idex == 7:
            embed = discord.Embed(title="We could not detect a popup/phishing, please contact someone", description="```Screenshot Failed | ERROR #7```", color=0x00ff2a)
            embed.set_thumbnail(url = "https://img.icons8.com/color/344/minus--v1.png")
            return embed
