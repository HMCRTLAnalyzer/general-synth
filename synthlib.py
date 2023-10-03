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
from multiprocessing import Pool, cpu_count
from pprint import *

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
    subprocess.Popen(command,shell=True)


def main():
    filename = './cfgs/example.json'
        
    testcases = getTestcases(filename)

    # Decode testcases into list of dictionaries
    testList = []
    for testcase in testcases:
        testList += [testcases[testcase]]
    
    pprint(testList)

    pool = Pool(processes=25)
    pool.map(runSynth, testList)
    pool.close()


if __name__ == "__main__":
    main()
