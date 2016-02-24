#!/bin/bash

if [ "$(uname)" == "Darwin" ];then
	export DYLD_FALLBACK_LIBRARY_PATH="/opt/local/lib/:$DYLD_FALLBACK_LIBRARY_PATH"
fi

python3 -i driver.py "$@"
