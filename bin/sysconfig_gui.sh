#!/bin/sh
#
# Run the SysConfig graphical user interface with specified parameters
# 
# For help with command line arguments, see sysconfig_cli.sh

DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
NW="$DIR/nw/nwjs.app"
open "$NW" --args "$DIR" "$@" > /dev/null 2>&1 &
