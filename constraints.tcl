##############################################################################
#                                                                            #
#                            CLOCK DEFINITION                                #
#                                                                            #
##############################################################################
set CLOCK_PERIOD $::env(CLK_PERIOD)

create_clock -name     "dco_clk"                              \
             -period   "$CLOCK_PERIOD"                        \
             -waveform "[expr $CLOCK_PERIOD/2] $CLOCK_PERIOD" \
             [get_ports dco_clk]

create_clock -name     "lfxt_clk"                             \
             -period   "$CLOCK_PERIOD"                        \
             -waveform "[expr $CLOCK_PERIOD/2] $CLOCK_PERIOD" \
             [get_ports lfxt_clk]


set_max_area $::env(MAX_AREA)

set_max_power $::env(MAX_POWER)

set_max_fanout $::env(MAX_FANOUT)
