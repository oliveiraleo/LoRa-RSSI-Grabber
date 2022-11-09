import socket
import time
import serial
import pynmea2
from datetime import datetime
import traceback
# import sys, select, os #for loop exit

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

# Safely ends the script
def killScript():
    endDevice.closeSerialPort()
    raise SystemExit(0) # stops the exectution

def sendLoRaJoinRequest():
    endDevice.sendMessage('AT+JOIN')
    # endDevice.printLstAnswer()

def getDeviceUpdatedRSSI():
    # resetSerialPort()
    # time.sleep(1)
    endDevice.sendMessage('AT+RSSI')
    endDevice.printLstAnswer()
    answerData = (endDevice.getLstAnswer()).splitlines() # splitlines to add returned data to a list
    RSSIFullData = []
    for elem in answerData:
        try:
            RSSIFullData.append(int(elem))
        except ValueError:
            pass
    # RSSIFullData = answerData[2].split(",") # last, xxx, xxx, avg (NOTE: since last reset/reboot)
    print("answerData:", answerData)
    print("RSSIFullData", RSSIFullData)
    lastPktRSSI = int(RSSIFullData[0])
    
    print("lastPktRSSI:", lastPktRSSI)

    return lastPktRSSI
    #TODO fix the return data being empty

def resetSerialPort():
    endDevice.closeSerialPort()
    time.sleep(2)
    endDevice.openSerialPort()

#TODO Create the main function and keep refactoring the code to separate and modularize it
#TODO Create the main menu to help the user control the program
endDevice = LoraEndDevice() # instantiate the ED object
try:
    endDevice.openSerialPort()
except serial.serialutil.SerialException:
    traceback.print_exc() # prints the error stack trace
    print("[ERROR] Error connecting to the serial port!")
    print(f"[INFO] Please check the serial port permissions using ls.\n[INFO] You can also try to run the command below:\nsudo chmod 666 {endDevice.loraSerial.port}\n[INFO] To change the permission")
    killScript()

delayBetweenPkt_sec = 3*60 
HOST = 'localhost'  # The server's hostname or IP address (to get  the GPS position from)
PORT = 20175        # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        print(f"Successfully connected to {HOST}:{PORT}")
    except ConnectionRefusedError:
        print(f"[ERROR] Got \"connection refused\" error while trying to connect to {HOST}:{PORT}")
        print("[INFO] Make sure you have properly setup the GPS device\n[INFO] Remember to make the port redirect. You can use the command below\nadb forward tcp:20175 tcp:50000\n[INFO] To enable it")
        killScript()

    id=0
    print("Begin to send control packets...")
    while id<5:        

        now = datetime.now()
        time_hour = now.strftime("%H:%M:%S")
        data = s.recv(1024).decode("utf-8")
        position = data.splitlines(0)[0]
        latitude = pynmea2.parse(position).latitude #latitude using float type (unit: decimal degrees)
        longitude = pynmea2.parse(position).longitude #longitude using float type (unit: decimal degrees)
        altitude = pynmea2.parse(position).altitude #altitude in meters, above sea level
        precision = pynmea2.parse(position).gps_qual #quality of GPS reception (ideally should be = '1')
        satellites = pynmea2.parse(position).num_sats #number of connected satellites

        endDevice.sendPacketToGateway(id) #sends packets containing the id inside
        lastRSSI = getDeviceUpdatedRSSI() #RSSI measured by the device

        data_to_send = '[{}] Id:{}, Lat: {}, Lon: {}, Alt:{}, Qual:{}, Sats:{}, RSSI:{}'. \
        format(time_hour, id, latitude, longitude, altitude, precision, satellites, lastRSSI)

        print(data_to_send)
        # endDevice.sendMessage('AT')
        # endDevice.printLstAnswer()

        id = id+1

        print(f"Packet {id} sent, sleeping...")
        time.sleep(3)
        # time.sleep(delayBetweenPkt_sec)

endDevice.closeSerialPort()
s.detach()
