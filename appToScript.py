def openFiles(fileName):
	global file
	file = open(fileName, "r")

def appendFile(readFile):
	appendedFile = open(readFile, "r")
	readOn = True
	while readOn:
		string = appendedFile.readline()
		if string[-1:] == "\n":
			allFile.write(string)
		else:
			allFile.write(string + "\n")
			readOn = False

def oneTeamOneMatch():
	global read 
	lines = []
	for i in range(20): #lines 0-19
		string = file.readline()
		if string[-1:] == "\n":
			lines.append(string[:-1])
		else:
			lines.append(string)
			read = False

	match = {} #dictionary; order might not be guaranteed (not the same when printed)
	#reading the file and putting into dictionary, and i'm kinda stupid too
	for i in range(0, 2):
		match[lines[i].split(",")[0]] = [int(s) for s in lines[i].split() if s.isdigit()]
	for i in range(2, 4):
		match[lines[i].split(",")[0]] = lines[i].split(", ", 1)[1]
	for i in range(4, 8):
		match[lines[i].split(",")[0]] = [int(s) for s in lines[i].split() if s.isdigit()]
	highStrings = (lines[8].split(",")[1]).split("-")
	match[lines[8].split(",")[0]] = []
	for j in range(len(highStrings)):
		highNum = [int(s) for s in highStrings[j].split() if s.isdigit()]
		for num in highNum:
			match[lines[8].split(",")[0]].append(num)
	for i in range(9, 10):
		match[lines[i].split(",")[0]] = [int(s) for s in lines[i].split() if s.isdigit()]
	lowStrings = (lines[10].split(",")[1]).split("-")
	match[lines[10].split(",")[0]] = []
	for j in range(len(lowStrings)):
		lowNum = [int(s) for s in lowStrings[j].split() if s.isdigit()]
		for num in lowNum:
			match[lines[10].split(",")[0]].append(num)
	for i in range(11, 12):
		match[lines[i].split(",")[0]] = [int(s) for s in lines[i].split() if s.isdigit()]
	for i in range(12, 13):
		match[lines[i].split(",")[0]] = lines[i].split(", ", 1)[1]
	for i in range(13, 15):
		match[lines[i].split(",")[0]] = [int(s) for s in lines[i].split() if s.isdigit()]
	for i in range(15, 16):
		match[lines[i].split(",")[0]] = lines[i].split(", ", 1)[1]
	for i in range(16, 18):
		match[lines[i].split(",")[0]] = [int(s) for s in lines[i].split() if s.isdigit()]
	for i in range(18, 20):
		match[lines[i].split(",")[0]] = lines[i].split(", ", 1)[1]

	autoGearsMade = 0
	for i in match["Auto Gears"]:
		if i == 1: autoGearsMade += 1
	match["Auto Gears Ratio"] = str(autoGearsMade) + "/" + str(len(match["Auto Gears"]))

	teleopGearsMade = 0
	for i in match["Teleop Gears"]:
		if i == 1: teleopGearsMade += 1
	match["Teleop Gears Ratio"] = str(teleopGearsMade) + "/" + str(len(match["Teleop Gears"]))

	highGoalScores = 0
	for i in range(len(match["Teleop High Goal Shots Per Cycle"])):
		highGoalScores += match["Teleop High Goal Shots Per Cycle"][i]
	match["Teleop High Goal Total Shots"] = highGoalScores

	lowGoalScores = 0
	for i in range(len(match["Teleop Low Goal Shots Per Cycle"])):
		lowGoalScores += match["Teleop Low Goal Shots Per Cycle"][i]
	match["Teleop Low Goal Total Shots"] = lowGoalScores

	match["Teleop High Goal Total Cycles"] = len(match["Teleop High Goal Shots Per Cycle"])
	match["Teleop Low Goal Total Cycles"] = len(match["Teleop Low Goal Shots Per Cycle"])

	for i in range(len(match["Teleop High Goal Shots Cycle Time"])):
		if i % 2 == 0:
			first = match["Teleop High Goal Shots Cycle Time"][i]
			second = match["Teleop High Goal Shots Cycle Time"][i + 1]
			match["Teleop High Goal Shots Cycle Time"][i / 2] = [first, second]
	halfLength = (len(match["Teleop High Goal Shots Cycle Time"]) / 2)
	for i in range(halfLength):
		match["Teleop High Goal Shots Cycle Time"].pop(halfLength)

	for i in range(len(match["Teleop Low Goal Shots Cycle Time"])):
		if i % 2 == 0:
			first = match["Teleop Low Goal Shots Cycle Time"][i]
			second = match["Teleop Low Goal Shots Cycle Time"][i + 1]
			match["Teleop Low Goal Shots Cycle Time"][i / 2] = [first, second]
	halfLength = (len(match["Teleop Low Goal Shots Cycle Time"]) / 2)
	for i in range(halfLength):
		match["Teleop Low Goal Shots Cycle Time"].pop(halfLength)

	singleRobotPoints = 0
	if match["Cross Baseline"] == "Yes": singleRobotPoints += 5
	if len(match["Auto High Goal"]) != 0: singleRobotPoints += match["Auto High Goal"][0]
	if len(match["Auto Low Goal"]) != 0: singleRobotPoints += ((match["Auto Low Goal"][0]) / 3)
	singleRobotPoints += ((match["Teleop High Goal Total Shots"]) / 3)
	singleRobotPoints += ((match["Teleop Low Goal Total Shots"]) / 9)
	#gears required for each rotor: 1, 2, 4, 6; auto rotor turning: 60, teleop rotor turning: 40
	totalGearsMade = autoGearsMade + teleopGearsMade
	multiplyFactor = 0
	if totalGearsMade >= 1 and totalGearsMade < 3: multiplyFactor = 1
	elif totalGearsMade >= 3 and totalGearsMade < 7: multiplyFactor = 2
	elif totalGearsMade >= 7 and totalGearsMade < 13: multiplyFactor = 3
	elif totalGearsMade == 13: multiplyFactor = 4
	singleRobotPoints += multiplyFactor * 40
	addFactor = 0
	if autoGearsMade >= 1 and autoGearsMade < 3: addFactor = 1
	elif autoGearsMade >= 3 and autoGearsMade < 7: addFactor = 2
	elif autoGearsMade >= 7 and autoGearsMade < 13: addFactor = 3
	elif autoGearsMade == 13: addFactor = 4
	singleRobotPoints += addFactor * 20
	if match["Takeoff"] == "Yes": singleRobotPoints += 50
	match["Estimated Single Robot Points"] = singleRobotPoints

	return match

