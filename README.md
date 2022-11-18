# LoRaLTA

**NOTE:** This file is in a "work in progress" state, so expect to see some TODOs. The file will be updated and this message removed when everything is done

## Project Description

TODO

## Repository File Description

\- `send_position.py`: This is the legacy source code obtained from the [original repo](https://github.com/mateusomattos/loraLTA)

\- `send_control_packets.py`: Python script that contains the project's functionality (Take a look at the section `Project Description`)

\- `pip-requirements.txt`: Python/pip modules required in order to run the python script (these should be already installed inside the env `pyvenv`)

\- `os-requirements.txt`: Operating system packets* required in order to run the python script

\* It's recommended to obtain these packets from your distro's official repositories (which is usually done through a packet manager (e.g APT) )

## Requirements

- Any GNU/Linux Operating System (e.g. Debian, Ubuntu, etc)
- A BASH shell
- The packets inside the files [pip-requirements.txt](./pip-requirements.txt) & [os-requirements.txt](./os-requirements.txt)**
- An android GPS-enabled phone (see the subsection below)
- A LoRa End Device (e.g. Multitech mDot)  <!-- TODO specify the device model here -->


** Each file contains the name of the package and the version required in order to run correctly

TODO Finish this subsection

### Configuring the GPS receiver

#### 1- Install the app called [Share GPS](https://play.google.com/store/apps/details?id=com.jillybunch.shareGPS) from Google PlayStore

#### 2- Open the app and give the required permissions

#### 3- Head to the `CONNNECTIONS` tab

#### 3.1- Click on the `ADD` button

#### 3.2- On the new screen, configure equals to the list below:

- **Activity:** Share my GPS with a laptop...using NMEA
- **Connection Method:** Use USB to send NMEA or host a GPSD server
- **Name:** PC (choose anything memorable)

#### 3.3- Click `NEXT`

#### 3.4- Leave the `Port` attribute at 50000 and hit `OK`

#### 4- Back on the main screen, click on 3-dot menu to open Settings

#### 4.1- Enable the option `Create NMEA`

#### 4.2- Go back to the previous screen

#### 5- Click once on the connection name (e.g. PC)

#### 5.1- Now the status must be changed from `Idle` (blue) to `Listening` (yellow)

#### 5.2- The phone is ready to be connected via USB now


**NOTE:** The status on `GPS STATUS` tab should be 3D Fix (green), if not, try to go to an outdoor place for some minutes or until the phone locks the position

**NOTE2:** To normal usage, just open the app and follow the step 5 again

## Running the program on Linux-based systems

The instructions are as follows:

### 1- Clone the repository

<code>git clone https://github.com/oliveiraleo/LoRaLTA.git</code>

### 2- Enter the project folder

<code>cd LoRaLTA</code>

### 3- Load the virtual environment

<code>source pyenv/bin/activate</code>

**NOTE:** The BASH console should now display `(pyenv)` on the command line

**OBS:** To exit the env, just issue the command <code>deactivate</code>

### 4- Connect the equipment to the computer

If not already done, please connect the phone (or the GPS receiver) and the LoRa-enabled device

### 5- Run the script using

<code>python send_control_packets.py</code>

### 6- Follow the onscreen instructions

**NOTE:** Please, be sure the requirements from the section `Requirements` are met in order to correctly run the script

## Acknowledgments

TODO

## License

This source code is licensed under the [AGPL-3.0](https://opensource.org/licenses/AGPL-3.0) license