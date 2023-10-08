#!/usr/bin/python3
#   -----------------------------------------   #
#   Script to generate json files for synthesis   
#   Written by Kaitlin Lucio 10/8/23
#
#   -----------------------------------------   #

# Import libraries

import json
from pprint import *

def genTestcase(name, experimentName, topModule, tech, language, srcPath, maxPower, maxArea, maxFanout, clkPeriod, extraParameters):
    # Function to generate a dictionary for a single testcase based on inputs
    testcase = {}
    testcase["name"] = name
    testcase["experimentName"] = experimentName
    testcase["topModule"] = topModule
    testcase["tech"] = tech
    testcase["language"] = language
    testcase["srcPath"] = srcPath
    testcase["extraParameters"] = extraParameters
    testcase["synthParams"] = {}
    testcase["synthParams"]["maxPower"]  = maxPower
    testcase["synthParams"]["maxArea"]   = maxArea
    testcase["synthParams"]["maxFanout"] = maxFanout
    testcase["synthParams"]["clkPeriod"] = clkPeriod
    return testcase

def main():
    testDict = {}
    topModules = [["openMSP430", "Verilog", "./RTL/opencores-ip/core/rtl/verilog"]]
    techList = ["sky130"]
    testType = "constraintSweep"
    powerList = ["0", "100", "1000", "10000"]
    areaList = ["0", "100", "1000", "10000"]
    fanoutList = ["0", "100", "1000", "10000"]
    clkPeriodList = ["6000", "4000", "2000", "1000", "500", "250", "125"]
    extraParameters = ""
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
                            experimentName = testType+"_"+str(topModule[0])+"_"+str(tech)+"_"+str(maxPower)+"_"+str(maxArea)+"_"+str(maxFanout)+"_"+str(clkPeriod)
                            testDict[experimentName] = genTestcase(name, experimentName, topModule[0], tech, language, srcPath, maxPower, maxArea, maxFanout, clkPeriod, extraParameters)
                            numTests += 1

    # Dump json file
    filepath = "./cfgs/"+testType+".json"
    with open(filepath, "w") as fp:
        json.dump(testDict, fp, indent = 4)

    print("generated "+str(numTests)+" tests for "+testType+" at file "+filepath)

if __name__ == "__main__":
    main()
