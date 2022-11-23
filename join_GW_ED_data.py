import pandas as pd

print("Please, provide the name of one of the files to be joinned\nNOTE: Assuming both have the same preffix (date + time)")
file_names = input("Type (or paste) it here: ")

clean_file_name = file_names.split('_')
file_name_preffix = clean_file_name[0] + '_' + clean_file_name[1] #gets only date + time
file_name = file_name_preffix + "_Full-Collected-data.csv" #adds the name
file_name_rssi = file_name_preffix + "_RSSI-data.csv" #adds the name

# The two files to get data from
file1 = file_name_preffix + "_LoRa-Device-GPS-RSSI-data.csv" #device data
file2 = file_name_preffix + "_LoRa-RSSI-GW-decoded.csv" #gw data

# Reads their content
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

#merge only merges the lines where keys exist, so the packages that didn't arrive at the gw are discarded automatically
data_frame = pd.merge(df1, df2, left_on='id', right_on='id', how='inner')

#extracts only the RSSI columns
data_frame_rssi = data_frame[['GW RSSI', 'ED RSSI']]

# print(data_frame) #DEBUG
# print(data_frame_rssi) #DEBUG

# Saves the results on CSV files
print("[INFO] Saving full content to the file ", file_name)
data_frame.to_csv(file_name, index=False)
print("[INFO] Full content saved successfully")
print("[INFO] Saving RSSI content to the file ", file_name_rssi)
data_frame_rssi.to_csv(file_name_rssi, index=False)
print("[INFO] RSSI content saved successfully")
