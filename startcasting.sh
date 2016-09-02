#!/bin/sh
#
# Startup script voor narrowcasting.
#
# Zorg ervoor dat midori, unclutter en matchbox geinstalleerd zijn.
#

# Zet hier de URL
URL=http://narrowcast.autotaal.biz/webplayer/imageviewer2.aspx?nodeid=417

# Laat de rest van het script zijn werk doen

xset -dpms # disable DPMS (Energy Star) features.
xset s off # disable screen saver
xset s noblank # don't blank the video device

unclutter # kill de mouse pointer

matchbox-window-manager & 
midori -e Fullscreen -a $URL

