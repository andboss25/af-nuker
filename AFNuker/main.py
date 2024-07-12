
# IMPORTS

import functions
import anticord
import anticord.AntiCordGateway
import anticord.AntiCordPlainHttpRequest
from colorama import Fore

# INITIALIZE VARIABLES

title = "Untitled template"
values = {"guild-rename":{"enabled":True,"name":"Nuked by antifurry"},"channel-nuke":{"enabled":True,"name":"nuked-by-antifurry"},"channel-rename":{"enabled":True,"name":"nuked-by-antifurry"},"message-nuke":{"enabled":True,"message":"Nuked by antifurry!"},"ban-nuke":{"enabled":True,"delete-messages":True,"tell-user-about-ban":True,"ban-message":"Server was nuked by antifurry"}}

with open("token.txt","r") as f:
    TOKEN = f.read()
    print("Using token " + Fore.BLUE + TOKEN + Fore.WHITE + " from token.txt")

INTENTS = 513

# INITIALIZE BOT AND GATEWAY

BOT,GATEWAYOBJ = functions.initialize_bot(TOKEN,INTENTS)

# DISPLAY AF-NUKER LOGO

print(Fore.BLUE+"""
 █████╗ ███████╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
███████║█████╗█████╗██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
██╔══██║██╔══╝╚════╝██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
██║  ██║██║         ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝         ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                               """ + Fore.WHITE)
print(Fore.BLUE + "\nMade by an antifurry" +Fore.WHITE)
print(Fore.BLUE + "Built using anticord" +Fore.WHITE)
print(Fore.BLUE + "Type help for a list of commands\n" +Fore.WHITE)

# MAIN COMMAND LINE LOOP

while True:
    text_arg = input("bot >> ")
    text_arg = text_arg.split()
    if text_arg == []:
        pass
    elif text_arg[0].lower() == "say":
        functions.say_command(BOT,text_arg)
    elif text_arg[0].lower() == "list":
        functions.list_command(BOT)
    elif text_arg[0].lower() == "check":
        functions.check_command(text_arg,values,title)
    elif text_arg[0].lower() == "nuke":
        functions.nuke_command(BOT,text_arg,values)
    elif text_arg[0].lower() == "membercount":
        functions.membercount_command(BOT,text_arg)
    elif text_arg[0].lower() == "invite":
        functions.invite_command(BOT,text_arg)
    elif text_arg[0].lower() == "help":
        print(Fore.LIGHTYELLOW_EX + "say " + Fore.LIGHTBLACK_EX + "<channelid> <content>" + Fore.WHITE + " - Say something in a channel")
        print(Fore.LIGHTYELLOW_EX + "list" + Fore.WHITE + " - List all servers the bot is in and their id")
        print(Fore.LIGHTYELLOW_EX + "check " + Fore.LIGHTBLACK_EX + "<file path>" + Fore.WHITE + " - Checks if a afnk template has errors or not")
        print(Fore.LIGHTYELLOW_EX + "nuke" + Fore.LIGHTBLACK_EX + " <serverid> <afnk template path>" + Fore.WHITE + " - Nuke's the server with the afnk template")
        print(Fore.LIGHTYELLOW_EX + "membercount " + Fore.LIGHTBLACK_EX + "<serverid>" + Fore.WHITE + " - Will show you the membercount of the server up to 1000 members")
        print(Fore.LIGHTYELLOW_EX + "invite " + Fore.LIGHTBLACK_EX + "<serverid>" + Fore.WHITE + " - Makes a invite for the server from a random channel")
    else:
        print(Fore.RED + "Invalid command! do help for a list of commands!" + Fore.WHITE)


