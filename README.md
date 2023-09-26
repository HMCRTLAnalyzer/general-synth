# Table of Contents
- [Table of Contents](#table-of-contents)
- [General Synthesis Tool](#general-synthesis-tool)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Usage](#usage)


# General Synthesis Tool

This project aims to create a generalized synthesis flow for aiding the HMC RTL analysis efforts. 

## Prerequisites
This project was developed on Rocky Linux 8.8 Green Obsidian.

The tools used for these specific scripts require:
- Synopsys Design Compiler
  - The version used to test these scripts is version S-2021.06-SP4. 
- Make
  

## Setup
Setting the configuration options in the Makefile is important to getting the scripts to synthesize properly. Importantly, the path to the different process technologies must be set to point to the correct .db file (s). 

## Usage

To call the synthesis script, go to the `general-synth` directory and use the following:
```
make synth DESIGN_NAME=<top module of HDL design> SRC_PATH=<path to source file directory>
```

Additional optional parameters include:
- TECH
- MAX_AREA
- MAX_POWER
- MAX_FANOUT
- HDL_LANG
- CLK_PERIOD

These have defaults set in the configun of the Makefile, but can be overriden with command line arguments. Eventually these options will be configurable using a configuration file with a Python wrapper.
