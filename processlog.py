import os
import pycosat
from scipy.stats import rankdata

currentDirectory = os.path.dirname(__file__)

def post_process_log(index, dataPath):
    solutionFilePath = os.path.relpath(dataPath + "solutions_" + str(int(index)) + ".log", currentDirectory)
    statisticsFilePath = os.path.relpath(dataPath + "statistics_" + str(int(index)) + ".log", currentDirectory)
    solutionFile = open(solutionFilePath, "w")
    statisticsFile = open(statisticsFilePath, "w")
    statisticsFile.write("\n")
    runLogPath = os.path.relpath(dataPath + "run_" + str(int(index)) + ".log", currentDirectory)
    f = open(runLogPath, "r")
    for line in f:
        strippedLine = line.rstrip("\n")
        if len(strippedLine) > 10 and len(strippedLine.split(",")[0]) > 4:
            if(strippedLine == "=============================="):
                statisticsFile.write("\n")
            elif(strippedLine == "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"):
                solutionFile.write("\n")
            else:
                if len(strippedLine) == 81:
                    solutionFile.write(strippedLine + "\n")
                else:
                    statisticsFile.write(strippedLine)
    f.close()
    solutionFile.write("\n")
    solutionFile.close()
    statisticsFile.close()
    process_statistics(index, dataPath)

def process_statistics(index, dataPath):
    statisticsLogPath = os.path.relpath(dataPath + "statistics_" + str(int(index)) + ".log", currentDirectory)
    consolidatedStatisticsFilePath = os.path.relpath(dataPath + "consolidated_statistics_" + str(int(index)) + ".log", currentDirectory)
    f = open(statisticsLogPath, "r")
    consolidatedStatisticsFile = open(consolidatedStatisticsFilePath, "w")
    for line in f:
        strippedLine = line.rstrip("\n")
        if len(strippedLine) > 0:
            reports = strippedLine.split("------------------------------")
            numberOfSatisfiableSolutions = 0
            numberOfUnsatisfiableSolutions = 0
            stats = [[0 for x in range(len(reports) - 1)] for y in range(12)]
            for (reportIndex, report) in enumerate(reports):
                if len(report) == 0:
                    consolidatedStatisticsFile.write("\n")
                else:
                    satvalStats = report.split(" ")
                    for satvalStat in satvalStats:
                        if len(satvalStat) > 2:
                            for (statIndex, stat) in enumerate(satvalStat.split(",")):
                                stats[statIndex][reportIndex] = float(stat)
                        else:
                            if satvalStat == "0":
                                numberOfUnsatisfiableSolutions += 1
                            elif satvalStat == "1":
                                numberOfSatisfiableSolutions += 1
            derivedStats = (
                numberOfSatisfiableSolutions,
                numberOfUnsatisfiableSolutions,
                str(round(sum(stats[0])/float(len(stats[0])), 2)),#average_seconds
                min(stats[0]),#minimum_seconds
                max(stats[0]),#maximum_seconds
                str(round(sum(stats[1])/float(len(stats[1])), 2)),#average_variables
                min(stats[1]),#minimum_variables
                max(stats[1]),#maximum_variables
                str(round(sum(stats[2])/float(len(stats[2])), 2)),#average_usage
                min(stats[2]),#minimum_usage
                max(stats[2]),#maximum_usage
                str(round(sum(stats[3])/float(len(stats[3])), 2)),#average_original
                min(stats[3]),#minimum_original
                max(stats[3]),#maximum_original
                str(round(sum(stats[4])/float(len(stats[4])), 2)),#average_conflicts
                min(stats[4]),#minimum_conflicts
                max(stats[4]),#maximum_conflicts
                str(round(sum(stats[5])/float(len(stats[5])), 2)),#average_learned
                min(stats[5]),#minimum_learned
                max(stats[5]),#maximum_learned
                str(round(sum(stats[6])/float(len(stats[6])), 2)),#average_limit
                min(stats[6]),#minimum_limit
                max(stats[6]),#maximum_limit
                str(round(sum(stats[7])/float(len(stats[7])), 2)),#average_agility
                min(stats[7]),#minimum_agility
                max(stats[7]),#maximum_agility
                str(round(sum(stats[8])/float(len(stats[8])), 2)),#average_memory
                min(stats[8]),#minimum_memory
                max(stats[8]),#maximum_memory
                str(round(sum(stats[9])/float(len(stats[9])), 2)),#average_decisions
                min(stats[9]),#minimum_decisions
                max(stats[9]),#maximum_decisions
                str(round(sum(stats[10])/float(len(stats[10])), 2)),#average_conflict_decisions_ratio
                min(stats[10]),#minimum_conflict_decisions_ratio
                max(stats[10])#maximum_conflict_decisions_ratio
            )
            consolidatedStatisticsFile.write(",".join(str(stat) for stat in derivedStats))
    f.close()
    consolidatedStatisticsFile.write("\n")
    consolidatedStatisticsFile.close()
    normalize_statistics(index, dataPath)

