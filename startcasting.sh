#!/bin/sh
#
# Startup script voor narrowcasting.
#
# Zorg ervoor dat midori, unclutter en matchbox geinstalleerd zijn.
#

# Zet hier de URL
URL=http://ncsilfhout.autotaal.biz:8092/webplayer/imageviewer.aspx?nodeid=1

# Laat de rest van het script zijn werk doen

xset -dpms # disable DPMS (Energy Star) features.
xset s off # disable screen saver
xset s noblank # don't blank the video device

sleep 5

matchbox-window-manager & unclutter & 
midori -e Fullscreen -a $URL

