import pandas as pd

print("Please, provide the name of the files to be joinned")
file_names = input("Type (or paste) it here: ")

clean_file_name = file_names.split('_')
file_name_preffix = clean_file_name[0] + '_' + clean_file_name[1] #gets only date + time
file_name = file_name_preffix + "_Full-Collected-data.txt" #adds the name

file1 = file_name_preffix + "_LoRa-Device-GPS-RSSI-data.csv" #device data
file2 = file_name_preffix + "_LoRa-RSSI-GW-decoded.csv" #gw data

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

data_frame = pd.merge(df1, df2, left_on='id', right_on='id', how='inner')

# print(data_frame) #DEBUG

print("[INFO] Saving content to the file ", file_name)
data_frame.to_csv(file_name, index=False)
print("[INFO] Content saved successfully")

#TODO Save another copy only with the RSSIs inside
