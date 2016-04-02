#!/bin/bash

if [ "$(uname)" == "Darwin" ];then
	export DYLD_FALLBACK_LIBRARY_PATH="/opt/local/lib/:$DYLD_FALLBACK_LIBRARY_PATH"
fi

if [ -z "$@" ];then
	export args="-i \"Q49 MIDI 1\" -o \"USB2.0-MIDI MIDI 1\""
else
	export args="$@"
fi

export program="$(which python3)"
export args="-i driver.py ${args}"
export runnable="${program} ${args}"
echo $runnable
eval "${runnable}"
