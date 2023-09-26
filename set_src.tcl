set src_dir $::env(SRC_PATH)
set DESIGN_NAME $::env(DESIGN_NAME)
set RESULTS_DIR $::env(RESULTS_DIR)

# check for files with the correct file extension
if {$::env(HDL_LANG) == "verilog"} {
    set file_ext "*.v"
} elseif {$::env(HDL_LANG) == "sverilog"} {
    set file_ext "*.sv"
} else {
    set file_ext "*.vhdl"
}

# put all files ending in file_ext in the src_files variable
set src_files [glob -directory $src_dir $file_ext]

# svf file contains info about how DC has tranformed names
set_svf ./$RESULTS_DIR/$DESIGN_NAME.svf
define_design_lib WORK -path ./WORK
analyze -format $::env(HDL_LANG) $src_files

elaborate $DESIGN_NAME
link

# Check design structure after reading HDL
current_design $DESIGN_NAME
redirect ./$RESULTS_DIR/report.check {check_design}

