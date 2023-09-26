##############################################################################
#                                                                            #
#                            SPECIFY LIBRARIES                               #
#                                                                            #
##############################################################################

# Define worst case library
set LIB_WC_FILE   /opt/riscv/cad/lib/sky130_osu_sc_t12/12T_hs/lib/sky130_osu_sc_12T_hs_tt_1P20_25C.ccs.db 

# Define best case library
set LIB_BC_FILE   /opt/riscv/cad/lib/sky130_osu_sc_t12/12T_hs/lib/sky130_osu_sc_12T_hs_tt_1P20_25C.ccs.db 

# Set library
set target_library $LIB_WC_FILE
set link_library   $LIB_WC_FILE
set_min_library    $LIB_WC_FILE  -min_version $LIB_BC_FILE
