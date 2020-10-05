#!/bin/bash

args="$1"

if [ $args = "lcd" ]; then
	#copy lcd service file to systemd location
	cp dump_service_lcd.service /lib/systemd/system/dump_service_lcd.service
	echo "copied dump_service_lcd.service to /lib/systemd/system/dump_service_lcd.service"

	#change permissions for service file
	chmod 644 /lib/systemd/system/dump_service_lcd.service
	echo "changed permissions of /lib/systemd/system/dump_service_lcd.service to 644"

	#restart system daemon
	echo "restarting systemd daemon"
	systemctl daemon-reload
	echo "systemd daemon reloaded"

	#start service
	systemctl start dump_service_lcd.service
	echo "started dump_service_lcd.service"

	#enable service
	systemctl enable dump_service_lcd.service
	echo "enabled dump_service_lcd.service to start on boot"

elif [ $args = "auto" ]; then
	#copy no lcd service file to systemd location
	cp dump_service_no_lcd.service /lib/systemd/system/dump_service_no_lcd.service
	echo "copied dump_service_no_lcd.service to /lib/systemd/system/dump_service_no_lcd.service"
	
	# copy no lcd timer file to systemd location
	cp dump_timer_no_lcd.timer /lib/systemd/system/dump_timer_no_lcd.timer
	echo "copied dump_timer_no_lcd.service to /lib/systemd/system/dump_service_no_lcd.timer"

	#change permissions for service file
	chmod 644 /lib/systemd/system/dump_service_no_lcd.service
	echo "changed permissions of /lib/systemd/system/dump_service_no_lcd.service to 644"

	#change permissions for timer file
	chmod 644 /lib/systemd/system/dump_timer_no_lcd.timer
	echo "changed permissions of /lib/systemd/system/dump_timer_no_lcd.timer to 644"

	#restart system daemon
	echo "restarting systemd daemon"
        systemctl daemon-reload
        echo "systemd daemon reloaded"

	#start systemd service file
	systemctl start dump_service_no_lcd.service
	echo "started dump_service_no_lcd.service"

	#start systemd timer file
	systemctl start dump_timer_no_lcd.timer
	echo "started dump_timer_no_lcd.timer"

	#enable system service file
	systemctl enable dump_service_no_lcd.service
	echo "enabled dump_service_no_lcd.service to start on boot"

	#enable system timer file
	systemctl enable dump_timer_no_lcd.timer
        echo "enabled dump_timer_no_lcd.timer to start on boot"	
else
	echo "Invalid option - lcd or auto"
fi
