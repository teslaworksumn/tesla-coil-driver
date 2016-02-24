# tesla-coil-driver
Drives the musical tesla coil via MIDI

## Usage:
`./driver.sh [input] [output]`

where [input] is the name of the midi port you would like to use as an input
and [output] is the name of the midi port you would like to use as an output

Use `./start_unix.sh list` to list the available inputs and outputs.

You may also use `./start_unix.sh list inputs` or `./start_unix.sh list outputs`
to list the inputs and outputs respectively.

`start_unix.sh` is a wrapper script for `driver.py` that initializes shell 
variables on some systems and sets some arguments automatically.  If it is 
called without arguments, it will assume the input "" and the output ""