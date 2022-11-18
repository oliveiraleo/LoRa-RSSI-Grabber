import socket
import time
import serial
import pynmea2
from datetime import datetime
import traceback
# import sys, select, os #for loop exit
import re

"""
To use, download the app share GPS and create a USB connection using adb and tcp forward.
Run: adb forward tcp:20175 tcp:50000
"""


# 
# sudo chmod a+rw /dev/ttyUSB0
class LoraEndDevice:
    def __init__(self):

        self.loraSerial = serial.Serial()
        self.loraSerial.port = '/dev/ttyUSB0'
        self.loraSerial.baudrate = 115200
        self.loraSerial.bytesize = 8
        self.loraSerial.parity='N'
        self.loraSerial.stopbits=1
        self.loraSerial.timeout=2
        self.loraSerial.rtscts=False
        self.loraSerial.xonxoff=False

        self.lastAtCmdRx = ''

    def setPortCom(self, newPort):
        self.loraSerial.port = newPort

    def openSerialPort(self):
        self.loraSerial.open()

    def closeSerialPort(self):
        self.loraSerial.close()

    def sendCmdAt(self,cmd):
        if self.loraSerial.is_open:
            self.loraSerial.write(cmd.encode())
        else:
            print('It\'s not possible to communicate with LoRa module!')

    def getAtAnswer(self):
        self.lastAtCmdRx = self.loraSerial.read(100)

    # gets the answer of device's serial port (e.g. the messages you see when using minicom)
    def printLstAnswer(self):
        print(self.lastAtCmdRx.decode('UTF-8'))

    def getLstAnswer(self):
        data = self.lastAtCmdRx.decode('UTF-8')
        return data

    # sends a command via serial port
    def sendMessage(self, msg):
        msg = '{}\r\n'.format(msg)
        self.sendCmdAt(msg)
        self.getAtAnswer()
    
    def sendPacketToGateway(self, message):
        cmd = 'AT+SEND=' + str(message)
        self.sendMessage(cmd)
        self.printLstAnswer()

#TODO Move all device functions to its class

# Safely ends the script
def killScript():
    endDevice.closeSerialPort()
    raise SystemExit(0) # stops the exectution

def sendLoRaJoinRequest():
    endDevice.sendMessage('AT+JOIN')
    # endDevice.printLstAnswer()

def getDeviceUpdatedRSSI():
    resetSerialPort()
    # time.sleep(1)
    endDevice.sendMessage('AT+RSSI')
    answer = endDevice.getLstAnswer() #.splitlines()
    answerData = map(int, re.findall('-?\d+', answer))
    RSSIFullData = list(answerData) # last, min, max, avg (NOTE: since last reset/reboot)
    # print("answer:", answer) #DEBUG
    # print("answerData:", answerData) #DEBUG
    print("RSSIFullData", RSSIFullData) #DEBUG
    lastPktRSSI = RSSIFullData[0]
    
    print("lastPktRSSI:", lastPktRSSI) #DEBUG

    return lastPktRSSI

def resetSerialPort():
    endDevice.closeSerialPort()
    time.sleep(2)
    endDevice.openSerialPort()

def returnFilteredINTs(data_stream):
    data_stream_list = data_stream.splitlines()
    # print(data_stream_list) #DEBUG
    filtered_data = []
    for elem in data_stream_list: #ignores anything but int numbers
        try:
            filtered_data.append(int(elem))
        except ValueError:
            pass
    return filtered_data

def checkJoinStatus():
    endDevice.sendMessage('AT+NJS?')
    # endDevice.printLstAnswer() #DEBUG
    answer_data = endDevice.getLstAnswer()
    data = returnFilteredINTs(answer_data)
    try:
        status = data[0]
        if status == 0:
            return False
        elif status == 1:
            return True
    except:
        print("Error aquiring join status! Please, check the serial connection")
        killScript()
        return None

def main_menu():
    print("-Script Main Menu-")
    option = print_menu_options()
    # while option != 0:
    if option == 0:
        print("[INFO] User asked to exit... Bye!")
        killScript()
    elif option == 1:
        # sendLoRaJoinRequest()
        print("Join request selected!")
    elif option == 2:
        # checkJoinStatus()
        print("Join status selected!")
    else:
        print("[ERROR] An invalid option was choosen, please try again")
        main_menu()