def sortByTeam(allMatches):
	team = []
	teamNumber = allMatches[0]["Team Number"]
	i = 0
	while i < len(allMatches): #make sure index doesn't go out of bounds
		if allMatches[i]["Team Number"] == teamNumber:
			team.append(allMatches[i])
			del(allMatches[i])
			i -= 1
		i += 1
	return team

def generateOneFile():
	global allFile
	allFile = open("oneFile.txt", "a") #append to end of file
	appendFile("r1.txt")
	appendFile("r2.txt")
	appendFile("r3.txt")
	appendFile("b1.txt")
	appendFile("b2.txt")
	readOn = True
	appendedFile = open("b3.txt", "r") #don't want \n at end of this
	while readOn:
		string = appendedFile.readline()
		if string[-1:] == "\n":
			allFile.write(string)
		else:
			allFile.write(string)
			readOn = False

def orderByMatchNumber(oldTeams):
	teams = {}
	for key in oldTeams:
		matches = getMatchesArray(oldTeams, key)
		indices = range(len(oldTeams[key]))
		bubbleSortLowToHigh(matches, indices)
		teams[key] = []
		for i in range(len(indices)):
			teams[key].append(oldTeams[key][indices[i]])
	return teams

def generateDict(fileName):
	global read
	openFiles(fileName)
	read = True
	matches = [] #append all 6 textfiles and read
	while read: #text file names: r1.txt, r2.txt, r3.txt, b1.txt, b2.txt, b3.txt
		matches.append(oneTeamOneMatch())
	unsortedTeams = {}
	i = 0
	while len(matches) > 0:
		team = sortByTeam(matches)
		num = str(team[0]["Team Number"][0])
		unsortedTeams[num] = team
	teams = orderByMatchNumber(unsortedTeams)
	return teams

