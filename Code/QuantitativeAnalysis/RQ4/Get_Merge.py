import pandas as pd
import os

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_dir =  root + "/Data/DataAscii/Manual/"                   # input：location 
res_dir = root + "/Data/DataRQ/RQ4/MergeFirst/"                # output：location 

if not os.path.exists(res_dir):    
    os.makedirs(res_dir) 

community_dirs = os.listdir(data_dir)
for per_community in community_dirs:
    print(per_community)
    community_txt_dir = data_dir + per_community
    community_name = per_community.split(".")[0]
    new_file_dir = res_dir + community_name + ".txt"
    new_file = open(new_file_dir, "w")
    with open (community_txt_dir, "r", encoding= "GB2312") as f:
        first_utterance_flag = 1  
        lines = f.readlines()
        dialog_count = 1
        continue_tag = 1
        for index, line in enumerate(lines):
            if (first_utterance_flag == 1):
                print(dialog_count)
                start_line = line
                print(start_line)
                start_name = line[line.find("<") + 1 : line.find(">")]
                first_utterance_flag = 0
                dialog_count += 1
                continue
            now_name = line[line.find("<") + 1 : line.find(">")]
            if (now_name == start_name):
                if (continue_tag == 1):
                    start_line = start_line.strip() + "." + line[line.find("> ") + 2 :]  
                    continue
            else: 
                if (continue_tag == 1):
                    new_file.write(start_line)
                    continue_tag = 0
            new_file.write(line)
            if (line == "-------" + str(dialog_count - 1) + '\n'):
                #rint(line)
                first_utterance_flag = 1 
                continue_tag = 1
        
        print("done")
        #break