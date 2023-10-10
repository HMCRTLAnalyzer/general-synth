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

def getTestcases(filename):
    """
        Grabs a synthesis cfg from a JSON file
    
        Input: jsonFilename (string)
        Output: Dictionary containing synthesis testcases
    """

    file = open(filename)
    
    testcases = json.load(file)

    return testcases


def writeTestcases(testcases, filepath):

    return


def runSynth(testcase):
    """
        Runs multithreaded synthesis given a testcase dictionary
    """
    # Code to decode testcase dictionary
    tech=testcase["tech"]
    language= testcase["language"]
    srcPath = testcase["srcPath"]
    designName = testcase["topModule"]
    testName = testcase["experimentName"]
    
    # synthParams decoding
    synthDict = testcase["synthParams"]
    maxPower = synthDict["maxPower"]
    maxArea = synthDict["maxArea"]
    maxFanout = synthDict["maxFanout"]
    clkPeriod = synthDict["clkPeriod"]
    
    command = 'make synth TECH={} HDL_lang={} SRC_PATH={} DESIGN_NAME={} MAX_POWER={} MAX_AREA={} MAX_FANOUT={} CLK_PERIOD={} EXPERIMENT_NAME={}'.format(tech, language, srcPath, designName, maxPower, maxArea, maxFanout, clkPeriod, testName)
    os.system(command)


def main():
    filename = args.json
    testcases = getTestcases(filename)

    # Decode testcases into list of dictionaries
    for testcase in testcases:
        runSynth(testcases[testcase])


if __name__ == "__main__":
    main()
