## Requirements and virtual environment setup

**NOTE:** The steps of this subsection may be required to run only on the for the first time. Once done, it's possible to skip them.

### 1- Install the OS requirements

These are listed on the [os-requirements.txt](./os-requirements.txt) file. The exact steps may vary according to the OS.

### 2- Clone the repository

```
git clone https://github.com/oliveiraleo/LoRa-RSSI-Grabber.git
```

### 3- Enter the project folder

```
cd LoRa-RSSI-Grabber
```

### 4- Create a new virtual environment

```
python -m venv pyvenv
```
This command will create a venv called `pyvenv`

### 5- Load the virtual environment

```
source pyvenv/bin/activate
```

**NOTE:** The BASH console should now display `(pyvenv)` on the command line

### 6- Install the python/pip requirements

```
pip install -r pip-requirements.txt
```

Now, please, follow the steps below step 2 of the [next](./README.md#running-the-program-on-linux-based-systems) subsection