def getMatchesArray(teams, teamNumber):
	matches = []
	for i in range(len(teams[teamNumber])):
		matches.append(teams[teamNumber][i]["Match Number"][0])
	return matches

def generateTeamOverall(teams):
	teamOverall = {} #dictionary to be returned
	global highCycleTimeLow #for rankings
	highCycleTimeLow = {}
	global lowCycleTimeLow
	lowCycleTimeLow = {}
	for key in teams:
		autoBaseline = 0
		autoHighGoals = 0
		autoLowGoals = 0
		autoGearsMade = 0
		autoGearsTried = 0
		teleopTotalHighGoalCycles = 0
		teleopTotalHighGoalCycleTimeLow = 0
		teleopTotalHighGoalCycleTimeHigh = 0
		teleopTotalHighGoals = 0
		teleopTotalLowGoalCycles = 0
		teleopTotalLowGoalCycleTimeLow = 0
		teleopTotalLowGoalCycleTimeHigh = 0
		teleopTotalLowGoals = 0
		teleopGearsMade = 0
		teleopGearsTried = 0
		totalPressure = 0
		totalReach40kPa = 0
		totalRotorsTurning = 0
		totalTakeoffs = 0
		totalAlliancePoints = 0
		totalSingleRobotPoints = 0
		totalRankingPoints = 0
		totalWins = 0
		teamOverall[key] = {} #dictionary in each key of teamOverall
		teamOverall[key]["Matches"] = []
		for i in range(len(teams[key])): #go through each match for each team
			teamOverall[key]["Matches"].append(teams[key][i]["Match Number"][0])
			if teams[key][i]["Cross Baseline"] == "Yes": autoBaseline += 1
			if len(teams[key][i]["Auto High Goal"]) != 0: autoHighGoals += teams[key][i]["Auto High Goal"][0]
			if len(teams[key][i]["Auto Low Goal"]) != 0: autoLowGoals += teams[key][i]["Auto Low Goal"][0]
			autoGearsMade += int(teams[key][i]["Auto Gears Ratio"].split("/", 1)[0])
			autoGearsTried += int(teams[key][i]["Auto Gears Ratio"].split("/", 1)[1])
			teleopTotalHighGoalCycles += teams[key][i]["Teleop High Goal Total Cycles"]
			for j in range(len(teams[key][i]["Teleop High Goal Shots Cycle Time"])):
				teleopTotalHighGoalCycleTimeLow += teams[key][i]["Teleop High Goal Shots Cycle Time"][j][0]
				teleopTotalHighGoalCycleTimeHigh += teams[key][i]["Teleop High Goal Shots Cycle Time"][j][1]
			teleopTotalHighGoals += teams[key][i]["Teleop High Goal Total Shots"]
			teleopTotalLowGoalCycles += teams[key][i]["Teleop Low Goal Total Cycles"]
			for j in range(len(teams[key][i]["Teleop Low Goal Shots Cycle Time"])):
				teleopTotalLowGoalCycleTimeLow += teams[key][i]["Teleop Low Goal Shots Cycle Time"][j][0]
				teleopTotalLowGoalCycleTimeHigh += teams[key][i]["Teleop Low Goal Shots Cycle Time"][j][1]
			teleopTotalLowGoals += teams[key][i]["Teleop Low Goal Total Shots"]
			teleopGearsMade += int(teams[key][i]["Teleop Gears Ratio"].split("/", 1)[0])
			teleopGearsTried += int(teams[key][i]["Teleop Gears Ratio"].split("/", 1)[1])
			totalPressure += teams[key][i]["Total Pressure"][0]
			if teams[key][i]["Reached 40 kPa"] == "Yes": totalReach40kPa += 1
			totalRotorsTurning += teams[key][i]["Rotors Turning"][0]
			if teams[key][i]["Takeoff"] == "Yes": totalTakeoffs += 1
			totalAlliancePoints += teams[key][i]["Total Points"][0]
			totalSingleRobotPoints += teams[key][i]["Estimated Single Robot Points"]
			totalRankingPoints += teams[key][i]["Ranking Points"][0]
			if teams[key][i]["Result"] == "Win": totalWins += 1
			elif teams[key][i]["Result"] == "Tie": totalWins += 0.5
		if teleopTotalHighGoalCycles != 0:
			averageHighGoalCycleTimeLow = round(float(teleopTotalHighGoalCycleTimeLow)/teleopTotalHighGoalCycles, 2)
			averageHighGoalCycleTimeHigh = round(float(teleopTotalHighGoalCycleTimeHigh)/teleopTotalHighGoalCycles, 2)
			teamOverall[key]["Teleop High Goal Average Shots Per Cycle"] = round(float(teleopTotalHighGoals)/teleopTotalHighGoalCycles, 2)
			teamOverall[key]["Teleop High Goal Average Cycle Time"] = str(averageHighGoalCycleTimeLow) + " - " + str(averageHighGoalCycleTimeHigh)
			highCycleTimeLow[key] = averageHighGoalCycleTimeLow
		else:
			teamOverall[key]["Teleop High Goal Average Shots Per Cycle"] = "N/A"
			teamOverall[key]["Teleop High Goal Average Cycle Time"] = "N/A"
			highCycleTimeLow[key] = "N/A"
		if teleopTotalLowGoalCycles != 0:
			averageLowGoalCycleTimeLow = round(float(teleopTotalLowGoalCycleTimeLow)/teleopTotalLowGoalCycles, 2)
			averageLowGoalCycleTimeHigh = round(float(teleopTotalLowGoalCycleTimeHigh)/teleopTotalLowGoalCycles, 2)
			teamOverall[key]["Teleop Low Goal Average Shots Per Cycle"] = round(float(teleopTotalLowGoals)/teleopTotalLowGoalCycles, 2)
			teamOverall[key]["Teleop Low Goal Average Cycle Time"] = str(averageLowGoalCycleTimeLow) + " - " + str(averageLowGoalCycleTimeHigh)
			lowCycleTimeLow[key] = averageLowGoalCycleTimeLow
		else:
			teamOverall[key]["Teleop Low Goal Average Shots Per Cycle"] = "N/A"
			teamOverall[key]["Teleop Low Goal Average Cycle Time"] = "N/A"
			lowCycleTimeLow[key] = "N/A"
		teamOverall[key]["Cross Baseline Ratio"] = str(autoBaseline) + "/" + str(len(teams[key]))
		teamOverall[key]["Auto Gears Ratio"] = str(autoGearsMade) + "/" + str(autoGearsTried)
		teamOverall[key]["Auto High Goal Total"] = autoHighGoals
		teamOverall[key]["Auto Low Goal Total"] = autoLowGoals
		teamOverall[key]["Teleop High Goal Total Cycles"] = teleopTotalHighGoalCycles
		teamOverall[key]["Teleop High Goal Average Cycles Per Game"] = round(float(teleopTotalHighGoalCycles)/len(teams[key]), 2)
		teamOverall[key]["Teleop High Goal Total Shots"] = teleopTotalHighGoals
		teamOverall[key]["Teleop Low Goal Total Cycles"] = teleopTotalLowGoalCycles
		teamOverall[key]["Teleop Low Goal Average Cycles Per Game"] = round(float(teleopTotalLowGoalCycles)/len(teams[key]), 2)
		teamOverall[key]["Teleop Low Goal Total Shots"] = teleopTotalLowGoals
		teamOverall[key]["Teleop Gears Ratio"] = str(teleopGearsMade) + "/" + str(teleopGearsTried)
		teamOverall[key]["Reached 40 kPa Ratio"] = str(totalReach40kPa) + "/" + str(len(teams[key]))
		teamOverall[key]["Average Total Pressure Per Game"] = round(float(totalPressure)/len(teams[key]), 2)
		teamOverall[key]["Average Rotors Turning Per Game"] = round(float(totalRotorsTurning)/len(teams[key]), 2)
		teamOverall[key]["Takeoff Ratio"] = str(totalTakeoffs) + "/" + str(len(teams[key]))
		teamOverall[key]["Average Alliance Total Points Per Game"] = round(float(totalAlliancePoints)/len(teams[key]), 2)
		teamOverall[key]["Average Single Robot Total Points Per Game"] = round(float(totalSingleRobotPoints)/len(teams[key]), 2)
		teamOverall[key]["Average Ranking Points Per Game"] = round(float(totalRankingPoints)/len(teams[key]), 2)
		teamOverall[key]["Winning Ratio"] = str(totalWins) + "/" + str(len(teams[key]))

	return teamOverall

