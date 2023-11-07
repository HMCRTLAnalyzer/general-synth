#!/usr/bin/python3
#   -----------------------------------------   #
#   Script to perform synthesis based on a .cfg
#   file parameters
#   
#   Written by Kaitlin Lucio 9/24/23
#
#   -----------------------------------------   #

# Import libraries
import json
import subprocess
import argparse
import os
import re
import pandas
import datetime
from multiprocessing import Pool, cpu_count
from pprint import *

# Code for argparse

parser = argparse.ArgumentParser(
                    prog='run_synth',
                    description='Script to perform automated synthesis from JSON files',
                    epilog='For more info contact nlucio@hmc.edu')

parser.add_argument('json', default="./cfgs/example.json", type=str,
                    help='filepath for a json containing synthesis runs')

args = parser.parse_args()


def get_testcases(filename):
    """
        Grabs a synthesis cfg from a JSON file
    
        Input: jsonFilename (string)
        Output: Dictionary containing synthesis testcases
    """

    file = open(filename)
    
    testcases = json.load(file)

    return testcases


def run_synth(testcase, JSON_name):
    """
        Runs multithreaded synthesis given a testcase dictionary. JSONName is optional
    """
    # Code to decode testcase dictionary
    tech=testcase["tech"]
    language= testcase["language"]
    src_path = testcase["srcPath"]
    design_name = testcase["topModule"]
    experiment_name = testcase["experimentName"]
    
    # synthParams decoding
    synth_dict = testcase["synthParams"]
    max_power = synth_dict["maxPower"]
    max_area = synth_dict["maxArea"]
    max_fanout = synth_dict["maxFanout"]
    clk_period = synth_dict["clkPeriod"]
    
    command = f"make synth TECH={tech} HDL_lang={language} SRC_PATH={src_path} DESIGN_NAME={design_name} MAX_POWER={max_power} MAX_AREA={max_area} MAX_FANOUT={max_fanout} CLK_PERIOD={clk_period} EXPERIMENT_NAME={experiment_name} JSON={JSON_name}"
    os.system(command)


def get_regex_match(filepath, pattern):
    """
        Finds and returns all matches of a pattern in a text file. Only works for 1 match.

        Takes in a filepath [str] and a pattern [re.pattern, string]
    """
    matches = []
    try:
        f = open(filepath)
        for line in f:
            result = re.match(pattern, line)
            if result:
                # Add captured group to matches
                matches += [result.group(1)]
    except Exception as e:
        print(e)
    return matches


def main():
    filename = args.json
    testcases = get_testcases(filename)

    # Get current time and cast into string
    now = datetime.datetime.now()
    curr_time = now.strftime("%Y-%m-%d-%H-%M")

    # Make directory for this specific json at this specific time
    JSON_name = filename.split(".")[0]
    JSON_name = JSON_name.split("/")[1]
    JSON_name = f"{JSON_name}_{curr_time}"
    results_path = f"results_dir/{JSON_name}"
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    # Send each testcase from json to synthesis wrapper
    for testcase in testcases:
        run_synth(testcases[testcase], JSON_name)

    # Once testcases are done, get module name, experiment name, area, and delay for each testcase, then put this in a pandas DF.
    name_list = []
    for testcase in testcases:
        name_list += [[testcases[testcase]["topModule"], testcases[testcase]["experimentName"]]]

    results_dir_paths = os.listdir(results_path)

    # Patterns to capture area, total area, and timing slack
    cell_area_p = ".*Total cell area:\s*(.*)" 
    total_area_p = ".*Total area:\s*(.*)"
    test_time_p = ".*Date\s*:\s*(.*)"
    time_elapsed_p = ".*Elapsed time for this session (.*) seconds \(.*\)."
    timing_p = ".*slack\s*\(.*\)\s*(.*)"

    results_dict = {}
    results_dict["name"] = []
    results_dict["experiment"] = []
    results_dict["cell_area"] = []
    results_dict["total_area"] = []
    results_dict["slack"] = []
    results_dict["date"] = []
    results_dict["runtime"] = []

    for names in name_list:
        path_pattern = re.compile(f"results_{names[0]}_.*_{names[1]}")
        for experiment_dir in results_dir_paths:
            base_dir = f"{results_path}/{experiment_dir}"
            if re.match(path_pattern, experiment_dir):
                area_report_path = f"{base_dir}/report.area"
                timing_report_path = f"{base_dir}/report.full_paths.max"
                synth_log_path = f"{base_dir}/synthesis_run.log"
                try:
                    cell_area = get_regex_match(area_report_path, cell_area_p)
                    total_area = get_regex_match(area_report_path, total_area_p)
                    date = get_regex_match(area_report_path, test_time_p)
                    all_slacks = get_regex_match(timing_report_path, timing_p)
                    runtime = get_regex_match(synth_log_path, time_elapsed_p)
                    # Get smallest slack, convert lists to strings
                    all_slacks = [float(x) for x in all_slacks] # Cast slack numbers to float

                    min_slack = min(all_slacks)
                    cell_area = cell_area[0]
                    total_area = total_area[0]
                    date = date[0]
                    runtime = runtime[0]

                    # Add entries to dictionary
                    results_dict["name"] += [names[0]]
                    results_dict["experiment"] += [names[1]]
                    results_dict["cell_area"] += [cell_area]
                    results_dict["total_area"] += [total_area]
                    results_dict["slack"] += [min_slack]
                    results_dict["runtime"] += [runtime]
                    results_dict["date"] += [date]
                except Exception as e:
                    print(e)

    # Put captured statistics into dataframe and save to CSV file
    csv_frame = pandas.DataFrame(results_dict)

    csv_frame.to_csv(f"{results_path}/results_{curr_time}.csv", index=False)



                

        


if __name__ == "__main__":
    main()
