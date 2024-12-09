import anticord
import anticord.AntiCordGateway
import anticord.AntiCordPlainHttpRequest
from colorama import Fore
import threading
import random

def initialize_bot(TOKEN,INTENTS):
    BOT = anticord.AntiCordPlainHttpRequest.BOT(TOKEN)
    print("Initialized bot with token  " + Fore.BLUE + TOKEN + Fore.WHITE)
    GATEWAYOBJ = anticord.AntiCordGateway.GatewayWebsocket.CreateGatewayObj(TOKEN)
    GATEWAYOBJ.CreateConnection()
    print("Created a gateway connection")
    print("Sending intents " + Fore.BLUE + str(INTENTS) + Fore.WHITE + " to the gateway connection")

    # It will give an error if token/bot is invalid

    try:
        response = GATEWAYOBJ.SendIntents(INTENTS)
    except:
        print(Fore.RED + "Error while sending intents to gateway!" + Fore.WHITE)
        print(Fore.RED + "Token may be invalid , double check the token you use" + Fore.WHITE)
        print(Fore.RED + "Make sure you also enable all the privleged gateway intents" + Fore.WHITE)
        input("Press enter to quit")
        quit(1)

    print(Fore.GREEN + "Sent intents to gateway!" + Fore.WHITE)

    # Just in case it somehow gets to this stage

    if response == 0:
        print(Fore.GREEN + "Recived a ready opcode from the gateway!" + Fore.WHITE)
    elif response == 1:
        print(Fore.RED + "Error while sending intents to gateway!" + Fore.WHITE)
        print(Fore.RED + "Token may be invalid , double check the token you use" + Fore.WHITE)
        print(Fore.RED + "Make sure you also enable all the privleged gateway intents" + Fore.WHITE)
        input("Press enter to quit")
        quit(1)
    
    return BOT,GATEWAYOBJ

def say_command(BOT,text_arg):
        try:
            channel_id = text_arg[1]
            channel = BOT.GetChannelByID(channel_id)
            text_arg.pop(0)
            text_arg.pop(0)
            response = channel.SendMessage(' '.join(text_arg))
            try:
                content = response["content"]
                print(Fore.GREEN + "Said " + Fore.BLUE + content + Fore.GREEN + " in channel " + Fore.BLUE + channel.GetChannelAttribute("name") + Fore.WHITE)
            except:
                print(Fore.RED + 'Error: ' + str(response) + Fore.WHITE)
        except:
            print(Fore.RED + "Invalid use of command say , please use: " + Fore.WHITE)
            print(Fore.LIGHTYELLOW_EX + "say " + Fore.LIGHTBLACK_EX + "<channelid> <content>" + Fore.WHITE)

def list_command(BOT):
        n = 0
        print(Fore.GREEN + "Listing all the servers the bot is in: " + Fore.WHITE)
        for i in BOT.GetBotGuilds():
            print(Fore.LIGHTBLACK_EX + i.GetGuildAttribute("name") + " - id is " + i.guildid + Fore.WHITE)
            n = n + 1
        print(Fore.GREEN + "Bot is in " + Fore.BLUE + str(n) + Fore.GREEN + " servers!" + Fore.WHITE)

def interpret_afnk_oneline(line,values,title,i):
                spec = []
                if line == []:
                    pass
                    return values,title,0
                elif line[0] == "#":
                    line.pop(0)
                    title = ' '.join(line)
                    return values,title,0
                elif line[0] == " " or line[0] == "":
                    pass
                    return values,title,0
                elif line[0] == "[":
                    if line[len(line) - 1] == "]":
                        if line[2] == ":":
                            if line[3][:2] == "|&": 
                                if (line[3][2:]) == "True":
                                    values[line[1]] = True
                                    return values,title,0
                                elif (line[3][2:]) == "False":
                                    values[line[1]] = False
                                    return values,title,0
                                else:
                                    print(Fore.RED + "Error at line " + str(i) + " , invalid bool type" + Fore.WHITE)
                                    return values,title,1
                            else:
                                line.pop(len(line) - 1)
                                values[line[1]] = ' '.join(line[3:])
                                return values,title,0
                        elif line[2] == "->":
                            spec = line[1]
                            line.pop(1)
                            line.pop(1)
                            if line[2] == ":":
                                if line[3][:2] == "|&": 
                                    if (line[3][2:]) == "True":
                                        values[spec][line[1]] = True
                                        return values,title,0
                                    elif (line[3][2:]) == "False":
                                        values[spec][line[1]] = False
                                        return values,title,0
                                    else:
                                        print(Fore.RED + "Error at line " + str(i) + " , invalid bool type" + Fore.WHITE)
                                        return values,title,1
                                else:
                                    line.pop(len(line) - 1)
                                    values[spec][line[1]] = ' '.join(line[3:])
                        
                                    return values,title,0
                            else:
                                print(Fore.RED + "Error at line " + str(i) + " , invalid operation " + Fore.WHITE)
                                return values,title,1 
                        else:
                            print(Fore.RED + "Error at line " + str(i) + " , invalid operation " + Fore.WHITE)
                            return values,title,1 
                    else:
                        print(Fore.RED + "Error at line " + str(i) + " , expected ']'" + Fore.WHITE)
                        return values,title,1

                elif line[0] == "//":
                    pass
                    return values,title,0
                else:
                    print(Fore.RED + "Error at line " + str(i) + Fore.WHITE)
                    return values,title,1