def generateTeamTextFiles(teamOverall):
	for key in teamOverall:
		team = open(key + ".txt", "a")
		strings = [
			"Cross Baseline Ratio",
			"Auto Gears Ratio",
			"Auto High Goal Total",
			"Auto Low Goal Total",
			"Teleop High Goal Total Cycles",
			"Teleop High Goal Average Cycles Per Game",
			"Teleop High Goal Average Shots Per Cycle",
			"Teleop High Goal Total Shots",
			"Teleop High Goal Average Cycle Time",
			"Teleop Low Goal Total Cycles",
			"Teleop Low Goal Average Cycles Per Game",
			"Teleop Low Goal Average Shots Per Cycle",
			"Teleop Low Goal Total Shots",
			"Teleop Low Goal Average Cycle Time",
			"Teleop Gears Ratio",
			"Reached 40 kPa Ratio",
			"Average Total Pressure Per Game",
			"Average Rotors Turning Per Game",
			"Takeoff Ratio",
			"Average Alliance Total Points Per Game",
			"Average Single Robot Total Points Per Game",
			"Average Ranking Points Per Game",
			"Winning Ratio",
			"Matches"
			]
		for data in strings:
			if isinstance(teamOverall[key][data], float) or isinstance(teamOverall[key][data], int):
				team.write(data + ", " + str(teamOverall[key][data]) + "\n")
			elif data == "Matches":
				team.write(data + ", ")
				for number in teamOverall[key]["Matches"]:
					team.write(str(number) + " ")
			else:
				team.write(data + ", " + teamOverall[key][data] + "\n")

