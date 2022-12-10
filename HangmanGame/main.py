import random
import os
import json

def menu():

    print()
    print("Choose a number that corresponds to the category from which you want to guess the word or EXIT: ")
    print("0 -> EXIT")
    print("1 -> Food")
    print("2 -> Sports")
    print("3 -> Feelings")
    print("4 -> Art")
    print("5 -> Careers")
    print("6 -> Programming")
    print("7 -> Animals")
    print("8 -> Languages")
    print("9 -> Human body")
    print("10 -> Music")


def get_category_number():

    while True:
        try:
            print()
            category = int(input("Category:"))
            if category < 0 or category > 10:
                raise ValueError()
            return category
        except ValueError:
            print("Enter a valid number between 0 and 10")



def get_word(category_name):

    category_file = category_name + ".txt"
    try:
        file = open("C:/Users/Alina/Desktop/Hangman_Game/HangmanGame/" + category_file, "r")
        rows = 0
        for _ in file:
            rows += 1
        row_pos = random.randint(0, rows - 1) 
        file.seek(0) # go to the beginning of the file
        word = ""
        for pos, row in enumerate(file): 
            if pos == row_pos:
                word = row
                break
        file.close()
        word = word.replace("\n", "") 
        return word
    except FileNotFoundError:
        print("Couldn't find the file!")
    except IOError:
        print("Couldn't open the file!")



def display_category(category_nr):

    possible_categories = {1: "Food", 2: "Sports", 3: "Feelings", 4: "Art", 5: "Careers", 6: "Programming", 7: "Animals", 8: "Languages", 9: "HumanBody", 10: "Music"}
    category_name = possible_categories.get(category_nr)
    print("It's a word from: " + category_name)
    return get_word(category_name), category_name

    
def player_scores(result, category_name):
    
    fsr = open("scores.json", "r") 
    scores = json.loads(fsr.read()) 
    
    scores["Played games"] += 1
    if result == 1:
        scores["Won games"] += 1
    else: 
        scores["Lost games"] += 1
    

    fcr= open("categ.json", "r")
    categ = json.loads(fcr.read())

    for key in categ.keys(): 
        if key == category_name: 
            categ[key] += 1 

    fcw= open("categ.json", "w")
    json.dump(categ, fcw) 

    for key in categ:
        if key == category_name and categ[key] != 0 : 
            scores[category_name] = categ[key]
            break

    fsw = open("scores.json", "w")
    json.dump(scores, fsw)   

    fcr.close()
    fcw.close()
    fsr.close()
    fsw.close()
    return scores


def guess(word, attempts):

    init_attempts = attempts
    current_state = ["_" for _ in range(len(word))] 
    used_letters = []

    while True:
        print("       " + ' '.join(current_state) + "              Attempts left: " + str(attempts))
        print()
        print("Check this letter: ", end='')
        letter_to_check = input().lower()
        mistake = 0
        if letter_to_check == '':
            print("!! Enter a letter.")
            continue
        if len(letter_to_check) > 1 or not letter_to_check.isalpha():
            print("!! Enter only one letter, no numbers or other characters.")
            mistake = 1
        if letter_to_check in used_letters:
            if attempts != 1:
                print("!! Letter chosen before. Try a different letter.")
            mistake = 1
        else:
            used_letters.append(letter_to_check)
            
        letter_placed = 0
        for i in range(0, len(word)): 
            if mistake == 1: 
                break  
            if word[i] == letter_to_check: 
                current_state[i] = letter_to_check # put the letter on the right positions
                letter_placed = 1 

        if "_" not in current_state: # no more _ in the word => the player won => 1
            return 1, init_attempts - attempts

        if letter_placed == 0 or mistake == 1:  
            attempts = attempts - 1  # keep guessing

        if attempts == 0: #  no more attempts => the player lost => -1
            print("       " + ' '.join(current_state) + "              Attempts left: " + str(attempts)) 
            return -1, init_attempts - attempts


def start_game():

    menu()
    while True:
        category = get_category_number() 
        if category == 0:
            print("༼ つ ⚈ ܫ ⚈ ༽つ -- See you next time!--")
            return
        word, category_name = display_category(category) # return the random word from the file and category_name
        attempts = len(word) 
        game, failed_attempts = guess(word, attempts) 
        player_scores(game, category_name) 

        if game == 1:
            print()
            print("Well played! ( ๑ ⇀‿‿↼ ๑ )❤")
            print("The word was: " + word.upper())
            print("Failed attempts: " + str(failed_attempts))
        else:
            if game == -1:
                print()
                print("You don't have any attempts left! ¯\_(ಥ ﹏ಥ )_/¯ ")
                print("The word was: " + word.upper())
                print("Failed attempts: " + str(failed_attempts))
        menu()


if __name__ == '__main__':
     start_game()