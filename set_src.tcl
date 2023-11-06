set src_dir $::env(SRC_PATH)
set config_dir $::env(CONFIG_HEADERS_PATH)
set DESIGN_NAME $::env(DESIGN_NAME)
set RESULTS_DIR $::env(RESULTS_DIR)
set PKG_FILENAME $::env(PKG_FILENAME) 

# check for files with the correct file extension
if {$::env(HDL_LANG) == "verilog"} {
    set file_ext "*.v"
    set config_ext "*.vh"
} elseif {$::env(HDL_LANG) == "sverilog"} {
    set file_ext "*.sv"
    set config_ext "*.vh"
} else {
    set file_ext "*.vhdl"
    # VHDL does not use headers
    set config_ext "" 
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
# set src_files    [findFiles $src_dir $file_ext]
# set config_files [findFiles $config_dir "*.vh"]

# move all files to one folder to have all be at the same directory hierarchy
eval file copy -force [findFiles $config_dir $config_ext] {$RESULTS_DIR/rtl_files}
eval file copy -force [findFiles $src_dir    $file_ext]   {$RESULTS_DIR/rtl_files}

# append config and source files
set src_files [glob -directory $RESULTS_DIR/rtl_files *]

# if package is used, grab it for compile order
if {$(PKG_FILENAME) != 0} {set pkg_files $RESULTS_DIR/rtl_files/$(PKG_FILENAME)}
else {set pkg_files {}}


# append list such that packages GO FIRST!!!
set src_files [concat $pkg_files $src_files]


# svf file contains info about how DC has tranformed names
set_svf ./$RESULTS_DIR/$DESIGN_NAME.svf
define_design_lib WORK -path ./WORK
analyze -format $::env(HDL_LANG) $src_files -lib WORK

elaborate $DESIGN_NAME -lib WORK
link

# Check design structure after reading HDL
current_design $DESIGN_NAME
redirect ./$RESULTS_DIR/report.check {check_design}