def generateMatchesFiles(teams):
	for team in teams:
		for match in range(len(teams[team])):
			oneTeamOneMatchFile = open(team + "_" + str(teams[team][match]["Match Number"][0]) + ".txt", "a")
			strings = [
				"Scouter Name",
				"Cross Baseline",
				"Auto Gears",
				"Auto Gears Ratio",
				"Auto High Goal",
				"Auto Low Goal",
				"Teleop High Goal Shots Per Cycle",
				"Teleop High Goal Shots Cycle Time",
				"Teleop High Goal Total Shots",
				"Teleop High Goal Total Cycles",
				"Teleop Low Goal Shots Per Cycle",
				"Teleop Low Goal Shots Cycle Time",
				"Teleop Low Goal Total Shots",
				"Teleop Low Goal Total Cycles",
				"Teleop Gears",
				"Teleop Gears Ratio",
				"Reached 40 kPa",
				"Total Pressure",
				"Rotors Turning",
				"Takeoff",
				"Total Points",
				"Estimated Single Robot Points",
				"Ranking Points",
				"Result",
				"Notes",
			]
			for data in strings:
				if isinstance(teams[team][match][data], float) or isinstance(teams[team][match][data], int):
					oneTeamOneMatchFile.write(data + ", " + str(teams[team][match][data]) + "\n")
				elif data == "Auto High Goal" or data == "Auto Low Goal" or data == "Total Pressure" or data == "Rotors Turning" or data == "Total Points" or data == "Ranking Points":
					if len(teams[team][match][data]) != 0:
						oneTeamOneMatchFile.write(data + ", " + str(teams[team][match][data][0]) + "\n")
					else:
						oneTeamOneMatchFile.write(data + ", ")
				elif data == "Auto Gears" or data == "Teleop Gears" or data == "Teleop High Goal Shots Per Cycle" or data == "Teleop Low Goal Shots Per Cycle":
					oneTeamOneMatchFile.write(data + ", ")
					if len(teams[team][match][data]) != 0:
						for number in teams[team][match][data]:
							oneTeamOneMatchFile.write(str(number) + " ")
					oneTeamOneMatchFile.write("\n")
				elif data == "Teleop High Goal Shots Cycle Time" or data == "Teleop Low Goal Shots Cycle Time":
					oneTeamOneMatchFile.write(data + ", ")
					if len(teams[team][match][data]) != 0:
						for cycle in range(len(teams[team][match][data])):
							oneTeamOneMatchFile.write(str(teams[team][match][data][cycle][0]) + " - " + str(teams[team][match][data][cycle][1]) + " ")
					oneTeamOneMatchFile.write("\n")
				elif data == "Notes":
					oneTeamOneMatchFile.write(data + ", " + teams[team][match][data])
				else:
					oneTeamOneMatchFile.write(data + ", " + teams[team][match][data] + "\n")

