# ---------------- CONFIG -----------------------
SKY130_PATH := /opt/riscv/cad/lib/sky130_osu_sc_t12/12T_hs/lib/sky130_osu_sc_12T_hs_tt_1P20_25C.ccs.db
TECH ?= sky130
MAX_AREA ?= 0.0
MAX_POWER ?= 0.0
MAX_FANOUT ?= 0
# HDL_LANG option is either verilog, sverilog, or vhdl. default to verilog unless set otherwise
HDL_LANG ?= verilog
EXPERIMENT_NAME ?= test

# CLK_PERIOD is in nanoseconds
CLK_PERIOD ?= 100.0

# if make is called with TECH=sky130, set the tech path
ifeq ($(TECH), sky130)
	TECH_PATH = $(SKY130_PATH)
endif

time := $(shell date +%F-%H-%M)

# IMPORTANT: DESIGN_NAME must be the name of the TOP module in the design! 
ifndef DESIGN_NAME
$(error DESIGN_NAME not set, please set in order to continue)
endif

ifndef SRC_PATH
$(error SRC_PATH not set, please set in order to continue)
endif

ifndef JSON
RESULTS_DIR = ./results_dir/results_$(DESIGN_NAME)_$(time)_$(EXPERIMENT_NAME)
else
RESULTS_DIR = ./results_dir/$(JSON)/results_$(DESIGN_NAME)_$(time)_$(EXPERIMENT_NAME)
endif

synth: clean_work
	export TECH_PATH=$(TECH_PATH) && \
	export MAX_AREA=$(MAX_AREA) && \
	export DESIGN_NAME=$(DESIGN_NAME) && \
	export SRC_PATH=$(SRC_PATH) && \
	export CLK_PERIOD=$(CLK_PERIOD) && \
	export MAX_POWER=$(MAX_POWER) && \
	export MAX_FANOUT=$(MAX_FANOUT) && \
	export HDL_LANG=$(HDL_LANG) && \
	export RESULTS_DIR=$(RESULTS_DIR) && \
	mkdir $(RESULTS_DIR) && \
	dc_shell-xg-t -f synthesis.tcl | tee $(RESULTS_DIR)/synthesis_run.log

clean_work:
	@if [ -d WORK ]; then \
        echo "Deleting contents of WORK folder"; \
        rm -rf WORK/*; \
    fi
