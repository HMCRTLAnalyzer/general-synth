#!/usr/bin/python3
#   -----------------------------------------   #
#   Script to generate json files for synthesis   
#   Written by Kaitlin Lucio 10/8/23
#
#   -----------------------------------------   #

# Import libraries

import json
from pprint import *

def genTestcase(name, experimentName, topModule, tech, language, srcPath, clkList, maxPower, maxArea, maxFanout, clkPeriod, extraParameters, configPath, packageName):
    # Function to generate a dictionary for a single testcase based on inputs
    testcase = {}
    testcase["name"] = name
    testcase["experimentName"] = experimentName
    testcase["topModule"] = topModule
    testcase["tech"] = tech
    testcase["language"] = language
    testcase["srcPath"] = srcPath
    testcase["clkSignalList"] = clkList
    testcase["extraParameters"] = extraParameters
    testcase["configPath"] = configPath
    testcase["packageName"] = packageName
    testcase["synthParams"] = {}
    testcase["synthParams"]["maxPower"]  = f"{maxPower}"
    testcase["synthParams"]["maxArea"]   = f"{maxArea}"
    testcase["synthParams"]["maxFanout"] = f"{maxFanout}"
    testcase["synthParams"]["clkPeriod"] = f"{clkPeriod}"
    return testcase

def main():
    testDict = {}
    """USER MODIFICATION SECTION BEGIN"""

    # Format for topmodule entry: [topModule, language, pathToSrc, [clk1, clk2, ...], configPath, packageName, ...]
    topModules = [["wallypipelinedcorewrapper", "sverilog", "../cvw/src", ["clk"], "../cvw/config", "cvw.sv"]]
    techList = ["sky130"]
    testType = "constraintSweep_wally_sweep_testinggen"
    powerList = [0]
    areaList = ["0", "80000"]
    fanoutList = ["0", "100"]
    clkPeriodList = ["1000", "500", "250", "125", "50", "10", "8.0", "7.0", "6.0", "5.0", "4.0"]
    extraParameters = ""

    """USER MODIFICATION SECTION END"""


    numTests = 0
    for topModule in topModules:
        for tech in techList:
            for maxPower in powerList:
                for maxArea in areaList:
                    for maxFanout in fanoutList:
                        for clkPeriod in clkPeriodList:
                            name = topModule[0]
                            language = topModule[1]
                            srcPath = topModule[2]
                            clkList = topModule[3]
                            configPath = topModule[4]
                            packageName =  topModule[5]
                            if packageName == "": # check for empty string in definition
                                packageName = "0" # default needs to be 0 for design compiler checking
                            if configPath == "":
                                configPath = srcPath

                            experimentName = f"{testType}_{topModule[0]}_{tech}_{maxPower}_{maxArea}_{maxFanout}_{clkPeriod}"
                            testDict[experimentName] = genTestcase(name, experimentName, topModule[0], tech, language, srcPath, clkList, maxPower, maxArea, maxFanout, clkPeriod, extraParameters, \
                                                                   configPath, packageName)
                            numTests += 1

    # Dump json file
    filepath = "./cfgs/"+testType+".json"
    with open(filepath, "w") as fp:
        json.dump(testDict, fp, indent = 4)

    print(f"generated {numTests} tests for {testType} at file {filepath}")

if __name__ == "__main__":
    main()
