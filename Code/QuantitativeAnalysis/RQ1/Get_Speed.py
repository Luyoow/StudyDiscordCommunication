#get the response time
import pandas as pd
import re
import textstat
#from textblob import TextBlob   #import error
import datetime 
import numpy as np
import os
import unicodedata

#get csv of data
root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_df = pd.DataFrame({"DialogNum":[], "dialog_speed":[]})   
data_dir = root + "/Data/DataRQ/RQ1/Response/"              # input：location dialogs with/without reponse
res_dir = root + "/Data/DataRQ/RQ1/Speed/"

if not os.path.exists(res_dir):    
    os.makedirs(res_dir) 

community_dirs = os.listdir(data_dir)
for per_community in community_dirs:
    if ("unrespond" in per_community):
        continue    #只需要有回答的对话
    
    # if ('Typescript' not in per_community):
    #     continue
    print(per_community)
    community_txt_dir = data_dir + per_community
    community_name = per_community.split(".")[0]
    
    dialog_count = 1
    data_df = pd.DataFrame({"DialogNum":[], "dialog_speed":[]})   
    with open (community_txt_dir, "r", encoding= "utf-8") as f:
        first_utterance_flag = 1  #标记当前这句话是不是一个对话的开始
        cal_dialog_time = 0 #标记这个对话是不是计算过时间了
        lines = f.readlines()
        for index, line in enumerate(lines):
            #print(line)
            if (first_utterance_flag == 1):
                print(dialog_count)
                #有可能开头的话是空的 因为都是ascii字符被删掉了
                judge_space = line.replace(" ", "").replace(" ", "")  #判断消息是不是为空
                if (judge_space.find('>') == len(judge_space) - 2):
                    print("the dialog is empty start")
                    first_utterance_flag = 0
                    dialog_count += 1
                    cal_dialog_time = 1
                    continue
                #判断名字是不是为'' 可能也是被字符处理导致的
                judge_name = line[line.find(' <') + 2 : line.find('> ')]  #名字为空舍弃
                if (judge_name == ""):
                    first_utterance_flag = 0
                    dialog_count += 1
                    cal_dialog_time = 1
                    print("the name is none")
                    continue
                first_name = line[line.find(' <') + 2 : line.find('> ')]
                first_time = datetime.datetime.strptime(line[line.find('[') + 1 : line.find('] ')], "%Y-%m-%d %H:%M:%S")
                #print(first_time)
                res = []
                res.append(dialog_count)
                first_utterance_flag = 0
                dialog_count += 1
                continue
            if (line == "--------------------------------------------------------------------------------\n"):
            #if (line == "--------------------------------------------------------------------------------------------------\n"):
                first_utterance_flag = 1 #说明下一句开始是对话第一句
                cal_dialog_time = 0
            #data_df.to_csv("D://zju//1-paper//1_newdataset//1-Discord_dataset//Rq1Analysis//rq1_res.csv")
            #break
            else:
                #说明是一个对话中非第一句的其他句
                if (cal_dialog_time == 0):
                    next_name = line[line.find(' <') + 2 : line.find('> ')]
                    if (next_name != first_name):
                        next_time = datetime.datetime.strptime(line[line.find('[') + 1 : line.find('] ')], "%Y-%m-%d %H:%M:%S")
                        #print(next_time)
                        cal_dialog_time = 1  #该对话计算过时间
                        dialog_speed = next_time - first_time
                        res.append(dialog_speed.total_seconds())
                        #print(res)
                        data_df.loc[len(data_df.index)] = res
                       # res = []

        print("done")
        data_df.to_csv(res_dir + community_name + ".speed.csv")

    #break