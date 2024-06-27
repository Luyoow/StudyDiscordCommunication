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

# The number of characters
def get_lexicons(mes):
    mes = mes[mes.find('> ') + 2 : ]
    mes = re.sub(' +', ' ', mes)  
    #print(mes)
    num_word = len(mes)
    return num_word

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
    weekday = mes[1 : 11]
    #print(weekday)
    weeknum = datetime.datetime.strptime(weekday, "%Y-%m-%d").weekday()
    if (weeknum < 5):
        return True
    else:
        return False


def get_daytime(mes):
    time_= int(mes[12:14]) 
    #print(time_)
    if (time_ >= 14 and time_ <= 20): #(time_ >= 9 and time_ < 17):
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

def get_roles(mes, community): 
    member_list = {}
    member_list["angular"] = ["AlexOkrushko", "delasteve", "Foxandxss", "GeromeGrignon", "alx", "Armandotrue",
    "Brocco", "Chau", "duluca", "JoeEames", "MainaWycliffe", "martina", "shairez", "webdave",
    "4javier", "Frederik", "JamesHenry", "jbnizet", "mark.whitfeld", "Raziel", "Tim Deschryver"]
    member_list["redis"] = ["GuyRoyse", "SimonPrickett", "SteveLorello", "AviMoskowitz", "DanielTseitlin", "EstherSchindler",
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
    user_message = {}
    for i in range(index, -1, -1):  
        per_line = lines[i]
        daytime = per_line[1 : per_line.find("] ")]
        nowtime = datetime.datetime.strptime(daytime, "%Y-%m-%d %H:%M:%S")
        name = per_line[per_line.find(' <') + 2 : per_line.find('> ')]
        if (name not in user_message.keys()):
            user_message[name] = 0
        if (nowtime > start_time):
            user_message[name] += 1
            #print(name)
    quantile_4 = np.percentile(list(user_message.values()), 75)
    #print(quantile_4)
    if (user_message[targetname] > quantile_4):
        return True
    else:
        return False

def get_active(mes, community_name, line_tag):
    raw_file = open(community_name, "r", encoding= "utf-8")
    lines = raw_file.readlines()
    #print(name_mes)
    daytime = mes[1 : mes.find("] ")]
    #print(daytime)
    #print(lines[line_tag])
    # mes1 = mes[mes.find('> ') + 2 : ].strip()
    # mes2 = lines[line_tag][lines[line_tag].find('> ') + 2 : ].strip()
    # if (mes1 != mes2):
    #     print("match error:", community_name, line_tag)
    mes = lines[line_tag]
    name = mes[mes.find(' <') + 2 : mes.find('> ')].replace(" ", "")
    nowtime = datetime.datetime.strptime(daytime, "%Y-%m-%d %H:%M:%S")
    last30time = nowtime - datetime.timedelta(days = 30)
    res = get_active_sub_4quantile(name, lines, line_tag, last30time)
    # for index, per_line in enumerate(lines):
    #     if (name_mes in per_line and time_mes in per_line):
    #         #print(index)
    #         daytime = per_line[1 : per_line.find("] ")]
    #         #print(daytime)
    #         nowtime = datetime.datetime.strptime(daytime, "%Y-%m-%d %H:%M:%S")
    #         last30time = nowtime - datetime.timedelta(days = 30)
    #         #print(last30time)
    #         res = get_active_sub_4quantile(name, lines, index, last30time)
    #         #print(1)
    #         break
    #         #print(per_line)
    return res

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_dir = root + "/Data/DataRQ/RQ4/MergeFirst/"            # input：location 
res_dir = root + "/Data/DataRQ/RQ4/Feature_Resolved/"                # output：location 

if not os.path.exists(res_dir):    
    os.makedirs(res_dir) 

community_dirs = os.listdir(data_dir)
for per_community in community_dirs:
    #get csv of data
    data_df = pd.DataFrame({"DialogNum":[], "active developer":[], "roles":[], 
    "lexicons":[], "code snippets":[], "URLs":[], "weekday":[], "daytime":[], "readbility(CLI)":[],
    "user mentions":[], "sentiment":[]})   
    print(per_community)
    community_txt_dir = data_dir + per_community
    community_name = per_community.split(".")[0]
    community_dir = root + "/Data/DataAscii/" + community_name + ".txt"
    
    with open (community_txt_dir, "r", encoding= "GB2312") as f:
        first_utterance_flag = 1 
        lines = f.readlines()
        dialog_count = 1
        for index, line in enumerate(lines):
            #print(line)
            if (first_utterance_flag == 1):
                print(dialog_count)
                line_tag = int(line[ : line.find("[")]) - 1
                #print(line_tag)
                line = line[line.find("[") : ]
                #print(line)
                judge_space = line.replace(" ", "").replace(" ", "")  
                if (judge_space.find('>') == len(judge_space) - 2):
                    print("the dialog is empty start")
                    first_utterance_flag = 0
                    dialog_count += 1
                    continue
                res = []
                #print(line)
                res.append(dialog_count)
                res.append(get_active(line,community_dir,line_tag))
                res.append(get_roles(line, community_name))
                res.append(get_lexicons(line))
                res.append(get_codesnippets(line))
                res.append(get_URLs(line))
                res.append(get_weekday(line, community_dir))
                res.append(get_daytime(line))
                res.append(get_readability(line))
                res.append(get_mention(line))
                res.append(get_sentiment(line))
                #res.append(mes_label)
                data_df.loc[len(data_df.index)] = res
                first_utterance_flag = 0
                dialog_count += 1
                continue
            if (line == "-------" + str(dialog_count - 1) + '\n'):
                #rint(line)
                first_utterance_flag = 1 
            #break
        print("done")
    data_df.to_csv(res_dir + per_community + "rq4_res.csv")

    #break