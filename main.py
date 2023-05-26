import random
import matplotlib.pyplot as plt


def function(x):
    return 1.5 * x**3 + 3 * x


def generate_population(n):
    population = []
    for i in range(n):
        individual = ''
        for j in range(10):
            rand = random.randint(0, 1)
            individual += str(rand)
        population.append(individual)
    return population


def decode(individual):
    return 0.015625 * int(individual, 2) + 0.015625 - 8


def encode(gene):
    _ = int((gene + 8 - 0.015625) / 0.015625)
    binary_str = bin(_)[2:].zfill(10)
    return binary_str


def fitness_function(chromosome):
    return function(decode(chromosome))


def mutation(chromosome):
    index = random.randint(0, len(chromosome) - 1)
    return chromosome[index:] + chromosome[:index]


def rank_selection(population):
    fitness_scores = [fitness_function(x) for x in population]
    population_fitness = list(zip(population, fitness_scores))
    population_fitness.sort(key=lambda x: x[1])

    mating_pool = []
    for i in range(len(population)):
        mating_pool.append(population[i])
    return mating_pool[:len(mating_pool)//2]


def cross_over(parent1, parent2):
    index = random.randint(0, len(parent1) - 1)
    child1 = parent1[:index] + parent2[index:]
    child2 = parent2[:index] + parent1[index:]
    return child1, child2


def genetic_algorithm(population_size, n_generations, mutation_chance):
    population = generate_population(population_size)
    top_population = []

    for generation in range(n_generations):
        mating_pool = rank_selection(population)
        top_population.append(fitness_function(mating_pool[0]))
        childrens = []

        for _ in range(len(mating_pool)):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = cross_over(parent1, parent2)

            if random.random() < mutation_chance:
                child1 = mutation(child1)
            if random.random() < mutation_chance:
                 child2 = mutation(child2)

            childrens.append(child1)
            childrens.append(child2)
            population = childrens

    fitness_scores = [fitness_function(x) for x in population]
    population_fitness = list(zip(population, fitness_scores))
    population_fitness.sort(key=lambda x: x[1])
    top_member = population_fitness[0]
    top_population.append(fitness_function(top_member[0]))
    print(f'Best member: x = {decode(top_member[0])}, y = {fitness_function(top_member[0])}')
    return decode(top_member[0]), top_population


best_member, best_population = genetic_algorithm(100, 50, 0.1)


x_values = [i * 0.1 for i in range(-91, 91)]
y_values = [function(x) for x in x_values]

plt.plot(x_values, y_values)
plt.plot(best_member, function(best_member), 'ro')
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Function and its calculated minimum")
plt.show()

plt.plot(best_population)
plt.xlabel("Generation")
plt.ylabel("Fitness function")
plt.title("Evolution of the best population member")
plt.show()
