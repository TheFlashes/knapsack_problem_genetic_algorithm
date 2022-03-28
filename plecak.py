import random

class Algorithm:
    _POPULATION_COUNT = 20
    _BAG_MAX_WEIGHT = 53
    _MAX_POSSIBLE_VALUE = 0 # 70
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
        (2, 7),
    )

    def addItem(self, weight, value):
        self.items.append({
            "weight": weight,
            "value": value
        })
        self._MAX_POSSIBLE_VALUE += value

    def initPopulation(self):
        for _ in range(self._POPULATION_COUNT):
            chromosome = []
            for _ in range(10):
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
            phenotype["chanceToCross"] = 0
        else:
            phenotype["score"] = phenotype["value"] + ((phenotype["value"] - phenotype["weight"]) / 2)
            phenotype["score"] = round(phenotype["score"], 2)
            phenotype["chanceToCross"] = round(random.uniform(0.0, 1.0), 2)
        return phenotype

    def __init__(self):
        self.items = []
        self.population = []
        for item in self._ITEMS: self.addItem(item[0], item[1])

        self.initPopulation()

        phenotypes = []
        for chromosome in self.population:
            phenotypes.append(self.fitnessAssessment(chromosome))

        phenotypes.sort(key=lambda p:p["score"], reverse=True)

        for p in phenotypes:
            print(p)

        print()

        for p in phenotypes:
            if (p["chanceToCross"] <= self._Pk):
                print(p)

Algorithm()