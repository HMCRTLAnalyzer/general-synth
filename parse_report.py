#!/usr/bin/python3

#to use: change the "results_folder" name to be the report folder you want to extract features from.
#run file

import re
import pandas
import datetime
import os

results_folder = "constraintSweep_openMSP430_2023-11-15-09-48"
results_dir = f"./results_dir/{results_folder}"
sub_dir = next(os.walk(results_dir))[1]


pattern_dict = {}
#general info
pattern_dict["synth_runtime"] = [".*Overall Compile Wall Clock Time:\s*(.*)"]

#timing info
pattern_dict["period"] = [".*Critical Path Clk Period:\s*(.*)"]
pattern_dict["logic_levels"] = [".*Levels of Logic:\s*(.*)"]
pattern_dict["crit_path"] = [".*Critical Path Length:\s*(.*)"]
pattern_dict["total_neg_slack"] = [".*Total Negative Slack:\s*(.*)"]

#area
pattern_dict["combo_area"] = [".*Combinational Area:\s*(.*)"]
pattern_dict["noncombo_area"] = [".*Noncombinational Area:\s*(.*)"]
pattern_dict["design_area"] = [".*Design Area:\s*(.*)"]

# cell count
pattern_dict["cell_count"] = [".*Leaf Cell Count:\s*(.*)"]
pattern_dict["combinational_cell_count"] = [".*Combinational Cell Count:\s*(.*)"]
pattern_dict["seqential_cell_count"] = [".*Sequential Cell Count:\s*(.*)"]

results_dict = {}
#general info
results_dict["name"] = []
results_dict["synth_runtime"] = []

#timing info
results_dict["period"] =[]
results_dict["logic_levels"] = []
results_dict["crit_path"] = []
results_dict["total_neg_slack"] = []

#area
results_dict["combo_area"] = []
results_dict["noncombo_area"] = []
results_dict["design_area"] = []

# cell count
results_dict["cell_count"] = []
results_dict["combinational_cell_count"] = []
results_dict["seqential_cell_count"] = []

for experiment in sub_dir:
    qor_path = f"{results_dir}/{experiment}/report.qor"
    f = open(qor_path)
    f_str = f.read()
    results_dict["name"] += [experiment]
    for pattern in pattern_dict:
        matches = re.finditer(pattern_dict[pattern][0], f_str, re.MULTILINE)
        for match in matches:
            results_dict[pattern] += [(match.group(1))]
csv_frame = pandas.DataFrame(results_dict)
csv_frame.to_csv(f"{results_dir}/results_{datetime.datetime.now()}.csv", index=False)
print(f"Created CSV at {results_dir}/results_{datetime.datetime.now()}.csv")
