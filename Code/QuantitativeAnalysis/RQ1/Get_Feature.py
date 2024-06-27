#get the features of all dialogs
import pandas as pd
import re
import textstat
from textblob import TextBlob
import datetime 
import numpy as np
import os
import unicodedata

#example
#[16:53] <cab11150904> Hey all.  Seriously considering starting to learn Android Dev. 
#the input is message like this

#The number of characters in utterance content
def get_lexicons(mes):
    mes = mes[mes.find('> ') + 2 : ]
    mes = re.sub(' +', ' ', mes)     # multiple blank into one
    #print(mes)
    num_word = len(mes)
    return num_word


#find code snippets
def get_codesnippets(mes):
    mes = mes[mes.find('> ') + 2 : ]
    mes = mes.replace("\"\"\"", "```").replace("\'\'\'", "```")
    res = re.findall('```', mes)
    if (len(res) != 0):
        return True
    else:
        return False

def get_URLs(mes):
    mes = mes[mes.find('> ') + 2 : ]
    str = "(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"
    res = re.findall(str, mes)
    if (len(res) != 0):
        return True
    else:
        return False

def get_weekday(mes, community_name):
    #community_name -> original date
    mes = mes[mes.find(' <') + 2 : ].strip()  #Add message -> match utterance
    raw_file = open(community_name, "r",encoding= "utf-8")
    for per_line in raw_file.readlines():
        if mes in per_line:
            weekday = per_line[1 : 11]
            break
    #print(weekday)
    weeknum = datetime.datetime.strptime(weekday, "%Y-%m-%d").weekday()
    if (weeknum < 5):
        return True
    else:
        return False

def get_daytime(mes):
    time_= int(mes[1:3])
    #print(time_)
    if (time_ >= 14 and time_ < 20):    #active time
        return True
    else:
        return False

def get_readability(mes):
    mes = mes[mes.find('> ') + 2 : ]
    CLI = textstat.coleman_liau_index(mes)
    return CLI

def get_mention(mes):
    mes = mes[mes.find('> ') + 2 : ]
    res = re.findall('@', mes)
    if (len(res) != 0):
        return True
    else:
        return False
        
def get_sentiment(mes):
    blob = TextBlob(mes)
    return blob.sentiment.polarity

def get_roles(mes, community):  #member list -> collection  #problem macth id/ name 
    member_list = {}
    member_list["angular"] = ["AlexOkrushko", "delasteve", "Foxandxss", "GeromeGrignon", "alx", "Armandotrue",
    "Brocco", "Chau", "duluca", "JoeEames", "MainaWycliffe", "martina", "shairez", "webdave",
    "4javier", "Frederik", "JamesHenry", "jbnizet", "mark.whitfeld", "Raziel", "Tim Deschryver"]
    member_list["Redis"] = ["GuyRoyse", "SimonPrickett", "SteveLorello", "AviMoskowitz", "DanielTseitlin", "EstherSchindler",
    "FrançoisCerbelle", "JohnSachs", "WillJohnston", "MateoDrk", "Mephalich", "DaShaun"]
    member_list["typescript"] = ["orta", "Micah-\"don\'tuseany\"-Zoltu", "T6", "Yanis", "!Winner", "acliclasCooker",
     "AfterLife", "alanaudi", "andjsrk", "Andreas~", "aravan", "Ascor", "astronaut", "Bablu", "baconsmoothie2", "bartass",
     "BIGFATMonad", "BlackKnight", "boltz", "bradmk", "burtek🇵🇱", "cake", "copleykj", "D-Reaper", "D3V_G;T", "d_0nkey", "DarkSoul",
     "DateP", "devdgehog", "DICE", "Doctor", "DogPawHat", "donthatedontkill", "EisKaffee", "EmanuelLeão", "Eric.Le", "ExoMemphiz (Chris)",
     "FiretronP75", "Frosk", "Futuristick", "GKjojogo", "hell", "HelloAnchorage", "horacio", "iconique", "Irveloper", "J0hn", "jacobwgillespie",
     "Jaquan", "jeliasson", "jhonghee", "JMN", "Kai", "Kar", "Kei", "Kiran", "krzymo", "Ktime", "LittleStar", "Lucas", "Mbani", "n_n", "Nerd", "Nero"
     "ngDeveloper", "NightSky", "Nudjialz", "OceanLeo", "okanisis", "oneilllee", "paarth", "plaidman", "ProCul", "puresoul", "Qru", "Quadristan", "Qudusayo",
     "ReinHardtBerkeley", "rezonant", "Rinzai", "robertotomás", "Rock3r", "SaudruH", "shivamm", "shivampurohit", "shockwave", "shubhamku044", "T-Rex", "tejprady",
     "TheWinnerTeam", "TheCodedProf", "themogul", "thomas7sea", "TsDraco", "tzaycam", "Volks", "WhiteKnife", "wholespace", "WildPanda", "ケンゾウ", "ꜱᴛᴀᴄɪᴀ."]
    member_list["vscode"] = ["Nikos-dmonlyforserverissue", "Olivia", "Mylon", ".ʟᴜᴄɪᴀ!♡", "AndrewFrozen", "CEntertain", "ZBAGI", "moonguy", "RustyKeel(ACAB)", "Count_MHM",
     "DanoFPV", "Togira", "◢◤mICON", "tommarek", "BenForge", "Dhruv", "GinoMan2440", "Kubixgames", "KulaGGin", "Lycoris", "M3tex", "Pierce", "TứnCôĐơn"]
    member_list["docker"] = ["Pirion", "xy", "khalid", "cssoftware", "Heatman","Lildirt", "!Timon"]
    member_list["tensorflow"] = ["Huzuni", "Nikos", "⎛⎝tehZevo⎠⎞", "NGL|Nikos", "Grofit", "Rojepi", "swissbeats93", "TexHik", "GantMan"]
    member_list["android"] = ["borninbronx", "Heron", "IPat", "sLAUGHTER", "TorchDragon", "Wearenottechsupport", "s73v3r"]
    name = mes[mes.find(' <') + 2 : mes.find('> ')]
    #print(name)
    if name in member_list[community]:
        return True
    else:
        return False