def normalize_statistics(index, dataPath):
    consolidatedStatisticsFilePath = os.path.relpath(dataPath + "consolidated_statistics_" + str(int(index)) + ".log", currentDirectory)
    consolidatedStatisticsFile = open(consolidatedStatisticsFilePath, "r")
    consolidatedStatisticsNormalizedFilePath = os.path.relpath(dataPath + "consolidated_statistics_normalized_" + str(int(index)) + ".log", currentDirectory)
    consolidatedStatisticsNormalizedFile = open(consolidatedStatisticsNormalizedFilePath, "w")
    consolidatedStatisticsNormalizedFile.write("\n")
    medianStats = [0 for x in range(36)]
    minimumStats = [float("inf") for y in range(36)]
    maximumStats = [float("-inf") for z in range(36)]
    for (lineIndex, line) in enumerate(consolidatedStatisticsFile):
        strippedLine = line.rstrip("\n")
        stats = strippedLine.split(",")
        if len(strippedLine) > 0:
            for (statIndex, stat) in enumerate(stats):
                if lineIndex == 1:
                    medianStats[statIndex] = float(stat)
                if minimumStats[statIndex] > float(stat):
                    minimumStats[statIndex] = float(stat)
                if maximumStats[statIndex] < float(stat):
                    maximumStats[statIndex] = float(stat)
    consolidatedStatisticsFile.seek(0)
    for line in consolidatedStatisticsFile:
        strippedLine = line.rstrip("\n")
        stats = strippedLine.split(",")
        if len(strippedLine) > 0:
            for (statIndex, stat) in enumerate(stats):
                if (maximumStats[statIndex] - minimumStats[statIndex]) > 0:
                    consolidatedStatisticsNormalizedFile.write("%0.2f" % ((float(stat) - medianStats[statIndex])/(maximumStats[statIndex] - minimumStats[statIndex])))
                else:
                    consolidatedStatisticsNormalizedFile.write("0")
                if statIndex < len(stats) - 1:
                    consolidatedStatisticsNormalizedFile.write(",")
            consolidatedStatisticsNormalizedFile.write("\n")
    consolidatedStatisticsNormalizedFile.close()
    consolidatedStatisticsFile.close()
    calculate_rank(index, dataPath)

def calculate_rank(index, dataPath):
    consolidatedStatisticsNormalizedFilePath = os.path.relpath(dataPath + "consolidated_statistics_normalized_" + str(int(index)) + ".log", currentDirectory)
    consolidatedStatisticsNormalizedFile = open(consolidatedStatisticsNormalizedFilePath, "r")
    weights = [1 for x in range(36)]
    rankMeasures = []
    for (lineIndex, line) in enumerate(consolidatedStatisticsNormalizedFile):
        strippedLine = line.rstrip("\n")
        if len(strippedLine) > 0:
            stats = strippedLine.split(",")
            rankMeasure = 0
            for (statIndex, stat) in enumerate(stats):
                rankMeasure += (float(stat) * weights[statIndex])
            rankMeasures.append(rankMeasure)
    ranks = rankdata(rankMeasures, method="min")
    rankDensity = rankdata(rankMeasures, method="dense")
    rankFilePath = os.path.relpath(dataPath + "rank_" + str(int(index)) + ".log", currentDirectory)
    rankFile = open(rankFilePath, "r+")
    rankString = ""
    for (lineNumber, line) in enumerate(rankFile):
        strippedLine = line.rstrip("\n")
        rankString += strippedLine + "," + str(ranks[lineNumber]) + "," + str(rankDensity[lineNumber]) + "\n"
    rankFile.seek(0)
    rankFile.write(rankString)
    rankFile.close()
    consolidatedStatisticsNormalizedFile.close()