def check_command(text_arg,values,title):
        try:
            with open(text_arg[1],"r") as f:    
                text_lines = f.readlines()
                i = 0
                errors = 0
            
            if text_arg[1].endswith(".afnk"):
                for line in text_lines:
                    i = i + 1
                    line = line.strip()
                    line = line.split()
                    values,title,error = interpret_afnk_oneline(line,values,title,i)
                    if error == 1:
                        errors = errors + 1
                
                if errors == 0:
                    print(Fore.GREEN + "Nuke template interpreted without any errors!" + Fore.WHITE)
                    print(Fore.GREEN + "Scince unknown values are not detected as errors" + Fore.WHITE)
                    print(Fore.GREEN + "We recomend you to check if the value array mathces what you want:" + Fore.WHITE)
                    print(values)

                else:
                    print(Fore.RED + "Nuke template interpreted with " + Fore.LIGHTRED_EX + str(errors) + Fore.RED + " errors!" + Fore.WHITE)
            else:
                print(Fore.RED + "File must end with .afnk!" + Fore.WHITE)
        except FileNotFoundError:
            print(Fore.RED + "File not found!" + Fore.WHITE)
        except:
            print(Fore.RED + "Invalid use of command check , please use: " + Fore.WHITE)
            print(Fore.LIGHTYELLOW_EX + "check " + Fore.LIGHTBLACK_EX + " <file path>" )

