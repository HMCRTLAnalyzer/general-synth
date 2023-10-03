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

# findFiles, from https://stackoverflow.com/questions/429386/tcl-recursively-search-subdirectories-to-source-all-tcl-files
# basedir - the directory to start looking in
# pattern - A pattern, as defined by the glob command, that the files must match
proc findFiles { basedir pattern } {

    # Fix the directory name, this ensures the directory name is in the
    # native format for the platform and contains a final directory seperator
    set basedir [string trimright [file join [file normalize $basedir] { }]]
    set fileList {}

    # Look in the current directory for matching files, -type {f r}
    # means ony readable normal files are looked at, -nocomplain stops
    # an error being thrown if the returned list is empty
    foreach fileName [glob -nocomplain -type {f r} -path $basedir $pattern] {
        lappend fileList $fileName
    }

    # Now look for any sub direcories in the current directory
    foreach dirName [glob -nocomplain -type {d  r} -path $basedir *] {
        # Recusively call the routine on the sub directory and append any
        # new files to the results
        set subDirList [findFiles $dirName $pattern]
        if { [llength $subDirList] > 0 } {
            foreach subDirFile $subDirList {
                lappend fileList $subDirFile
            }
        }
    }
    return $fileList
 }



# put all files ending in file_ext in the src_files variable
set src_files [findFiles $src_dir $file_ext]

# svf file contains info about how DC has tranformed names
set_svf ./$RESULTS_DIR/$DESIGN_NAME.svf
define_design_lib WORK -path ./WORK
analyze -format $::env(HDL_LANG) $src_files

elaborate $DESIGN_NAME
link

# Check design structure after reading HDL
current_design $DESIGN_NAME
redirect ./$RESULTS_DIR/report.check {check_design}

