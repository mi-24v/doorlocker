#!/bin/sh
$server_port=8080
$controller_port=8888
ssh -f -N -R $server_port:127.0.0.1:$controller_port user@example.com

