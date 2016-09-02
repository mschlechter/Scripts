#!/bin/sh
#
# Startup script voor narrowcasting.
#
# Zorg ervoor dat midori, unclutter en matchbox geinstalleerd zijn.
#
# Je kunt dit script installeren door het op te slaan als het ~/.xsession
# bestand. Zodra X wordt opgestart, worden de onderstaande commando's
# uitgevoerd.

# Zet hier de URL
URL=http://narrowcast.autotaal.biz/webplayer/imageviewer2.aspx?nodeid=417

# Laat de rest van het script zijn werk doen

xset -dpms # disable DPMS (Energy Star) features.
xset s off # disable screen saver
xset s noblank # don't blank the video device

# Start midori fullscreen en verberg de mouse pointer
matchbox-window-manager & unclutter & 
midori -e Fullscreen -a $URL