def nuke_command(BOT,text_arg,values):
        try:
            title = "Untitled template"
            server_id = text_arg[1]
            template_file = text_arg[2]
            guild = BOT.GetGuildByID(text_arg[1])

            YN=input("Are you sure you wanna nuke " + Fore.BLUE + guild.GetGuildAttribute("name") + Fore.WHITE + "? " + Fore.GREEN + "y" + Fore.WHITE + "/" + Fore.RED + "n " + Fore.WHITE)
            if YN.capitalize() == "N":
                print(Fore.RED + "Aborted nuke" + Fore.WHITE)
            elif YN.capitalize() == "Y":
                print("Nuking " + Fore.BLUE + guild.GetGuildAttribute("name") + Fore.WHITE)
                try:
                    with open(text_arg[2],"r") as f:    
                        text_lines = f.readlines()
                        i = 0
                        errors = 0
                    
                    if text_arg[2].endswith(".afnk"):
                        for line in text_lines:
                            i = i + 1
                            line = line.strip()
                            line = line.split()
                            values,title,error = interpret_afnk_oneline(line,values,title,i)
                            if error == 1:
                                errors = errors + 1
                        
                        if errors == 0:
                            print(Fore.GREEN + "Nuke template interpreted without any errors!" + Fore.WHITE)
                            print("Loading template "  + Fore.BLUE + title + Fore.WHITE)
                            spam_message = values["message-nuke"]["message"]
                            channel_name = values["channel-nuke"]["name"]
                            channel_rename_name = values["channel-rename"]["name"]
                            print(Fore.GREEN + "Loaded template!" + Fore.WHITE)
                            print(Fore.GREEN + "Nuking server!" + Fore.WHITE)

                            if values["guild-rename"]["enabled"]:
                                print("Renaming guild...")
                                response = guild.ChangeGuildAttribute({"name":values["guild-rename"]["name"]})
                                try:
                                    e = response["name"]
                                    print(Fore.GREEN + "Renamed guild to " + Fore.BLUE + guild.GetGuildAttribute("name") + Fore.WHITE)
                                except:
                                    print(Fore.RED + "Cloudn't rename guild" + Fore.WHITE)
                                

                            if values["channel-rename"]["enabled"]:
                                print("Renaming channels...")
                                for i in guild.GetGuildChannels():
                                    old_name = i.GetChannelAttribute("name")
                                    response = i.ChangeGuildChannelAttribute({"name":channel_rename_name})
                                    try:
                                        e = response["name"]
                                        print(Fore.GREEN + "Renamed channel " + Fore.BLUE + old_name + Fore.WHITE)
                                    except:
                                        print(Fore.RED + "Cloudn't rename channel " + i.GetChannelAttribute("name") + Fore.WHITE)
                            
                            def spam_nuke(channel):
                                print("Spamming messages in channel...")
                                while True:
                                    response = channel.SendMessage(values["message-nuke"]["message"])
                                    try:
                                        e = response['content']
                                        print(Fore.GREEN + "Sent message!" + Fore.WHITE)
                                    except:
                                        print(Fore.RED + "Cloudn't send message :" + str(response) + Fore.WHITE)
                            
                            def ban_all():
                                print("Banning users...")
                                for user in guild.GetGuildMembers(limit=1000):
                                    if values["ban-nuke"]["delete-messages"]:
                                        if values["ban-nuke"]["tell-user-about-ban"]:
                                            try:
                                                dm = user.CreateUserDm()
                                                dm.SendMessage(values["ban-nuke"]["ban-message"])
                                            except:
                                                pass
                                        try:
                                            response = guild.BanUser(user,604800)
                                            print(Fore.RED + "Cloudn't ban " + Fore.BLUE + user.GetUserAttribute("username") + Fore.WHITE)
                                        except:
                                            print(Fore.GREEN + "Bannned " + Fore.BLUE + user.GetUserAttribute("username") + Fore.WHITE)
                                    else:
                                        try:
                                            response = guild.BanUser(user)
                                            print(Fore.RED + "Cloudn't ban " + Fore.BLUE + user.GetUserAttribute("username") + Fore.WHITE)
                                        except:
                                            print(Fore.GREEN + "User was probably bannned " + Fore.BLUE + user.GetUserAttribute("username") + Fore.WHITE)
                                        

                            def channel_nuke():
                                if values["channel-nuke"]["enabled"]:
                                    print("Making channels...")
                                    if values["ban-nuke"]["enabled"]:
                                        threading.Thread(target=ban_all).start()
                                    
                                    while True:
                                        try:
                                            channel = guild.CreateGuildChannelText(values["channel-nuke"]["name"])
                                            print(Fore.GREEN + "Made channel " + Fore.BLUE + e + Fore.WHITE)
                                            if values["message-nuke"]["message"]:
                                                threading.Thread(target=spam_nuke,args=(channel,)).start()
                                        except:
                                            print(Fore.Red + "Cannot Make channel ")
                                                
                            channel_nuke()
        
                        else:
                            print(Fore.RED + "Nuke template interpreted with " + Fore.LIGHTRED_EX + str(errors) + Fore.RED + " errors!" + Fore.WHITE)
                            print(Fore.RED + "Aborted nuke" + Fore.WHITE)
                    else:
                        print(Fore.RED + "File must end with .afnk!" + Fore.WHITE)
                        print(Fore.RED + "Aborted nuke" + Fore.WHITE)
                except FileNotFoundError:
                    print(Fore.RED + "File not found!" + Fore.WHITE)
                    print(Fore.RED + "Aborted nuke" + Fore.WHITE)
            else:
                print(Fore.RED + "Aborted nuke" + Fore.WHITE)
        except:
            print(Fore.RED + "Invalid use of command nuke , please use: " + Fore.WHITE)
            print(Fore.LIGHTYELLOW_EX + "nuke " + Fore.LIGHTBLACK_EX + "<serverid> <afnk template path>" + Fore.WHITE)

def membercount_command(BOT,text_arg):
        try:
            guild = BOT.GetGuildByID(text_arg[1])
            member_list = []
            for member in guild.GetGuildMembers(1000):
                member_list.append(member)
                member_count = len(member_list)
                if member_count == 1000:
                    member_count = "1000+"
            print(Fore.BLUE + guild.GetGuildAttribute("name") + Fore.LIGHTBLACK_EX + " has " + Fore.BLUE + str(member_count) + Fore.LIGHTBLACK_EX + " members!" + Fore.WHITE)
        except:
            print(Fore.RED + "Invalid use of command membercount , please use: " + Fore.WHITE)
            print(Fore.LIGHTYELLOW_EX + "membercount " + Fore.LIGHTBLACK_EX + "<serverid>" + Fore.WHITE)

def invite_command(BOT,text_arg):
    try:
        invites = []
        guild = BOT.GetGuildByID(text_arg[1])
        print("Generating invite...")
        for channel in guild.GetGuildChannels():
            try:
                response = channel.CreateInivte()
                invites.append(response["code"])
            except:
                pass
        
        invite = random.choice(invites)

        print(Fore.GREEN + "Generated invite code for " + Fore.BLUE + guild.GetGuildAttribute("name") + Fore.WHITE + " : " + Fore.BLUE + invite + Fore.WHITE)
    except:
        print(Fore.RED + "Invalid use of command membercount , please use: " + Fore.WHITE)
        print(Fore.LIGHTYELLOW_EX + "invite " + Fore.LIGHTBLACK_EX + "<serverid>" + Fore.WHITE)