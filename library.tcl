##############################################################################
#                                                                            #
#                            SPECIFY LIBRARIES                               #
#                                                                            #
##############################################################################

# Define worst case library
set LIB_WC_FILE   /opt/riscv/cad/lib/sky130_osu_sc_t12/12T_hs/lib/sky130_osu_sc_12T_hs_tt_1P20_25C.ccs.db 
set LIB_WC_NAME   "<YOUR SLOW LIBRARY DB FILE>:<YOUR SLOW LIBRARY NAME>"

# Define best case library
set LIB_BC_FILE   /opt/riscv/cad/lib/sky130_osu_sc_t12/12T_hs/lib/sky130_osu_sc_12T_hs_tt_1P20_25C.ccs.db 
set LIB_BC_NAME   "<YOUR FAST LIBRARY DB FILE>:<YOUR FAST LIBRARY NAME>"

# Define operating conditions
set LIB_WC_OPCON  "<YOUR SLOW OPERATING CONDITION>"
set LIB_BC_OPCON  "<YOUR FAST OPERATING CONDITION>"

# Define wire-load model
set LIB_WIRE_LOAD "<YOUR WIRE LOAD MODEL>"

# Define nand2 gate name for aera size calculation
set NAND2_NAME    "<YOUR LIBRARY NAND2 GATE NAME>"


# Set library
set target_library $LIB_WC_FILE
set link_library   $LIB_WC_FILE
set_min_library    $LIB_WC_FILE  -min_version $LIB_BC_FILE
