#!/bin/bash
export XDG_RUNTIME_DIR=/run/user/1000
battery_level=`acpi -b | grep -P -o '[0-9]+(?=%)'`
datum=$(date +"%Y.%d.%m. %H:%M")
if [ $battery_level -ge 80 ]; then
  /usr/bin/notify-send "Battery Full" "Level: ${battery_level}%"
  /usr/bin/paplay /usr/share/sounds/freedesktop/stereo/complete.oga
  echo "${datum} - Battery Full" >> $HOME/battery_alert.log
elif [ $battery_level -le 15 ]; then
  /usr/bin/notify-send --urgency=CRITICAL "Battery Low" "Level: ${battery_level}%"
  /usr/bin/paplay /usr/share/sounds/freedesktop/stereo/suspend-error.oga
  echo "${datum} - Battery Critically Low" >> $HOME/battery_alert.log
elif [ $battery_level -le 25 ]; then
  /usr/bin/notify-send "Battery Low" "Level: ${battery_level}%"
  /usr/bin/paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga
  echo "${datum} - Battery Low" >> $HOME/battery_alert.log
fi
