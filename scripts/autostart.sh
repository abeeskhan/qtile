#!/bin/bash

function run {
	if ! pgrep $1;
	then
		$@&
	fi
}

run compton --vsync opengl-swc --backend glx &
run nitrogen --restore &
run nm-applet &
run blueman-applet &
run volumeicon &
run dunst &
run sxhkd &
