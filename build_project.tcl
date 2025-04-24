# build_project.tcl - FPGA Flow Simulator with CLI options

proc run_clean {} {
    puts "Cleaning reports..."
    file delete -force ./reports/*
    puts "Reports cleaned."
}

proc run_synthesis {} {
    puts "Running synthesis..."
    file copy -force ./logs/synthesis.log ./reports/synthesis_result.log
    puts "Synthesis complete."
}

proc run_implementation {} {
    puts "Running implementation..."
    file copy -force ./logs/implementation.log ./reports/implementation_result.log
    puts "Implementation complete."
}

proc generate_bitstream {} {
    set bitfile "./reports/fake_bitstream.bit"
    set f [open $bitfile w]
    puts $f "This is a simulated bitstream file."
    close $f
    puts "Bitstream written to: $bitfile"
}

proc summarize_logs {} {
    set synth_log "./reports/synthesis_result.log"
    set impl_log "./reports/implementation_result.log"
    set summary_file "./reports/build_summary.txt"

    set errors 0
    set warnings 0
    set luts_used "N/A"
    set ffs_used "N/A"

    # Parse synthesis log
    if {[file exists $synth_log]} {
        set f [open $synth_log r]
        while {[gets $f line] >= 0} {
            if {[string match "*ERROR*" $line]} { incr errors }
            if {[string match "*WARNING*" $line]} { incr warnings }
        }
        close $f
    }

    # Parse implementation log
    if {[file exists $impl_log]} {
        set f [open $impl_log r]
        while {[gets $f line] >= 0} {
            if {[regexp {LUTs used: ([0-9]+)} $line -> match]} {
                set luts_used $match
            }
            if {[regexp {FFs used: ([0-9]+)} $line -> match]} {
                set ffs_used $match
            }
        }
        close $f
    }

    # Write summary
    set f [open $summary_file w]
    puts $f "Build Summary Report"
    puts $f "--------------------"
    puts $f "Synthesis Errors: $errors"
    puts $f "Synthesis Warnings: $warnings"
    puts $f "LUTs Used: $luts_used"
    puts $f "FFs Used: $ffs_used"
    close $f

    puts "Summary written to: $summary_file"
}


proc run_full {} {
    puts "Starting full build flow..."

    # Load sources
    puts ""
    puts "Finding VHDL source files..."
    set sources [glob ./sources/*.vhdl]
    foreach src $sources {
        puts "Loaded: $src"
    }

    # Load constraints
    set xdc_file "./constraints/constraints.xdc"
    if {[file exists $xdc_file]} {
        puts ""
        puts "Constraint file loaded: $xdc_file"
    } else {
        puts ""
        puts "Constraint file NOT found"
    }

    run_synthesis
    run_implementation
    generate_bitstream
    puts ""
    puts "Build simulation complete"

    summarize_logs
}

# Parse CLI args
set arg [lindex $argv 0]

if {$argc == 0 || $arg == "--full"} {
    run_full

} elseif {$arg == "--clean"} {
    run_clean

} elseif {$arg == "--bitstream-only"} {
    generate_bitstream

} elseif {$arg == "--simulate"} {
    if {$argc < 2} {
        puts "Usage: tclsh build_project.tcl --simulate <module_name>"
        exit
    }
    set file [lindex $argv 1]
    exec python sim/simulate.py --file sources/$file.vhdl

} elseif {$arg == "--simulate-all"} {
    set vhdl_files [glob -nocomplain sources/*.vhdl]
    file delete -force reports/simulation_output.txt
    foreach vfile $vhdl_files {
        set module_name [file rootname [file tail $vfile]]
        set test_file "tests/${module_name}_tests.json"
        if {[file exists $test_file]} {
            puts "Simulating $module_name..."
            exec python sim/simulate.py --file sources/${module_name}.vhdl
        } else {
            puts "Skipping $module_name (no test file found)"
        }
    }
    puts "All simulations complete."

} else {
    puts "Unknown command: $arg"
    puts "Usage:"
    puts "  tclsh build_project.tcl --full"
    puts "  tclsh build_project.tcl --clean"
    puts "  tclsh build_project.tcl --bitstream-only"
    puts "  tclsh build_project.tcl --simulate <module_name>"
    puts "  tclsh build_project.tcl --simulate-all"
}
