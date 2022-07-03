import discord
import threading
import asyncio
import base64, subprocess
from discord.ext import commands, tasks
from modules import Utils, PopUpManager, Exceptions

class DiscordBot():
    def __init__(this, proxy):
        this.client = commands.Bot(command_prefix=Utils.configBot(str("bot.prefix")), activity=discord.Activity(name = 'eating scammers'), intents=discord.Intents.all())
        this.lookupData = Utils.loadLookup()
        this.ex = Exceptions.Exceptions()
        this.PopUpManager = PopUpManager.PopUps(proxy, this.lookupData, this.ex)
        #this.PhishManager = PhishManager.Phishings(proxy, this.lookupData, this.ex)
        this.channels = Utils.configBot(str("bot.infochannels")).split(',')
        
        @this.client.event
        async def on_ready():
            print("[#] Username: %s" % this.client.user.name)
            print("[#] ID: %s" % this.client.user.id)

        @this.client.command()
        async def add(ctx, url):  # Checks if url is pop up
            embed = discord.Embed(title="Loading...", color=0x00ff62)
            message=await ctx.send(embed=embed)
            
            try:
                out=this.PopUpManager.isPopUp(url)
                cc = this.client.get_channel(int(983737219510595604))
                fil = discord.File("./files/screenshots/"+out[0]+".png", filename=out[0]+".png")
                img_msg = await cc.send(file=fil)
                await asyncio.sleep(2)
                out[1].set_image(url=img_msg.attachments[0].url)
                await message.edit(embed=out[1])
            except this.ex.connection_error:
                await message.edit(embed = this.ex.getException(2))
            except this.ex.not_popup:
                await message.edit(embed = this.ex.getException(1))
                
        @this.client.command()
        async def record(ctx, url):
            filedir = "./files/recordings/" + Utils.to_domain(url) + ".mp4"
            if os.path.exists(filedir):
                await ctx.send(file=discord.File(filedir, filename="video.mp4"))
            else:
                await ctx.send("Recording...")
                Utils.record(url)
                await ctx.send(file=discord.File(filedir, filename="video.mp4"))
        @this.client.command()
        async def callflood(ctx,tok,sec,num):
            if ctx.message.author.id != 507461745548460032:
                await ctx.send("go away skid")
                return
            num=num[0:3]+")"+num[3:]
            num="("+num
            num=num[0:9]+"-"+num[9:]
            subprocess.Popen(["python3","flooder.py",tok,sec,num])
            await ctx.send("flooded")
        @this.client.command()
        async def lookup(ctx, Hash):
            ID = URL = Date = IP = ASN = ASNDESC = PHONE = PHONECOUNTRY = PHONECARRIER = ""
            TOLL = False
            ABEMails = []
            for x in this.lookupData["popups"]:
                if x["id"] == Hash:
                    ID = x["id"]
                    URL = x["url"]
                    Date = x["date"]
                    IP = x["ip"]
                    ASN = x["asn"]
                    ASNDESC = x["asndescription"]
                    PHONE = x["telephone_number"]
                    TOLL = x["isTollFree"]
                    print(x["isTollFree"])
                    PHONECOUNTRY = x["phone_country"]
                    PHONECARRIER = x["phone_carrier"]
                    ABEMails = x["abuse_emails"]
                    
            if ID != "":
                embed = discord.Embed(title="Information about ID "+ID, color=0x00ff62)
                embed.set_thumbnail(url="https://img.icons8.com/color/344/list--v1.png")
                embed.add_field(name = "Submission Date:", value = Date, inline = False)
                embed.add_field(name = "URL:", value = URL, inline = False)
                embed.add_field(name = "IP Address:", value = IP, inline = False)
                if IP != "":
                    if ASNDESC != "None":
                        embed.add_field(name = "ASN:", value = ASN + " (" + ASNDESC + ")", inline = False)
                    else:
                        embed.add_field(name = "ASN:", value = ASN, inline = False)
                if TOLL != False:
                    embed.add_field(name = "Telephone Number:", value = PHONE + "(Toll Free)", inline = False)
                else:
                    embed.add_field(name = "Telephone Number:", value = PHONE, inline = False)
                if PHONECOUNTRY != "":
                    embed.add_field(name = "Country:", value = PHONECOUNTRY, inline = True)
                if PHONECARRIER != "":
                    embed.add_field(name = "Carrier:", value = PHONECARRIER, inline = True)
                if ABEMails != None:
                    embed.add_field(name = "Abuse Emails:", value = str(ABEMails), inline = True)
                embed.set_image(url="attachment://"+Hash+".png")
                await ctx.send(file=discord.File("./files/screenshots/"+Hash+".png", filename=Hash+".png"),embed=embed)
            else:
                await ctx.send("The id is not valid.")
            
    @tasks.loop(seconds = 5)
    async def SendMessage(this):
        for channel in this.channels:
            cc = this.client.get_channel(int(channel))
            print(channel)
            if cc != None:
                if len(this.PopUpManager.messages) > 0:
                    await cc.send(file=discord.File("./files/screenshots/"+this.PopUpManager.messages[0][0]+".png", filename=this.PopUpManager.messages[0][0]+".png"), embed=this.PopUpManager.messages[0][1])
        if len(this.PopUpManager.messages) > 0:
            this.PopUpManager.messages.pop(0)
                    
    def Execute(this):
        this.client.start(Utils.configBot(str("bot.token")))
        
    def init(this):
        this.SendMessage.start()
        loop = asyncio.get_event_loop()
        loop.create_task(this.client.start(Utils.configBot(str("bot.token"))))
        threading.Thread(target=loop.run_forever).start()
