import random
import sys
import time

PC = 0.8
PM = 1.0


def fitnessSum(fitness):
    T = 0.0
    for i in range(0, len(fitness)):
        T += fitness[i]
    return T


def wheelOfFortuneSelection(fitness, population):
    p = list()
    T = fitnessSum(fitness)
    for i in range(0, len(fitness)):
        p.append(fitness[i] / T)
    q = list()
    q.append(0.0)
    for i in range(0, len(fitness)):
        q.append(q[i] + p[i])

    newPopulation = list()
    while len(newPopulation) == 0:
        for i in range(0, len(fitness)):
            r = random.uniform(0, 1)
            for j in range(0, len(population)):
                if q[j] < r and r <= q[j + 1]:
                    newPopulation.append(population[j])
                    break
    return newPopulation


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


def crossover(population, toParticipateInCrossover, numberOfLiterals):
    firstCromosomAfterCrossover = list()
    secondCromosomAfterCrossover = list()
    for i in range(0, len(toParticipateInCrossover) - 1, 2):
        for j in range(i + 1, len(toParticipateInCrossover)):
            # for k in range(5):
            cuttingPoint = random.randint(
                1, len(population) - 1)
            firstCromosomAfterCrossover = population[toParticipateInCrossover[i]][:cuttingPoint]
            firstCromosomAfterCrossover.extend(
                population[toParticipateInCrossover[j]][cuttingPoint:])
            secondCromosomAfterCrossover = population[toParticipateInCrossover[j]][:cuttingPoint]
            secondCromosomAfterCrossover.extend(
                population[toParticipateInCrossover[i]][cuttingPoint:])
            population[toParticipateInCrossover[i]
                       ] = firstCromosomAfterCrossover
            population[toParticipateInCrossover[j]
                       ] = secondCromosomAfterCrossover
            break
    return population


def randomOrder(seq):
    shuffled = list(range(0, len(seq)))
    random.shuffle(shuffled)
    return shuffled


def alter(population, numberOfLiterals, formula):
    toParticipateInCrossover = list()
    for i in range(0, len(population)):
        if random.uniform(0, 1) < PC:
            toParticipateInCrossover.append(i)
    population = crossover(
        population, toParticipateInCrossover, numberOfLiterals)

    for i in range(0, len(population)):
        initialFitness = calculate_satisfiability(formula, population[i])
        for locus in randomOrder(population[i]):
            if random.uniform(0, 1) <= PM:
                population[i][locus] = 1 - population[i][locus]
                currentFitness = calculate_satisfiability(
                    formula, population[i])
                if currentFitness <= initialFitness:
                    if currentFitness == initialFitness:
                        if random.uniform(0, 1) < 0.5:
                            population[i][locus] = 1 - population[i][locus]
                    else:
                        population[i][locus] = 1 - population[i][locus]
                else:
                    initialFitness = currentFitness
    return population


def generateAssignation(numberOfLiterals):
    literals = list()
    for number in range(0, numberOfLiterals):
        literals.append(random.randint(0, 1))
    return literals


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


def evaluate(formula, population):
    fitness = list()
    maximum = 0
    for cromosom in population:
        cromosomsFitness = calculate_satisfiability(formula, cromosom)
        fitness.append(cromosomsFitness)
        if cromosomsFitness > maximum:
            maximum = cromosomsFitness
    return [fitness, maximum]


def genPop(numberOfLiterals):
    pop = list()
    for x in range(0, 20):
        pop.append(generateAssignation(numberOfLiterals))
    return pop


def genAlg(file, outputFile):
    startingTime = time.time()
    essentialData = parseFile(file)
    numberOfLiterals = essentialData[0]
    print("no of literals:", numberOfLiterals)
    formula = essentialData[1]
    print("formula length:", len(formula))

    population = genPop(numberOfLiterals)

    var = evaluate(formula, population)
    fitness = var[0]
    globalMaximum = 0

    endingTime = time.time()
    while endingTime - startingTime < 28800 and globalMaximum != len(formula):
        population = wheelOfFortuneSelection(fitness, population)
        population = alter(population, numberOfLiterals, formula)
        var = evaluate(formula, population)
        fitness = var[0]
        maximum = var[1]
        # print(maximum, 'out of', len(formula))
        endingTime = time.time()
        if maximum > globalMaximum:
            globalMaximum = maximum
            print('maximum:', globalMaximum)
            print('percentage:', float(globalMaximum) * 100 / len(formula), '%')
            with open(outputFile + ".txt", "a+") as f:
                toWrite = str(globalMaximum) + "\n"
                f.write(toWrite)
            with open(outputFile + "percentage.txt", "a+") as f:
                toWrite = str(float(globalMaximum) * 100 / len(formula)) + "%\n"
                f.write(toWrite)
            with open(outputFile + "time.txt", "a+") as f:
                toWrite = str(endingTime - startingTime) + "\n"
                f.write(toWrite)


if __name__ == '__main__':
    try:
        genAlg(sys.argv[1], sys.argv[2])
    except:
        print("Usage: python " + sys.argv[0] + " file.cnf output")
