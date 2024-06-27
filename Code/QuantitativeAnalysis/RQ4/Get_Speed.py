#Remove dialogs with negative response times while setting unresponsive dialogues to the maximum value and log the response times Max-Min on features
import os
import pandas as pd
import numpy as np

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
csv_dir = root + "/Data/DataRQ/RQ4/Feature_Responded/all.csv"                 # input：location 
res_dir = root + "/Data/DataRQ/RQ4/Feature_Responded/DealData.csv"            # output：location 

csv_data= pd.read_csv(csv_dir)

#print(pd.value_counts(csv_data["dialog_speed"]))
max_time = csv_data["dialog_speed"].max()
#print(max_time)
csv_data.loc[csv_data["respond"] == -1, "dialog_speed"] = max_time * 1000
#print(pd.value_counts(csv_data.loc[csv_data["respond"] == -1, "dialog_speed"]))
csv_data = csv_data.loc[csv_data["dialog_speed"] > 0]
csv_data["dialog_speed"] = np.log(csv_data["dialog_speed"])
#csv_data["lexicons"] = np.log(csv_data["lexicons"])
#csv_data["readbility(CLI)"] = np.log(csv_data["readbility(CLI)"])
print(pd.value_counts(csv_data["respond"]))

normalize = lambda x: (x - x.min()) / (x.max() - x.min())

csv_data[['lexicons', 'readbility(CLI)']] = csv_data[['lexicons', 'readbility(CLI)']].apply(normalize)
csv_data.to_csv(res_dir)