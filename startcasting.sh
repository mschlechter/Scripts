#!/bin/sh
#
# Startup script voor narrowcasting.
#
# Zorg ervoor dat midori, unclutter en matchbox geinstalleerd zijn.
#

# URL wordt geladen uit /boot/easycast.url.txt bestand

URL=""

if [ -e "/boot/easycast.url.txt" ]
then
	URL=$(cat /boot/easycast.url.txt)
fi

# Laat de rest van het script zijn werk doen

xset -dpms # disable DPMS (Energy Star) features.
xset s off # disable screen saver
xset s noblank # don't blank the video device

sleep 5

matchbox-window-manager & unclutter & 
midori -e Fullscreen -a $URL