def generateRankings(teamOverall):
	rankings = {}
	teamNumbers = []
	for key in teamOverall:
		teamNumbers.append(key)
	categories = [
		"Cross Baseline Ratio",
		"Auto Gears Ratio",
		"Auto High Goal Total",
		"Auto Low Goal Total",
		"Teleop High Goal Total Cycles",
		"Teleop High Goal Average Cycles Per Game",
		"Teleop High Goal Average Shots Per Cycle",
		"Teleop High Goal Total Shots",
		"Teleop High Goal Average Cycle Time",
		"Teleop Low Goal Total Cycles",
		"Teleop Low Goal Average Cycles Per Game",
		"Teleop Low Goal Average Shots Per Cycle",
		"Teleop Low Goal Total Shots",
		"Teleop Low Goal Average Cycle Time",
		"Teleop Gears Ratio",
		"Reached 40 kPa Ratio",
		"Average Total Pressure Per Game",
		"Average Rotors Turning Per Game",
		"Takeoff Ratio",
		"Average Alliance Total Points Per Game",
		"Average Single Robot Total Points Per Game",
		"Average Ranking Points Per Game",
		"Winning Ratio"
	]
	baselineRatio = []
	autoHighGoals = []
	autoLowGoals = []
	autoGearsRatio = []
	teleopTotalHighGoalCycles = []
	teleopAverageHighGoalCycles = []
	teleopAverageHighGoalShotsPerCycle = []
	teleopAverageHighGoalCycleTimeLow = []
	teleopTotalHighGoals = []
	teleopTotalLowGoalCycles = []
	teleopAverageLowGoalCycles = []
	teleopAverageLowGoalShotsPerCycle = []
	teleopAverageLowGoalCycleTimeLow = []
	teleopTotalLowGoals = []
	teleopGearsRatio = []
	averagePressure = []
	reach40kPaRatio = []
	averageRotorsTurning = []
	takeoffRatio = []
	averageAlliancePoints = []
	averageSingleRobotPoints = []
	averageRankingPoints = []
	winningRatio = []

	variables = [
		baselineRatio,
		autoGearsRatio,
		autoHighGoals,
		autoLowGoals,
		teleopTotalHighGoalCycles,
		teleopAverageHighGoalCycles,
		teleopAverageHighGoalShotsPerCycle,
		teleopTotalHighGoals,
		teleopAverageHighGoalCycleTimeLow,
		teleopTotalLowGoalCycles,
		teleopAverageLowGoalCycles,
		teleopAverageLowGoalShotsPerCycle,
		teleopTotalLowGoals,
		teleopAverageLowGoalCycleTimeLow,
		teleopGearsRatio,
		reach40kPaRatio,
		averagePressure,
		averageRotorsTurning,
		takeoffRatio,
		averageAlliancePoints,
		averageSingleRobotPoints,
		averageRankingPoints,
		winningRatio
	]

	for number in range(len(categories)):
		data = categories[number]
		rankings[data] = {}
		if data[-5:] == "Ratio":
			for i in range(len(teamNumbers)):
				ratio = teamOverall[teamNumbers[i]][data]
				if int(ratio.split("/", 1)[1]) != 0:
					variables[number].append(float(ratio.split("/", 1)[0])/int(ratio.split("/", 1)[1]))
				else:
					variables[number].append("N/A")
			bubbleSortHighToLow(variables[number], teamNumbers)
			for j in range(len(teamNumbers)):
				rankings[data][j + 1] = teamNumbers[j]
		elif data == "Teleop High Goal Average Cycle Time" or data == "Teleop Low Goal Average Cycle Time":
			for i in range(len(teamNumbers)):
				if data == "Teleop High Goal Average Cycle Time":
					variables[number].append(highCycleTimeLow[teamNumbers[i]])
				elif data == "Teleop Low Goal Average Cycle Time":
					variables[number].append(lowCycleTimeLow[teamNumbers[i]])
			bubbleSortLowToHigh(variables[number], teamNumbers)
			for j in range(len(teamNumbers)):
				rankings[data][j + 1] = teamNumbers[j]
		else:
			for i in range(len(teamNumbers)):
				variables[number].append(teamOverall[teamNumbers[i]][data])
			bubbleSortHighToLow(variables[number], teamNumbers)
			for j in range(len(teamNumbers)):
				rankings[data][j + 1] = teamNumbers[j]
	return rankings

