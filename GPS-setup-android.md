## Android GPS receiver setup

### 1- Install the app called [Share GPS](https://play.google.com/store/apps/details?id=com.jillybunch.shareGPS) from Google PlayStore

### 2- If not yet done, enable the Android Debugging mode

**NOTE:** The steps for this part are different for each phone model, so please do your own research. The general steps are: activate the Developer Options (by clicking in the build information) and then activate the USB debugging option.

### 3- If not already done, install the Android Debugging Bridge (ADB) on your Linux system

**TIP:** Run `adb devices` on a console and it should return that your phone is connected

### 4- Open the Share GPS app and give the required permissions

### 5- Head to the `CONNNECTIONS` tab

#### 5.1- Click on the `ADD` button

#### 5.2- On the new screen, configure equals to the list below:

- **Activity:** Share my GPS with a laptop...using NMEA
- **Connection Method:** Use USB to send NMEA or host a GPSD server
- **Name:** PC (choose anything memorable)

#### 5.3- Click `NEXT`

#### 5.4- Leave the `Port` attribute at 50000 and hit `OK`

### 6- Back on the main screen, click on 3-dot menu to open Settings

#### 6.1- Enable the option `Create NMEA`

#### 6.2- Go back to the previous screen

### 7- Click once on the connection name (e.g. PC)

#### 7.1- Now the status must be changed from `Idle` (blue) to `Listening` (yellow)

#### 7.2- The phone is ready to be connected via USB now

**NOTE:** The status on `GPS STATUS` tab should be 3D Fix (green), if not, try to go to an outdoor place for some minutes or until the phone locks the position

**TIP:** For normal usage, just open the app and follow the step 7 instructions again