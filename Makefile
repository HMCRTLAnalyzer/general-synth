# ---------------- CONFIG -----------------------
export SKY130_PATH := /opt/riscv/cad/lib/sky130_osu_sc_t12/12T_hs/lib/sky130_osu_sc_12T_hs_tt_1P20_25C.ccs.db
export TECH ?= sky130
export MAX_AREA ?= 0.0
export MAX_POWER ?= 0.0
export MAX_FANOUT ?= 0
# HDL_LANG option is either verilog, sverilog, or vhdl. default to verilog unless set otherwise
export HDL_LANG ?= verilog
export EXPERIMENT_NAME ?= test
export CONFIG_HEADERS_PATH ?= $(SRC_PATH)
export PKG_FILENAME ?= 0

# CLK_PERIOD is in nanoseconds
export CLK_PERIOD ?= 100.0

# if make is called with TECH=sky130, set the tech path
ifeq ($(TECH), sky130)
	export TECH_PATH = $(SKY130_PATH)
endif

time := $(shell date +%F-%H-%M)

# IMPORTANT: DESIGN_NAME must be the name of the TOP module in the design! 
ifndef DESIGN_NAME
$(error DESIGN_NAME not set, please set in order to continue)
endif
export DESIGN_NAME

ifndef SRC_PATH
$(error SRC_PATH not set, please set in order to continue)
endif
export SRC_PATH


export RESULTS_DIR = ./results_dir/results_$(DESIGN_NAME)_$(time)_$(EXPERIMENT_NAME)

synth: 
	mkdir $(RESULTS_DIR) && \
	mkdir $(RESULTS_DIR)/rtl_files && \
	dc_shell-xg-t -64bit -f synthesis.tcl | tee $(RESULTS_DIR)/synthesis_run.log

clean_work:
	@if [ -d WORK ]; then \
        echo "Deleting contents of WORK folder"; \
        rm -rf WORK/*; \
    fi
