#!/bin/bash
servo_setup(){
	echo -n "servo init..."

	gpio -g mode 18 pwm
	gpio pwm-ms
	# 50 Hz = 19.2e6 Hz / pwmClock / pwmRange
	gpio pwmc 1920 #clock 1920
	gpio pwmr 200 #range 200

	echo -e "[\e[32mOK\e[m]"
}

servo_shutdown(){
	echo -n "shutdowning..."

	gpio -g mode 18 output
	gpio -g write 18 0

	echo -e "[\e[32mOK\e[m]"
}

door_close(){
	echo -n "door closing..."

	#pwm <pin> <val(0-1023)>
	gpio -g pwm 18 22 #1.3msec
	#gpio -g pwm 18 26 #max?
	sleep 1
	gpio -g pwm 18 10
	sleep 1

	echo -e "[\e[32mOK\e[m]"
}
door_open(){
	echo -n "door opening..."

	gpio -g pwm 18 1 #0.2msec
	sleep 1
	gpio -g pwm 18 10
	sleep 1

	echo -e "[\e[32mOK\e[m]"
}

door_open_via_serial(){
	echo -n "door opening..."
	echo open > /dev/ttyAMA0
	echo -e "[\e[32mOK\e[m]"
}

door_close_via_serial(){
	echo -n "door closing..."
	echo close > /dev/ttyAMA0
	echo -e "[\e[32mOK\e[m]"
}

parse_args(){
	declare -i argc=0
	declare -a argv=()

	while (( $# > 0 ))
	do
		case "$1" in
			-*)
				if [[ "$1" =~ 'o' ]]; then
					oflag='-o'
				fi
				if [[ "$1" =~ 'c' ]]; then
					cflag='-c'
				fi
				if [[ "$1" =~ 'r' ]]; then
					rflag='-r'
				fi
				if [[ "$1" =~ 's' ]]; then
					sflag='-s'
				fi
				if [[ "$1" =~ 'h' ]]; then
					hflag='-h'
				fi
				shift
				;;
			*)
				((++argc))
				argv=("${argv[@]}" "$1")
				shift
				;;
		esac
	done
}

main_operation(){
	flag_done=false
	if [[ -n "$oflag" && -n "$rflag" ]]; then
		servo_setup
		door_close
		servo_shutdown
		flag_done=true
	elif [[ -n "$oflag" && -n "$sflag" ]]; then
		door_open_via_serial
		flag_done=true
	elif [[ -n "$oflag" ]]; then
		servo_setup
		door_open
		servo_shutdown
		flag_done=true
	fi

	if [[ -n "$cflag" && -n "$rflag" ]]; then
		servo_setup
		door_open
		servo_shutdown
		flag_done=true
	elif [[ -n "$cflag" && -n "$sflag" ]]; then
		door_close_via_serial
		flag_done=true
	elif [[ -n "$cflag" ]]; then
		servo_setup
		door_close
		servo_shutdown
		flag_done=true
	fi
}

#main

parse_args $@
echo "door operation start."

main_operation

if [[ "$flag_done" = false ]]; then
	echo "no options specified. listening to standard input."

	read operation1 operation2
	operations=($operation1 $operation2)
	parse_args $operations

	main_operation
fi

echo "door operation done."