def get_active_sub_4quantile(targetname, lines, index, start_time):
    # the last 30 days -> the number of utterances posted by each practitioners
    user_message = {}
    for i in range(index, -1, -1):  #count from the current utterance
        per_line = lines[i]
        daytime = per_line[1 : per_line.find("] ")]
        nowtime = datetime.datetime.strptime(daytime, "%Y-%m-%d %H:%M:%S")
        name = per_line[per_line.find(' <') + 2 : per_line.find('> ')]
        if (name not in user_message.keys()):
            user_message[name] = 0
        if (nowtime > start_time):
            user_message[name] += 1
            #print(name)
    # calculate quartiles
    #print(list(user_message.values()))
    quantile_4 = np.percentile(list(user_message.values()), 75)
    #print(quantile_4)
    if (user_message[targetname] > quantile_4):
        return True
    else:
        return False

def get_active(mes, community_name):
    name = mes[mes.find(' <') + 2 : mes.find('> ')]
    time_mes = mes[1:6]
    #print(name)
    name_mes = mes[mes.find(' <') + 2 : ].strip() #Remove extra line breaks, you need to add the name to match because the message will be duplicated.
    #print(name)
    raw_file = open(community_name, "r", encoding= "utf-8")
    lines = raw_file.readlines()
    #print(name_mes)
    for index, per_line in enumerate(lines):
        if (name_mes in per_line and time_mes in per_line):
            #print(index)
            daytime = per_line[1 : per_line.find("] ")]
            #print(daytime)
            nowtime = datetime.datetime.strptime(daytime, "%Y-%m-%d %H:%M:%S")
            last30time = nowtime - datetime.timedelta(days = 30)
            #print(last30time)
            res = get_active_sub_4quantile(name, lines, index, last30time)
            #print(1)
            break
        #print(per_line)
    return res


# test = "[17:00] <cab11150904> I assume more experienced people hang out here too."
# com_dir = "D://zju//1-paper//1_newdataset//1-Discord_dataset//Dataset_1//Android//android.txt"
# print(get_active(test, com_dir))

#get csv of data
# data_df = pd.DataFrame({"DialogNum":[], "active developer":[], "newcomer":[], "roles":[], 
# "lexicons":[], "code snippets":[], "URLs":[], "weekday":[], "daytime":[], "readbility(CLI)":[],
# "user mentions":[], "sentiment":[], "respond":[]})   

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_dir = root + "/Data/DataRQ/RQ1/Response/"            # input：location 
res_dir = root + "/Data/DataRQ/RQ1/Feature/"     # output：location 

if not os.path.exists(res_dir):    
    os.makedirs(res_dir) 

community_dirs = os.listdir(data_dir)
for per_community in community_dirs:
    data_df = pd.DataFrame({"DialogNum":[], "active developer":[], "roles":[], 
    "lexicons":[], "code snippets":[], "URLs":[], "weekday":[], "daytime":[], "readbility(CLI)":[],
    "user mentions":[], "sentiment":[], "respond":[]}) 
    community_txt_dir = data_dir + per_community
    community_name = per_community.split(".")[0]
    community_dir = root + "/Data/DataAscii/" + community_name + ".txt"   

    mes_label = 0   # Marking messages as responded or unresponded
    print(per_community)
    if ("unrespond" in per_community):
        mes_label = -1    # responded
    else:
        mes_label = 1     # unresponded
    with open (community_txt_dir, "r", encoding= "utf-8") as f:
        first_utterance_flag = 1   # Mark whether the current sentence is a dialogue starter
        lines = f.readlines()
        dialog_count = 1
        for index, line in enumerate(lines):
            #print(line)
            if (first_utterance_flag == 1):
                print(dialog_count)
                # It's possible that the beginning of the sentence is empty because it's all ascii characters that have been deleted.
                judge_space = line.replace(" ", "").replace(" ", "")  # Determine if the message is empty
                if (judge_space.find('>') == len(judge_space) - 2):
                    print("the dialog is empty start")
                    first_utterance_flag = 0
                    dialog_count += 1
                    continue
                # Determining whether a name is ' ' may also be caused by character handling
                judge_name = line[line.find(' <') + 2 : line.find('> ')]  # Discard if name is null
                if (judge_name == ""):
                    first_utterance_flag = 0
                    dialog_count += 1
                    print("the name is none")
                    continue
                res = []
                res.append(dialog_count)
                res.append(get_active(line,community_dir))
                res.append(get_roles(line, community_name))
                res.append(get_lexicons(line))
                res.append(get_codesnippets(line))
                res.append(get_URLs(line))
                res.append(get_weekday(line, community_dir))
                res.append(get_daytime(line))
                res.append(get_readability(line))
                res.append(get_mention(line))
                res.append(get_sentiment(line))
                res.append(mes_label)
                data_df.loc[len(data_df.index)] = res
                first_utterance_flag = 0
                dialog_count += 1
                continue
            if (line == "--------------------------------------------------------------------------------\n"):
                first_utterance_flag = 1  # the next utterance is the start of a new dialog
        print("done")
        data_df.to_csv(res_dir + per_community + ".feature.csv" )
            #break

#print("done")
#data_df.to_csv("/data/luyaowang/mydata/Discord/RQ1/rq1_res.csv")

    #break