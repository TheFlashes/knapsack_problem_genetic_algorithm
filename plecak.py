import random

class Algorithm:
    _POPULATION_COUNT = 20
    _BAG_MAX_WEIGHT = 53
    _MAX_POSSIBLE_VALUE = 0 # 70
    _GENERATIONS = 20
    _Pm = 0.1
    _Pk = 0.8
    _ITEMS = (
        (3, 5),
        (12, 9),
        (8, 1),
        (11, 14),
        (10, 8),
        (7, 12),
        (6, 5),
        (2, 6),
        (14, 3),
        (2, 7)
    )

    def printInfo(self):
        print("\033[H\033[J", end="") # Czyści ekran
        print(f"Population: {self._POPULATION_COUNT}")
        print(f"Chance for interbreeding: {self._Pk}")
        print(f"Chance for mutations: {self._Pm}")
        print(f"Generations: {self._GENERATIONS}\n")
        print(f"Maximum load lifting capacity: {self._BAG_MAX_WEIGHT}")
        print(f"Value of all items: {self._MAX_POSSIBLE_VALUE}\n")
        print("Items:")

        for idx, i in enumerate(self.items):
            print("{}. {}kg, {}$".format(idx + 1, i["weight"], i["value"]))

    def printTable(self, phenotypes):
        def fs(text, length):
            text = str(text)
            while(len(text) < length):
                text = "{} ".format(text)
            return text

        print("┌──────────────────────────────┬──────┬─────┬─────┐")
        print("│          Chromosome          │Weight│Value│Score│")
        print("├──────────────────────────────┼──────┼─────┼─────│")
        for p in phenotypes:
            print("│{}│ {}kg │ {}$ │{} │".format(p["chromosome"], fs(p["weight"], 2), fs(p["value"], 2), fs(p["score"], 4)))
        print("└──────────────────────────────┴──────┴─────┴─────┘")

    def addItem(self, weight, value):
        self.items.append({
            "weight": weight,
            "value": value
        })
        self._MAX_POSSIBLE_VALUE += value

    def initPopulation(self):
        for _ in range(self._POPULATION_COUNT):
            chromosome = []
            for _ in range(len(self._ITEMS)):
                chromosome.append(random.randint(0,1))
            self.population.append(chromosome)

    def fitnessAssessment(self, chromosome):
        phenotype = {
            "chromosome": chromosome,
            "weight": 0,
            "value": 0
        }
        for idx, gene in enumerate(chromosome):
            if (gene):
                phenotype["weight"] += self.items[idx]["weight"]
                phenotype["value"] += self.items[idx]["value"]
        
        if (phenotype["weight"] > self._BAG_MAX_WEIGHT):
            phenotype["score"] = 0
            phenotype["chanceToCross"] = 1
        else:
            phenotype["score"] = phenotype["value"] + ((phenotype["value"] - phenotype["weight"]) / 2)
            phenotype["score"] = round(phenotype["score"], 2)
            phenotype["chanceToCross"] = round(random.uniform(0.0, 1.0), 2)
        return phenotype

    def __init__(self):
        self.items = []
        self.population = []
        self.generation = 0
        for item in self._ITEMS: self.addItem(item[0], item[1])

        self.initPopulation()

        while(True):
            self.generation += 1

            phenotypes = []
            for chromosome in self.population:
                phenotypes.append(self.fitnessAssessment(chromosome))

            phenotypes.sort(key=lambda p:p["score"], reverse=True)
            
            self.printInfo()
            print(f"\n{self.generation} generation:")
            self.printTable(phenotypes)

            newPopulation = []
            childs = []
            pair = [None, None]
            for idx, p in enumerate(phenotypes):
                newPopulation.append(p["chromosome"])
                if (p["chanceToCross"] <= self._Pk):
                    if (pair[0] == None and pair[1] == None):
                        pair[0] = idx
                    elif (pair[0] != None and pair[1] == None):
                        pair[1] = idx
                        locus = random.randint(0, len(self._ITEMS) -1)
                        childs.append([*phenotypes[pair[0]]["chromosome"][:locus], *phenotypes[pair[1]]["chromosome"][locus:]])
                        childs.append([*phenotypes[pair[1]]["chromosome"][:locus], *phenotypes[pair[0]]["chromosome"][locus:]])
                        pair = [None, None]

            for i in range(len(childs)):
                newPopulation[-(i + 1)] = childs[i]

            for i in range(len(newPopulation)):
                chanceOfMutation = round(random.uniform(0.0, 1.0), 2)
                if (chanceOfMutation <= self._Pm):
                    locus = random.randint(0, len(self._ITEMS) - 1)
                    if (newPopulation[i][locus] == 1): newPopulation[i][locus] = 0
                    else: newPopulation[i][locus] = 1

            self.population = newPopulation
            input()

Algorithm()