def print_menu_options():
    print("Please, choose an option:")
    print("\
1- Send a join request\n\
2- Get the join status\n\
3- Start sending the control packets\n\
0- Exit the program")
    opt = input("\nYour option: ")
    return int(opt)

#TODO Create the main function and keep refactoring the code to separate and modularize it
#TODO Create the main menu to help the user control the program
#TODO If rssi still fails, try using AT+NLC (see manual)
# Vars / Pre setup #
endDevice = LoraEndDevice() # instantiate the ED object
try:
    endDevice.openSerialPort()
except serial.serialutil.SerialException:
    traceback.print_exc() # prints the error stack trace
    print("[ERROR] Error connecting to the serial port!")
    print(f"[INFO] Please check the serial port permissions using ls.\n[INFO] You can also try to run the command below:\nsudo chmod 666 {endDevice.loraSerial.port}\n[INFO] To change the permission")
    killScript()

delayBetweenPkt_sec = 3*60 #TODO Update the delay to adhere to maximum duty time
HOST = 'localhost'  # The server's hostname or IP address (to get  the GPS position from)
PORT = 20175        # The port used by the server

main_menu()

# sendLoRaJoinRequest()
# time.sleep(6)

#TODO Create a way to auto join the network
# joinned_network = checkJoinStatus()
# print(joinned_network)

# endDevice.sendMessage('AT+SEND=0')
# endDevice.getAtAnswer()
# endDevice.printLstAnswer()

# if joinned_network == False:
#     print("Device didn't join the network yet!")
#     killScript()

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     try:
#         s.connect((HOST, PORT))
#         print(f"Successfully connected to {HOST}:{PORT}")
#     except ConnectionRefusedError:
#         print(f"[ERROR] Got \"connection refused\" error while trying to connect to {HOST}:{PORT}")
#         print("[INFO] Make sure you have properly setup the GPS device\n[INFO] Remember to make the port redirect. You can use the command below\nadb forward tcp:20175 tcp:50000\n[INFO] To enable it")
#         killScript()

#     id=0
#     print("Sending control packets...")
#     while id<100:        
#         try:
#             now = datetime.now()
#             time_hour = now.strftime("%H:%M:%S")
#             data = s.recv(1024).decode("utf-8") #reads 1024 bytes from the buffer and converts it to utf-8 chars
#             full_GPS_data = data.splitlines(0) #splits the data in a list of strings
#             # print(f"full_GPS_data: {full_GPS_data}") #DEBUG

#             pos_pattern = ".GPGGA*" #regex pattern to find the GPGGA GPS data
#             filtered_GPS_data = [x for x in full_GPS_data if re.match(pos_pattern, x)] #matches the pos_pattern pattern using list comprehension
#             # print(f"filtered_GPS_data: {filtered_GPS_data}") #DEBUG
#             position = filtered_GPS_data[0] #gets the first match

#             #parses the data retrieved from the phone
#             latitude = pynmea2.parse(position).latitude #latitude using float type (unit: decimal degrees)
#             longitude = pynmea2.parse(position).longitude #longitude using float type (unit: decimal degrees)
#             altitude = pynmea2.parse(position).altitude #altitude in meters, above sea level
#             precision = pynmea2.parse(position).gps_qual #quality of GPS reception (ideally should be = '1')
#             satellites = pynmea2.parse(position).num_sats #number of connected satellites

#             # endDevice.sendPacketToGateway(id) #sends a packet containing the id inside
#             time.sleep(2)
#             # lastRSSI = getDeviceUpdatedRSSI() #RSSI measured by the device
#             lastRSSI = 0

#             data_to_send = '[{}] Id:{}, Lat: {}, Lon: {}, Alt:{}, Qual:{}, Sats:{}, RSSI:{}'. \
#             format(time_hour, id, latitude, longitude, altitude, precision, satellites, lastRSSI)

#             print(data_to_send) #TODO Write that data into a CSV file
#             # endDevice.sendMessage('AT')
#             # endDevice.printLstAnswer()
        
#             id = id+1

#             print(f"Packet {id} sent, sleeping...")
#             time.sleep(5)
#             # time.sleep(delayBetweenPkt_sec)

#         except KeyboardInterrupt:
#             s.close() #closes the connection to the GPS server
#             print("\n[INFO] User asked to exit... Bye!")
#             killScript()

# s.close() #closes the connection to the GPS server
# endDevice.closeSerialPort()
