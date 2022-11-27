#!/bin/sh
# This will connect to the MQTT end point and listen for the data

# NOTE: The attribute "frm_payload" will be base64 encoded

END_POINT_SERVER="nam1.cloud.thethings.network"
MQTT_PORT="1883"
APP_NAME=$1
TOPIC_TYPE="#" #See the reference for other options
API_KEY=$2
FILE_NAME="GW-MQTT-API-data.txt"

if [[ $# -ne 2 ]]
then
    echo "USAGE: $0 APPLICATION-NAME MQTT-API-KEY"
    echo "EXAMPLE: $0 application-1 NNSXS.BAA[REDACTED]"
else
    echo "[INFO] Connecting to the server with these parameters:"
    echo "Hostname: $END_POINT_SERVER"
    echo "Port: $MQTT_PORT"
    echo "Application name: $APP_NAME"
    echo -e "Topic type: $TOPIC_TYPE \n"

    echo "[INFO] Saving the content to the file $FILE_NAME"

    echo "[INFO] Connected to the MQTT end point..."
    mosquitto_sub -h $END_POINT_SERVER -p $MQTT_PORT -u "$APP_NAME@ttn" -P $API_KEY -t $TOPIC_TYPE > $FILE_NAME
    echo "[INFO] Data saved to the file $FILE_NAME"
    echo "[INFO] Don't forget to rename it"
    echo -e "\nDisconnecting... Bye!"
fi

# Reference for this script: https://www.thethingsindustries.com/docs/integrations/mqtt/#mqtt-clients