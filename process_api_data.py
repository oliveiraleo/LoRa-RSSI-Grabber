import json
import csv
import base64

def get_file_data(file_name):
    with open(file_name, "r") as f:
        print("[INFO] Reading the file", file_name)
        data = f.read()
    
    return data

def process_raw_data(data, file_name_to_save):
    d_list = data.splitlines()
    j_list = []
    id_and_rssi_list = []
    for elem in d_list:
        if elem != '': #filters out the blank lines
            j_list.append(elem)

    header = ['id', 'GW RSSI'] #header for the CSV file
    clean_file_name = file_name_to_save.split('_')
    file_name = clean_file_name[0] + '_' + clean_file_name[1] + '_LoRa-RSSI-GW-decoded.csv'
    
    with open(file_name, 'w+') as f:
        write = csv.writer(f) #creates a reader object
        write.writerow(header) #writes the reader line at the beggining of the file

        for elem in j_list: #filters the data of interest and writes it to the CSV file
            dct = json.loads(elem)
            try: #executes the filtering according to the Storage API data format
                rssi = dct['result']['uplink_message']['rx_metadata'][0]['rssi']
                id_base64 = dct['result']['uplink_message']['frm_payload']

            except KeyError: #if it fails, tries to filter according to the MQTT API data format
                try:
                    rssi = dct['uplink_message']['rx_metadata'][0]['rssi']
                    id_base64 = dct['uplink_message']['frm_payload']
                except KeyError: #ignores the join requests or other data that doesn't contain RSSI on its headers
                    print("[ERROR] Error parsing some data\n[INFO] Probably it's join request data, ignoring it...")
                    continue

            except json.decoder.JSONDecodeError:
                print("[ERROR] Couldn't parse data! Please, check if you choose the correct file")
                raise SystemExit(0)

            id_b64_encoded = id_base64.encode('ascii')
            id = base64.b64decode(id_b64_encoded).decode('ascii')

            data_line = [str(id), str(rssi)]
            write.writerow(data_line)

        print(f"[INFO] File {file_name} saved successfully")

def menu():
    print("Please, give the name of the TXT file you want to read from")
    file_name = str(input("Type (or paste) it here: "))

    file_data_raw = get_file_data(file_name)
    process_raw_data(file_data_raw, file_name)

def main():
    menu() #TODO add some commets to explain what is happening here

# Calls the main function
if __name__ == "__main__":
    main()
