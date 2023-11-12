##############################################################################
#                                                                            #
#                            CLOCK DEFINITION                                #
#                                                                            #
##############################################################################
set CLOCK_PERIOD $::env(CLK_PERIOD)

# this structure is required for all clock signals in the design. 
create_clock -name     "clk"                              \
             -period   "$CLOCK_PERIOD"                        \
             -waveform "[expr $CLOCK_PERIOD/2] $CLOCK_PERIOD" \
             [get_ports clk]


set_max_area $::env(MAX_AREA)

set_max_power $::env(MAX_POWER)

set_max_fanout $::env(MAX_FANOUT)

