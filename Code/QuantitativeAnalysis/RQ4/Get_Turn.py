import pandas as pd
import os
import datetime 

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
dialog_dir = root + "/Data/DataDialog/Manual/"             # input：location 
res_dir = root + "/Data/DataRQ/RQ4/Turn/"                  # output: lcation

if not os.path.exists(res_dir):    
    os.makedirs(res_dir) 

coms = os.listdir(dialog_dir)
for com in coms:
    res = pd.DataFrame()
    res_time = []
    com_dir = dialog_dir + com
    with open (com_dir, "r", encoding="utf-8") as com_dialog:
        lines = com_dialog.readlines()
        start_line = lines[0]
        end_line = ""
        asker = start_line[start_line.find("<") + 1 : start_line.find("> ")]     # find the asker
        dialog_turn = 0
        last_name = asker
        for line in lines:
            if (end_line[:7] == "-------"):     # the satrt of a new dialog
                start_line = line
                asker = start_line[start_line.find("<") + 1 : start_line.find("> ")]       # find the asker
                last_name = asker
                res_time.append(dialog_turn)
                dialog_turn = 0
            if (line[:7] != "-------"):
                now_name = line[line.find("<") + 1 : line.find("> ")]      # the speaker of current utterance
                if (now_name != asker):
                    now_name = "res"       #the rest respondents are seen as one respondent
                if (now_name != last_name):
                    dialog_turn += 1
                    last_name = now_name
            end_line = line    #the utterance before the current utterance
        res_time.append(dialog_turn)
        res["Turns"] = res_time
        res.to_csv(res_dir + com +"truns.csv")
    #break



