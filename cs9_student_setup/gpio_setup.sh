#!/bin/bash
function setup_gpiozero {
        printf "Updating Pi and installing GPIOZERO library\n"

        sudo pip3 install gpiozero
        sudo apt-get install rpi.gpio
        sudo adduser $(whoami) gpio
}

setup_gpiozero

printf "\n"
printf "Your Pi is configured!\n"
printf "Rebooting Pi...\n"
sudo reboot
~                                                                             
~                                                                             
~                                                                             
~                                                                             
~                                                                             
~                              
