#get the response time
import pandas as pd
import re
import textstat
#from textblob import TextBlob   #import error
import datetime 
import numpy as np
import os
import unicodedata

# need to devide dialogs into : responded / unresponded

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_dir = root + "/Data/DataDialog/Auto"                      # input：location 
new_file_dir = root + "/Data/DataRQ/RQ1/Response/"             # output: lcation

if not os.path.exists(new_file_dir):    
    os.makedirs(new_file_dir) 

txt_dirs = os.listdir(data_dir)
for per_txt in txt_dirs:
    respond_file_dir = new_file_dir + per_txt + "respond.txt"
    unrespond_file_dir = new_file_dir + per_txt + "unrespond.txt"
    res_file = open(respond_file_dir, "w")
    unres_file = open(unrespond_file_dir, "w")
    per_txt_dir = data_dir + "/" + per_txt
    with open(per_txt_dir, "r") as txt_file:   #find the utterances which get no response
        lines = txt_file.readlines()
        dialog_par = set()
        last_line = 0
        for index, per_line in enumerate(lines):
            if (per_line == "--------------------------------------------------------------------------------\n"):
                #print(lines[last_line:index])
                if (len(dialog_par) == 1):
                    for i in range(last_line, index + 1):
                        unres_file.write(lines[i])
                        #print(lines[i][:-1])
                    #print(lines[index])
                else:
                    for i in range(last_line, index + 1):
                        res_file.write(lines[i])

                dialog_par = set()
                last_line = index + 1 
                #break
            else:
                #print(per_line.find("<"))
                per_name = per_line[per_line.find('<') + 1 : per_line.find('>')]
                dialog_par.add(per_name)
                #print(per_name)
            #break
    #break
