# ---------------- CONFIG -----------------------
SKY130_PATH := /opt/riscv/cad/lib/sky130_osu_sc_t12/12T_hs/lib/sky130_osu_sc_12T_hs_tt_1P20_25C.ccs.db
TECH ?= sky130
MAX_AREA ?= 0.0
MAX_POWER ?= 0.0
MAX_FANOUT ?= 0

# CLK_PERIOD is in nanoseconds
CLK_PERIOD ?= 100.0

# if make is called with TECH=sky130, set the tech path
ifeq ($(TECH), sky130)
	TECH_PATH = $(SKY130_PATH)
endif


ifndef DESIGN_NAME
$(error DESIGN_NAME not set, please set in order to continue)
endif

ifndef SRC_PATH
$(error SRC_PATH not set, please set in order to continue)
endif

RESULTS_DIR = ./$(DESIGN_NAME)_results


test:
	echo arg passed in is $(TECH_PATH), $(MAX_AREA), $(CLK_PERIOD)

synth: 
# export config options as environment variables
	export TECH_PATH=$(TECH_PATH) && \
	export MAX_AREA=$(MAX_AREA) && \
	export DESIGN_NAME=$(DESIGN_NAME) && \
	export SRC_PATH=$(SRC_PATH) && \
	export CLK_PERIOD=$(CLK_PERIOD) && \
	export MAX_POWER=$(MAX_POWER) && \
	export MAX_FANOUT=$(MAX_FANOUT) && \
	echo synthesis was executed
#	dc_shell-xg-t -f synthesis.tcl | tee 

clean:
# something here, probably deleting the results folder and going from there


