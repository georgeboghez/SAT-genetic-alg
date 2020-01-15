import random
import sys
import time


def parseFile(file):
    with open(file, 'r') as f:
        cnfFileContent = f.read()

    cnfFileContent = cnfFileContent.split('\n')

    formula = list()

    for line in cnfFileContent:
        if line:
            if line[0] not in ('c', 'p'):
                line = line.replace('  0', '')
                line = line.replace(' 0', '')
                line = [int(x) for x in line.split(' ')]
                formula.append(line)
            elif line[0] == 'p':
                line = line.split(' ')
                numberOfLiterals = int(line[2])
    return [numberOfLiterals, formula]


def generateAssignation(numberOfLiterals):
    literals = list()
    for number in range(0, numberOfLiterals):
        literals.append(random.randint(0, 1))
    return literals


def genPop(numberOfLiterals):
    return generateAssignation(numberOfLiterals)


def calculate_satisfiability(formula, assignation):
    numberOfTrueClauses = 0
    for clause in formula:
        isClauseTrue = False
        for literal in clause:
            if literal < 0:
                if assignation[abs(literal) - 1] == 0:
                    isClauseTrue = True
                    break
            else:
                if assignation[literal - 1] == 1:
                    isClauseTrue = True
                    break
        if isClauseTrue:
            numberOfTrueClauses += 1
    return numberOfTrueClauses


def euristic(filename, outputFilename):
    startTime = time.time()
    essentialData = parseFile(filename)
    numberOfLiterals = essentialData[0]
    print("no of literals:", numberOfLiterals)
    formula = essentialData[1]
    print("formula length:", len(formula))

    globalMaximum = 0
    it = 0
    endtTime = time.time()
    while endtTime - startTime < 28800 and globalMaximum != len(formula):
        it += 1
        bitlist = genPop(numberOfLiterals)
        initialSat = calculate_satisfiability(formula, bitlist)
        for i in range(0, len(bitlist) * 2):
            randLocus = random.randint(0, len(bitlist) - 1)
            bitlist[randLocus] = 1 - bitlist[randLocus]
            currentSat = calculate_satisfiability(formula, bitlist)
            if currentSat < initialSat:
                bitlist[randLocus] = 1 - bitlist[randLocus]
            else:
                initialSat = currentSat
        endtTime = time.time()
        print(it)
        print("Time: " + str(endtTime - startTime))
        print(initialSat)
        print('percentage:', float(initialSat) * 100 / len(formula), '%')
        if initialSat > globalMaximum:
            globalMaximum = initialSat
            print('maximum:', globalMaximum)
            print('percentage:', float(globalMaximum) * 100 / len(formula), '%')
            with open(outputFilename + '.txt', "a+") as f:
                f.write(str(globalMaximum) + '\n')
            with open(outputFilename + 'time.txt', "a+") as f:
                f.write(str(endtTime - startTime) + '\n')
            with open(outputFilename + 'percentage.txt', "a+") as f:
                f.write(str(float(globalMaximum) * 100 / len(formula)) + '%\n')


def main():
    try:
        file = sys.argv[1]
        outputFilename = sys.argv[2]
        euristic(file, outputFilename)
    except:
        print("Usage: python " + sys.argv[0] + " file.cnf output")


if __name__ == '__main__':
    main()
