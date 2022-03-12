import pandas as pd
import csv

class Pokemon:
    def __init__(self, row):
        self.index = row["index"]
        self.name = row["name"]
        self.generation = row["generation"]
        self.type_number = row["type_number"]
        self.type_1 = row["type_1"]
        self.type_2 = row["type_2"]
        self.height = row["height_m"]
        self.weight = row["weight_kg"]

class Hint:
    def __init__(self, generation, type_1, type_2, min_height, max_height, min_weight, max_weight):
        self.generation = generation
        self.type_1 = type_1
        self.type_2 = type_2
        self.min_height = min_height
        self.max_height = max_height
        self.min_weight = min_weight
        self.max_weight = max_weight

def check_guess(answer, guess, hint):
    hint.generation = check_generation(answer.generation, guess.generation, hint.generation)
    hint.type_1, hint.type_2 = check_types(answer, guess, hint.type_1, hint.type_2)
    hint.min_height, hint.max_height = check_stat(answer.height, guess.height, hint.min_height, hint.max_height)
    hint.min_weight, hint.max_weight = check_stat(answer.weight, guess.weight, hint.min_weight, hint.max_weight)
    return hint

def check_index(answer, guess):
    if(answer == guess):
        return True
    return False

def check_generation(answer, guess, gen_list):
    if(answer == guess):
        return [answer]
    if(answer < guess):
        for gen in gen_list:
            if(gen >= guess):
                gen_list.remove(gen)
        return gen_list
    for gen in gen_list:
        if(gen >= guess):
            gen_list.remove(gen)
    return gen_list

def check_types(answer, guess, type_1, type_2):
    if(answer.type_1 == guess.type_1 or answer.type_1 == guess.type_2):
        type_1 = [answer.type_1]
    if(answer.type_2 == guess.type_2 or answer.type_2 == guess.type_1):
        type_2 = [answer.type_2]
    if(guess.type_1 not in [answer.type_1, answer.type_2]):
        if(guess.type_1 in type_1):
            type_1.remove(guess.type_1)
    if(guess.type_2 not in [answer.type_1, answer.type_2]):
        if(guess.type_number == 2 and guess.type_2 in type_2):
            type_2.remove(guess.type_2)
    return type_1, type_2

def check_stat(answer, guess, min, max):
    if(answer == guess):
        return answer, answer
    if(guess > answer and guess < max):
        return min, guess
    if(guess < answer and guess > min):
        return guess, max
    if(guess == max):
        return min, (max - 0.1)
    if(guess == min):
        return (min + 0.1), max
    if(int(guess) == max):
        return min, (guess - 0.1)
    if(int(guess) == min):
        return (guess + 0.1), max

def next_guess(guess_list, hint, current_guess):
    new_guess_list = []
    for pokemon in guess_list:
        if(pokemon.weight <= hint.max_weight and pokemon.weight >= hint.min_weight and pokemon.height <= hint.max_height and pokemon.height >= hint.min_height
        and pokemon.type_1 in hint.type_1 and pokemon.type_2 in hint.type_2 and pokemon.generation in hint.generation and pokemon.index != current_guess.index):
            new_guess_list.append(pokemon)
    return new_guess_list, new_guess_list[int(len(new_guess_list)/2)]


pokedex = pd.read_csv(r'C:\Users\CSUKFRME\Downloads\pokedex.csv')

generations = [1, 2, 3, 4, 5, 6, 7, 8]
types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dark", "Dragon", "Steel", "Fairy"]

guess_list = []
for index, row in pokedex.iterrows():
    pokemon = Pokemon(row)
    if(pokemon.type_number == 1):
        pokemon.type_2 = "Mono"
    guess_list.append(pokemon)

for index, answer_row in pokedex.iterrows():
    answer = Pokemon(answer_row)
    for index, start_row in pokedex.iterrows():
        current_guess_list = list(guess_list)
        start_guess = Pokemon(start_row)
        current_guess = Pokemon(start_row)
        current_guess_list.pop(index)
        gens = generations
        type_1 = list(types)
        type_2 = list(types)
        type_2.append("Mono")
        min_height = 0.1
        max_height = 999
        min_weight = 0.1
        max_weight = 999
        total_guesses = 1
        hint = Hint(gens, type_1, type_2, min_height, max_height, min_weight, max_weight)
        while(not check_index(answer.index, current_guess.index)):
            hint = check_guess(answer, current_guess, hint)
            hint.max_height = round(hint.max_height,1)
            hint.min_height = round(hint.min_height,1)
            hint.max_weight = round(hint.max_weight,1)
            hint.min_weight = round(hint.min_weight,1)
            current_guess_list, current_guess = next_guess(current_guess_list, hint, current_guess)
            total_guesses += 1
        print("Start Guess: " + start_guess.name + " Answer: " + answer.name + " Guesses: " + str(total_guesses))
        with open('guesses.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([start_guess.name, answer.name, total_guesses])
        
