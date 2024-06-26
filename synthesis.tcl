# Ignore unnecessary warnings:
# intraassignment delays for nonblocking assignments are ignored
suppress_message {VER-130} 
# statements in initial blocks are ignored
suppress_message {VER-281} 
suppress_message {VER-173} 


source -echo -verbose ./library.tcl

source -echo -verbose ./set_src.tcl

source -echo -verbose ./constraints.tcl

set RESULTS_DIR $::env(RESULTS_DIR)


# Prevent assignment statements in the Verilog netlist
set_fix_multiple_port_nets -all -buffer_constants

# synthesize!
compile_ultra


redirect -file ./$RESULTS_DIR/report.qor            {report_qor}
redirect -file ./$RESULTS_DIR/report.timing         {check_timing}
redirect -file ./$RESULTS_DIR/report.constraints    {report_constraints -all_violators -verbose}
redirect -file ./$RESULTS_DIR/report.paths.max      {report_timing -path end  -delay max -max_paths 200 -nworst 2}
redirect -file ./$RESULTS_DIR/report.full_paths.max {report_timing -path full -delay max -max_paths 5   -nworst 2}
redirect -file ./$RESULTS_DIR/report.paths.min      {report_timing -path end  -delay min -max_paths 200 -nworst 2}
redirect -file ./$RESULTS_DIR/report.full_paths.min {report_timing -path full -delay min -max_paths 5   -nworst 2}
redirect -file ./$RESULTS_DIR/report.refs           {report_reference}
redirect -file ./$RESULTS_DIR/report.area           {report_area}

# generate netlists
current_design $DESIGN_NAME

change_name -rules verilog -hierarchy

# write verilog netlist
write -hierarchy -format verilog -output "./$RESULTS_DIR/$DESIGN_NAME.netlist.v"
write -hierarchy -format ddc     -output "./$RESULTS_DIR/$DESIGN_NAME.ddc"

quit