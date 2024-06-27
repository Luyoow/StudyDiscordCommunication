import pandas as pd
import os
import datetime 


root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
dialog_dir = root + "/Data/DataDialog/Manual/"              # input：location 
res_dir = root + "/Data/DataRQ/RQ4/Length/"                 # output: lcation

if not os.path.exists(res_dir):    
    os.makedirs(res_dir) 

coms = os.listdir(dialog_dir)
for com in coms:
    res = pd.DataFrame()
    res_time = []
    com_dir = dialog_dir + com
    print(com_dir)
    with open (com_dir, "r", encoding='utf-8') as com_dialog:
        lines = com_dialog.readlines()
        last_num = -1
        start_time = 0
        now_time = 0
        for line in lines:
            if (line[:7] == "-------"):
                # print(start_time)
                # print(now_time)
                dialog_length = now_time - start_time
                res_time.append(dialog_length.seconds)
                last_num = -1
                continue
            if (last_num == -1):
                start_time = line[line.find("[") + 1 : line.find("]")]  # get the time
                start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                #print(start_time)
                now_time = start_time
                last_num = 1
                #print(last_num)
                continue
            else:
                now_time = line[line.find("[") + 1 : line.find("]")]
                #print(now_time)
                now_time =  datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")

        #res_time.append(flag)
        res["Duration"] = res_time
        res.to_csv(res_dir + com +".csv")
   # break



