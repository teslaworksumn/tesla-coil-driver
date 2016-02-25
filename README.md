# tesla-coil-driver
Drives the musical tesla coil via MIDI

## Usage:
`./driver.sh [input] [output]`

where [input] is the name of the midi port you would like to use as an input
and [output] is the name of the midi port you would like to use as an output

Use `./start_unix.sh --list` to list the available inputs and outputs.

This list will be in the format:

    Available inputs:
     input1
     input2
    Available outputs:
     output1
     output2

The inputs and outputs will begin with a space, if you want to parse this list.

`start_unix.sh` is a wrapper script for `driver.py` that initializes shell 
variables on some systems and sets some arguments automatically.  If it is 
called without arguments, it will assume the input "" and the output ""