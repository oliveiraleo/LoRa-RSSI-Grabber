# LoRa-RSSI-Grabber

**NOTE:** This file is in a "work in progress" state, so expect to see some TODOs. The file will be updated and this message removed when everything is done

## Project Description

This source code provides a framework that sends control packets and collects RSSI measurements. It is designed to control Multitech`s mDot and xDot LoRa devices using the The Things Network infrastructure as backend. LoRa RSSI Grabber is capable of creating datasets cotaining RSSI measurements, it helped creating [this dataset](https://github.com/oliveiraleo/LoRa-RSSI-dataset-outdoor) and was used as a proof of concept of the first step of a key generation framework called [RSSignal](https://github.com/oliveiraleo/RSSignal-LoRa).

## Repository File Description

\- `send_position.py`: This is the legacy source code obtained from the [original repo](https://github.com/mateusomattos/loraLTA)

\- `send_control_packets.py`: Python script that contains the project's main functionality (Take a look at the section `Project Description`)

\- `pip-requirements.txt`: Python/pip modules required in order to run the python script (these should be already installed inside the env `pyvenv`)

\- `os-requirements.txt`: Operating system packets* required in order to run the python script

\* It's recommended to obtain these packets from your distro's official repositories (which is usually done through a packet manager (e.g. APT, DNF, Pacman, etc) )

## Requirements

- Any GNU/Linux Operating System (e.g. Debian, Ubuntu, etc)
- A BASH shell
- The packets inside the files [pip-requirements.txt](./pip-requirements.txt) & [os-requirements.txt](./os-requirements.txt)**
- An android GPS-enabled phone (see the subsection below)
- A LoRa End Device (e.g. Multitech mDot-915)

** Each file contains the name of the package and the version required in order to run correctly

### Configuring the GPS receiver

Please refer to the file [GPS-setup-android.md](./GPS-setup-android.md)

## Running the program on Linux-based systems

The instructions are as follows:

### 1- Clone the repository

<code>git clone https://github.com/oliveiraleo/LoRa-RSSI-Grabber.git</code>

### 2- Enter the project folder

<code>cd LoRa-RSSI-Grabber</code>

### 3- Load the virtual environment

<code>source pyvenv/bin/activate</code>

**NOTE:** The BASH console should now display `(pyvenv)` on the command line

**OBS:** To exit the env, just issue the command <code>deactivate</code>

### 4- Connect the equipment to the computer

If not already done, please connect the phone (or the GPS receiver) and the LoRa-enabled device

### 5- Run the script using

<code>python send_control_packets.py</code>

### 6- Follow the onscreen instructions

**NOTE:** Please, be sure that requirements from the section `Requirements` are met in order to correctly run the script

## Workflow

get-mqtt-data > send_control_packets > process_api_data > join_GW_ED_data

[TODO] create an image/diagram

## Component architecture

[TODO] put image here

## FAQ

### Q1: What makes your project stand out?

A: It provides an easy and standardized way to obtain RSSI measurements on both sides (ED & GW) of a LoRa communication.

### Q2: The gateway is reporting RSSI correctly but the device measurements are frozen/locked. What is happenning?

A: As you are getting measurements from both sides of the connection (ED & GW), you should send data (uplink) and receive something back on the device (downlink) in order to get signal emissions on both directions so to be able to get updated RSSI measurements on the device side too. It's possible to try to enable receiving ACKs if your LoRa device supports it.

### Q3: Why the computer can't connect to the android phone?

A: Check that the GPS related steps were successfully followed. Check that the USB cable is fully operational and the phone allows the computer to read its data. Then check that the adb program is working and issue the `adb forward` command.

### Q4: Why is the GPS reporting incorrect location data?

A: This can be the result of a couple of things: Poor GPS signal reception (e.g. inside an indoor place); GPS margin of error (e.g. position estimated error); Some or one ShareGPS app permission not allowed; Android's battery optimization is messing with the ShareGPS app; Phone is in energy saving mode; Bluetooth and/or WiFi location services (i.e. Wi-Fi & Bluetooth scanning) are enabled; [Google High Precision/Improved](https://support.google.com/android/answer/3467281) location option is disabled.

### Q5: I'm sure everything is set up correctly but the GPS still reports incorrect data or it freezes after some time. What else can I do?

A: If your android device is running android 8+, there are [some security implementations](https://developer.android.com/about/versions/oreo/background-location-limits) under the hood that limit the GPS functionality while in background. So please, install the app [Wakey](https://play.google.com/store/apps/details?id=com.doublep.wakey&hl=pt_BR) and don't let your screen go off during the survey. Keep the ShareGPS app onscreen all the time (i.e. don't minimize or close it). If you still face issues, try clicking "Start Track" *before* collecting GPS data (this will create a background service that will try to keep the GPS 'locked' (i.e. keeps requesting precise location every second)). The last attempt is to put the phone in airplane mode (disabling WiFi and Mobile Data), because this will prevent android from getting the approximate location from the carrier network or IP address (instead of the high precision one from GPS receiver) during the survey.

## Citing this work

If you used any of the source code available here, please, cite it as:

De Oliveira, L. A. (2023). *Arcabouços para Coleta de RSSI e Evolução de Técnicas de Acordo de Chaves em Redes LoRaWAN.* Federal University of Juiz de Fora.

### Latex citation

Or you can use the Latex citation below:

```
@phdthesis{leonardo2023arcaboucos,
 title = {Arcabouços para Coleta de RSSI e Evolução de Técnicas de Acordo de Chaves em Redes LoRaWAN},
 author = {Leonardo Azalim de Oliveira},
 month = {01},
 year = {2023},
 note = {Available at  http://monografias.ice.ufjf.br/tcc-web/tcc?id=724},
 school = {Federal University of Juiz de Fora},
 key = {OLIVEIRA,2023}
}
```

## Acknowledgments

The authors would like to thank Mr. Rogerio Casagrande and Mr. Thiago Scher, members of the LTA (Laboratorio de Telecomunicacoes Aplicadas) laboratory from the Engineering Faculty of the [Federal University of Juiz de Fora](https://ufjf.br), for assisting the configuration process and lending the LoRa equipment used during the deployment and test of the framework

## License

This source code is licensed under the [AGPL-3.0](https://opensource.org/licenses/AGPL-3.0) license