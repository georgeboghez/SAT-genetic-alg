
# Comparare Algoritm Genetic - Algoritm Euristic
-   Nume: Boghez George si Tanase Teofil
-   An: II
-   Grupa: A2
-   Tema: T2

## Introducere
**SAT**, problema satisfiabilitatii, NP-completa, din clasa  presupune determinarea existentei unei tautologii/atribuiri satisfiabile unei formule booleene in forma normala conjunctiva - CNF. O formulă booleana este formata din literali, operatori logici (non, si, sau, implicatie, echivalenta) si paranteze. O atribuire de valori booleene pentru variabilele acestei expresii se numeste atribuire satisfiabila daca evaluarea expresiei dupa atribuirea valorilor da ca rezultat valoarea de adevar adevarat. Forma normal conjunctiva in care expresia este exprimata ca o conjunctie de propozitii, iar fiecare propozitie este formata dintr-o disjunctie de literali. Un literal este o variabila care poate fi sau nu negata. Un exemplu de expresie în forma normal conjunctiva ar fi: ![enter image description here](https://www.infoarena.ro/static/images/latex/078a2a2bd5464e27079b92d309d4f18d_3.5pt.gif)
Pentru rezolvarea problemei satisfiabilitatii vom utiliza un algoritm genetic si un algoritm euristic, intentionand sa comparam rezultatele obtinute pentru determinarea celui mai bun pentru aceasta problema.
## Motivatie
**Problema SAT** este prima problema NP-completa găsita. Stephen Cook a demonstrat NP-completitudinea ei in 1971. Aceasta problema ramane NP-completa chiar daca restrictionam expresiile la unele care in forma normal conjunctiva au doar trei literali. Problema satisfiabilităţii pentru asemenea expresii se numeşte 3-SAT, şi multe probleme pot fi demonstrate a fi NP-complete prin reducerea lui 3-SAT la problemele respective in timp polinomial. Obiectvul urmarit in acest proiect este de a gasi cea mai buna metoda de rezolvare a problemei satisfiabilitatii din punct de vedere al timpului de executie, cat si al consistentei rezultatelor obtinute, utilizand atat algoritmi genetici, cat si euristici. 

## Experiment
Problemele selectate pentru a fi rezolvate se gasesc la [http://sites.nlsde.buaa.edu.cn/~kexu/benchmarks/benchmarks.htm](http://sites.nlsde.buaa.edu.cn/~kexu/benchmarks/benchmarks.htm), iar abordarea acestora presupune urmatorii algoritmi:
#### Algoritm Genetic
**Populatia** este reprezentata dintr-o lista de indivizi, fiecare cromozom fiind compus dintr-o lista de X valori 0 sau 1, unde X reprezinta numarul de literali unici ai formulei, 0 reprezentand valoarea de adevar False, 1 reprezentand valoarea de adevar True, iar intreaga lista reprezentand **tautologia/atribuirea**.

```
def generateAssignation(numberOfLiterals):
    literals = list()
    for number in range(0, numberOfLiterals):
        literals.append(random.randint(0, 1))
    return literals
```
```
def genPop(numberOfLiterals):
    pop = list()
    for x in range(0, 20):
        pop.append(generateAssignation(numberOfLiterals))
    return pop
```

Exista diferite metode de selectie a noii populatii in diferite implementari ale algoritmilor genetici, in acest experiment fiind utilizata selectia **Wheel Of Fortune**.

```
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
```
 In functie de un **fitness** calculat anterior, se vor alege cromozomii ce vor da nastere urmatoarei populatii dupa inca o generatie.
```
def evaluate(formula, population):
    fitness = list()
    maximum = 0
    for cromosom in population:
        cromosomsFitness = calculate_satisfiability(formula, cromosom)
        fitness.append(cromosomsFitness)
        if cromosomsFitness > maximum:
            maximum = cromosomsFitness
    return [fitness, maximum]
```
Fitness-ul consta in determinarea numarului de clauze adevarate din formula booleana data.
```
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
```
Pentru a ajunge la noi generatii, dupa selectia facuta anterior, cromozomii trec prin doua metode de alterare ce constau in incrucisare (**crossover**) - cu o probabilitate de 80% - si mutatie (**mutation**) - cu o probabilitate de 100%. Dupa alegerea cu o probabilitate stabilita initial a cromozomilor ce vor participa in procesul de incrucisare, pentru fiecare pereche de doi cromozomi se va selecta un punct de "taiere" la intamplare, urmand sa faca schimb de informatii in felul urmator:\
**01 001011** -> **01** 111100\
10 111100 -> 10 **001011**       
\
In cadrul procesului de mutatie, am optat pentru o mutatie Greedy. Astfel, pentru fiecare locus, selectat de la stanga la dreapta, am verificat daca prin schimbarea valorii cu cealalta valoare disponibila in multimea de posibilitati (**alela**) creste fitness-ul, in caz afirmativ, valoarea ramanand modificata, iar daca sunt egale fitness-urile, exista o posibilitate de 50% pentru a reveni la forma precedenta, altfel revenind asigurat la forma anterioara. Exemplu de mutatie:\
0010110**0**0 -> 0010110**1**0 

```
def crossover(population, toParticipateInCrossover, bitsPerNum, dimensions):
    firstCromosomAfterCrossover = list()
    secondCromosomAfterCrossover = list()
    for i in range(0, len(toParticipateInCrossover) - 1):
        for j in range(i + 1, len(toParticipateInCrossover)):
            cuttingPoint = random.randint(1, bitsPerNum - 1)
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

def alter(population, numberOfLiterals, formula):
	# Incrucisare
    toParticipateInCrossover = list()
    for i in range(0, len(population)):
        if random.uniform(0, 1) < PC:
            toParticipateInCrossover.append(i)
    population = crossover(
        population, toParticipateInCrossover, numberOfLiterals)
    # Sfarsit Incrucisare

	# Mutatie
    for i in range(0, len(population)):
        initialFitness = calculate_satisfiability(formula, population[i])
        for locus in randomOrder(population[i]): # pozitiile genelor (toate) sunt alese la intamplare
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
    # Sfarsit Mutatie
    return population
```

#### Algoritm Euristic

Generam o tautologie formata din valori de adevar alese aleatoriu, vom alege la intamplare cate o valoare de adevar de X ori, unde X este de 3 ori numarul de literali, pe care o vom nega, iar daca rezultatul este mai mare sau egal cu precedentul, valoarea de adevar ramane schimbata, altfel revenind la valoarea precedenta.  Procesul se repeta pentru o perioada predefinita de timp.

```
def genPop(numberOfLiterals):
    return generateAssignation(numberOfLiterals)
```

```
startTime = time.time()
globalMaximum = 0
while endtTime - startTime < 28800 and globalMaximum != len(formula):
    bitlist = genPop(numberOfLiterals)
    initialSat = calculate_satisfiability(formula, bitlist)
    for i in range(0, len(bitlist) * 3):
        randLocus = random.randint(0, len(bitlist) - 1)
        bitlist[randLocus] = 1 - bitlist[randLocus]
        currentSat = calculate_satisfiability(formula, bitlist)
        if currentSat < initialSat:
            bitlist[randLocus] = 1 - bitlist[randLocus]
        else:
            initialSat = currentSat
    endtTime = time.time()
    if initialSat > globalMaximum:
        globalMaximum = initialSat
```

## Rezultate

Algoritmii au fost rulati de 30 de ori pentru fiecare dintre probleme, cu un timp de rulare de 4 ore sau 8 ore alocat fiecaruia.


| Literali | Clauze | Metoda   | Maxim | Maxim Procentaj | Media       | Deviatia Standard | Varianta    | Timp |
|----------|--------|----------|-------|-----------------|-------------|-------------------|-------------|------|
| 450      | 19084  | Genetic  | 19080 | 99.9790%        | 19078.60    | 1.624807681       | 2.64        | 2h   |
| 450      | 19084  | Euristic | 19046 | 99.8009%        | 18974.43333 | 132.4677781       | 17547.71222 | 2h   |
  
![SAT - 450L, 19084C](https://i.imgur.com/pUh4feT.png)
  
  Algoritm Genetic 450 literali - Grafic
  
| Literali | Clauze | Metoda   | Maxim | Maxim Procentaj | Media   | Deviatia Standard | Varianta | Timp |
|----------|--------|----------|-------|-----------------|---------|-------------------|----------|------|
| 760      | 43780  | Genetic  | 43774 | 99.9863%        | 43768.8 | 7.152621897       | 51.16    | 4h   |
| 760      | 43780  | Euristic | 43663 | 99.7328%        | 43565.4 | 63.65092301       | 4051.44  | 4h   |
  
![SAT - 760L, 43780C](https://i.imgur.com/tmzxL3m.png)
  
  Algoritm Genetic 760 literali - Grafic  

| Literali | Clauze | Metoda   | Maxim | Maxim Procentaj | Media   | Deviatia Standard | Varianta    | Timp |
|----------|--------|----------|-------|-----------------|---------|-------------------|-------------|------|
| 945      | 61855  | Genetic  | 61849 | 99.9903%        | 61840.8 | 6.559471523       | 43.02666667 | 8h   |
| 945      | 61855  | Euristic | 61709 | 99.7640%        | 61605.5 | 103.8713146       | 10789.25    | 8h   |
  
![SAT - 945L, 61855C](https://i.imgur.com/UuFztCg.png)
  
  Algoritm Genetic 450 literali - Grafic  
  
| Literali | Clauze | Metoda   | Maxim | Maxim Procentaj | Media   | Deviatia Standard | Varianta    | Timp |
|----------|--------|----------|-------|-----------------|---------|-------------------|-------------|------|
| 1150     | 84508  | Genetic  | 84500 | 99.9905%        | 84493.8 | 4.110150038       | 16.89333333 | 8h   |
| 1150     | 84508  | Euristic | 84259 | 99.7054%        | 84126.1 | 142.0460841       | 20177.09    | 8h   |
  
![SAT - 1150L, 84508C](https://i.imgur.com/F6XSYSS.png)
  
  Algoritm Genetic 1150 literali - Grafic  

| Literali | Clauze | Metoda   | Maxim  | Maxim Procentaj | Media       | Deviatia Standard | Varianta    | Timp |
|----------|--------|----------|--------|-----------------|-------------|-------------------|-------------|------|
| 1534     | 132295 | Genetic  | 132282 | 99.9902%        | 132277.4667 | 4.014418458       | 16.11555556 | 8h   |
| 1534     | 132295 | Euristic | 131901 | 99.7022%        | 131428.7333 | 517.8364564       | 268154.5956 | 8h   |
  
![SAT - 1534L, 132295C](https://i.imgur.com/RZUDnR3.png)
  
  Algoritm Genetic 1534 literali - Grafic  

## Concluzie
Dupa cum putem observa in tabelul de rezultate, niciuna dintre abordari nu rezolva problema in timpul alocat, dar se apropie considerabil de solutia dorita, majoritatea instantelor avand un procentaj de rezolvare apropiat de 100%.

Cu toate ca exista similitudini intre rezultate, este evident ca algoritmul genetic ajunge la rezultate mult mai bune, intr-un timp, totusi, mai mare decat al celui euristic, dar diferenta de timp este compensata de sansa crescuta a algoritmului genetic de a ajunge la solutia dorita comparativ cu probabilitatea aproape neglijabila a algoritmului euristic de a solutiona problema.

Algoritmii genetici ar putea fi modificati, spre exemplu, putand fi alese mai multe puncte de taiere in crossover, cresterea sau scaderea probabilitatilor de alegere a cromozomilor care intra in crossover si in mutatie sau chiar schimbarea metodei de selectie sau a celei de mutatie. Totodata, algoritmul euristic *poate* fi imbunatatit prin cresterea numarului de verificari ale valorilor de adevar aleator alese, dar cu aceasta modificare exista o consecinta legata de timpul de executie a unei iteratii in cadrul while-ului.

## Bibliografie

[http://sites.nlsde.buaa.edu.cn/~kexu/benchmarks/benchmarks.htm](http://sites.nlsde.buaa.edu.cn/~kexu/benchmarks/benchmarks.htm)  
[https://en.wikipedia.org/wiki/Boolean_satisfiability_problem](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem)  
[https://profs.info.uaic.ro/~pmihaela/GA/](https://profs.info.uaic.ro/~pmihaela/GA/)  
[https://profs.info.uaic.ro/~pmihaela/GA/laborator3.html](https://profs.info.uaic.ro/~pmihaela/GA/laborator3.html)  
[https://profs.info.uaic.ro/~marta/ga/L3/](https://profs.info.uaic.ro/~marta/ga/L3/)