def generateRankingsFiles(rankings, teamOverall):
	for data in rankings:
		rankingFile = open(data + ".txt", "a")
		for number in range(len(rankings[data])):
			if number == len(rankings[data]) - 1:
				team = rankings[data][number + 1]
				if isinstance(teamOverall[team][data], float) or isinstance(teamOverall[team][data], int):
					rankingFile.write(team + ": " + str(teamOverall[team][data]))
				else:
					rankingFile.write(team + ": " + teamOverall[team][data])
			else:
				team = rankings[data][number + 1]
				if isinstance(teamOverall[team][data], float) or isinstance(teamOverall[team][data], int):
					rankingFile.write(team + ": " + str(teamOverall[team][data]) + "\n")
				else:
					rankingFile.write(team + ": " + teamOverall[team][data] + "\n")

def bubbleSortLowToHigh(values, numbers): #smallest to biggest
	for onePass in range(len(values) - 1, 0, -1):
		for i in range(0, onePass):
			if values[i + 1] == "N/A":
				a = values[i + 1]
				b = numbers[i + 1]
				values.append(a)
				numbers.append(b)
				del(values[i + 1])
				del(numbers[i + 1])
				i -= 1
			elif values[i + 1] < values[i]:
				tempValue = values[i]
				tempNumber = numbers[i]
				values[i] = values[i + 1]
				numbers[i] = numbers[i + 1]
				values[i + 1] = tempValue
				numbers[i + 1] = tempNumber

def bubbleSortHighToLow(values, numbers): #biggest to smallest
	for onePass in range(len(values) - 1, 0, -1):
		for i in range(0, onePass):
			if values[i + 1] == "N/A":
				a = values[i + 1]
				b = numbers[i + 1]
				values.append(a)
				numbers.append(b)
				del(values[i + 1])
				del(numbers[i + 1])
				i -= 1
			elif values[i + 1] > values[i]:
				tempValue = values[i]
				tempNumber = numbers[i]
				values[i] = values[i + 1]
				numbers[i] = numbers[i + 1]
				values[i + 1] = tempValue
				numbers[i + 1] = tempNumber


# generateOneFile() #generates a file with all the appended text files!  NOTE: must delete the file generated to run the code again
# allFile.close()
# teams = generateDict("oneFile.txt")
teams = generateDict("b3.txt")
print teams
print "\n"
overall = generateTeamOverall(teams)
print overall
print "\n"
generateTeamTextFiles(overall)
generateMatchesFiles(teams)
rankings = generateRankings(overall)
print rankings
generateRankingsFiles(rankings, overall)