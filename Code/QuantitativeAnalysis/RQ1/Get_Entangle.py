import pandas as pd
import os



root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir

res_root = root + "/Data/DataRQ/RQ1/Entangle/ALL.csv"         # output: lcation
data_dir = root + "/Data/DataRQ/RQ1/Entangle/AutoDailogLine/"
LineD_dir = root + "/Data/DataRQ/RQ1/Entangle/Line2Dialog/"
new_data_dir =  root + "/Data/DataRQ/RQ1/Entangle/DialogEntangleLine/"

com_dirs = os.listdir(data_dir)
for per_com in com_dirs:
    print(per_com)
    res = pd.DataFrame({"DialogNum": [], "EntangleLNum": [], "EntangleDNum":[]})
    com_dir = data_dir + per_com
    com_name = per_com.split(".")[0]
    new_csv_dir = new_data_dir + com_name + ".csv"
    lineD_data = pd.read_csv(LineD_dir + com_name + ".csv")

    with open(com_dir, "r") as f:
        D_Num = []
        line_res = []
        dialog_res = []
        dialog_cnt = 1
        Eline_cnt = 0
        dialog_set = set()
        start_flag = 1

        lines = f.readlines()
        for line in lines:
            if (line == "--------------------------------------------------------------------------------\n"):
                print(dialog_cnt)
                D_Num.append(dialog_cnt)
                line_res.append(Eline_cnt)
                dialog_res.append(len(dialog_set))
                dialog_cnt += 1
                Eline_cnt = 0
                start_flag = 1
                dialog_set = set()
                continue
            if (start_flag == 1):
                line_num_start = int(line[:line.find(" [")])
                start_flag = 0
            else:
                line_num_now = int(line[:line.find(" [")])
                steps = line_num_now - line_num_start
                if (steps <= 0): 
                    continue
                else:
                    line_num_start = line_num_now  

                Eline_cnt += steps - 1
                if (steps != 1):  
                    
                    for i in range(1, steps, 1):
                        Eline = line_num_start + i
                        
                        Edialog = lineD_data[lineD_data["LineNum"] == Eline]["DialogNum"]
                        
                        if (len(Edialog.values) == 0):
                            continue
                        else:
                            dialog_set.add(Edialog.values[0])
    res["DialogNum"] = D_Num
    res["EntangleLNum"] = line_res
    res["EntangleDNum"] = dialog_res
    res.to_csv(res_root)