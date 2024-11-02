#Terminal version of the popular word guessing game. Six Chances to guess the five letter word.
#Database has over 12,000 words. Play the game as many times as you like until the dictionary is exhausted.

from os import system
from time import sleep
from random import randint
from termcolor import colored

class wordle_tools():
    def __init__(self):
        pass

    def print_wordle(self):
        #Print wordle board. Previous guesses in a 2 dimensional matrix. Maps the letters to the correct colour. 
        #Uppercase letters were guessed correctly and translate to green
        #Lowercase letters are in the word but in the incorrect place and translate to yellow
        #Letters prefixed with . were guessed incorrectly and translate to white
        #Unplayed guesses depicted as - and translate to white

        system("cls")
        print("WORDLE")
        print("\n")
    
        for a in range (len(wordle_matrix)):
            for b in range(len(wordle_matrix[a])):     
                    if '.' in wordle_matrix[a][b]:
                        w_letter=wordle_matrix[a][b].replace(".","")
                        print(colored(w_letter.upper(),'white'),end="")
                    elif wordle_matrix[a][b] == "- ":
                        print(colored(wordle_matrix[a][b],'white'),end="")
                    elif wordle_matrix[a][b].islower():
                        print(colored(wordle_matrix[a][b].upper(),'yellow'),end="")
                    elif wordle_matrix[a][b].isupper():
                        print(colored(wordle_matrix[a][b],'green'),end="")      
            print()    

    def letter_matching(self):
        #Find all letters that are guessed correctly, incorrectly and in wrong position. 
        #Marks the letters in a specific fashion within the wordle board matrix so they can be mapped 
        #to speficic colour when printed to screen later on with the print_wordle() function.
        
        #Uppercase letters - Guessed correctly
        #Lowercase letters - Exist in the word but in the wrong place
        #lowercase letters prefixed with a dot - Dont exist in the word

                for a in range(len(wordle)):
                    if guess[a]==wordle[a]:  
                        #Letter guessed correctly
                        wordle_matrix[attempt][a]=guess[a].upper()+" "

                # Look for letters in the wrong place but are still used in the word
                for a in range(len(wordle)):
                    #Checks letters that haven't been gussed correctly
                    if wordle_matrix[attempt][a]=='- ':
                        #If letter exists somewhere else in word...
                        if guess[a] in wordle:
                            #...Make sure there is still a requirement to find this letter e.g havent found all the ocurrences of the letter
                            wordle_formatted=str(wordle_matrix[attempt]).lower()
                            if wordle_formatted.count(guess[a]) < wordle.count(guess[a].lower()):
                                wordle_matrix[attempt][a]=guess[a].lower()+" "
                            #If all occurences have been found then mark as incorrect gussed letter
                            else:
                                wordle_matrix[attempt][a]="."+guess[a].lower()+" "        
                        else:
                            #Letter not in wordle word
                            wordle_matrix[attempt][a]="."+guess[a].lower()+" "               
                print()

    def wrong_letters(self):
        #Updates a string containing all letters from users guesses that were not in the wordle word
        global bad_letters
        
        for a in range(len(wordle)):
            if guess[a] not in wordle: 
                if guess[a] not in bad_letters: 
                    bad_letters+=guess[a]+" "

    def finish_message(self):
        #Decide message to display when game finished
        global final_message,attempt
        if guess == wordle:
            final_message="\nCORRECT! " +praise[attempt]+"\n"
            attempt=6
        elif attempt == 5:
            final_message="\nUnlucky, word was "+ wordle.upper()+"\n"
            attempt=6
        else:
            attempt+=1

    def validation(self):
        #Raises custom exception if not a valid word
        if guess.isnumeric():
            raise validation_error("No numbers allowed")
        elif(len(guess)< 5):
            raise validation_error("To short")
        elif guess not in wordle_dictionary:
            raise validation_error("Not in wordle dictionary")
            
class validation_error(Exception):
        def __init__(self,err_message):
            self.message=err_message

        def error(self):
            return self.message

# Creating a wordle dictionary in the form of a list using a text file containing 12972 valid words
with open("C:\\Users\\miles\\OneDrive\\Desktop\\Python\\Progs\\letter-words.txt", 'r') as file:
    wordle_dictionary = file.read().splitlines()

praise=["Amazing","Impressive","Well done","Not bad","OK","Phew!"]
used_words=[]
wordle_turn=True
wordle_dict_len=len(wordle_dictionary)

#Enter loop to initiate the wordle game
while(wordle_turn):
    wordle_matrix=[['- ' for x in range(5)] for y in range(6)] #Wordle guess board
    attempt=0
    final_message=""
    bad_letters=""
    loop=True
    word_check=True
    wordle=wordle_dictionary[randint(0,len(wordle_dictionary)-1)].strip() #Choosing wordle word from dictionary
    
    #Checking randomly chosen wordle word hasnt been used before. Chooses new word if it has been used before
    while(word_check):
        if wordle in used_words:
            wordle=wordle_dictionary[randint(0,len(wordle_dictionary)-1)].strip()
        else:
            word_check=False    

    #Generate object for the class that contains the wordle tool set
    wordle_game=wordle_tools()

    ########################### Main part of program to play Wordle game ###########################
    while(loop):
        #If wordle game has finished display results and jump to section for playing another game..
        if attempt == 6:
            wordle_game.print_wordle() #Display board of previous Wordle guesses   
            print(final_message)
            loop=False
        #..Otherwise current game not finished, continue playing   
        else:      
            guess_input=True    

            while(guess_input):
                wordle_game.print_wordle() #Display board of previous Wordle guesses
              
                #Only display wrong letter guesses if they exist
                if attempt != 0:
                    print(f"\nBad letters: {bad_letters.upper()}")
            
                #User enters Wordle guess
                guess=input(f"\n\nPlease enter guess {attempt+1}:").lower()
               
                #Invokes function to check if users guess is a valid word (e.g word in the dictionary, 5 letters etc) 
                try:
                    wordle_game.validation()
                except validation_error as err:
                    #Custom exception displayed when guess isn't a valid word
                    print(f"\n{err}")
                    sleep(1.5)
                    guess_input=True
                else:
                    guess_input=False

            #Check how the users guess matches the chosen wordle word
            wordle_game.letter_matching()

            #Gathers all letters from users guesses that were not in the wordle word
            wordle_game.wrong_letters()

            #Decide message to display when game finished
            wordle_game.finish_message()

    #Put previous Wordle word into blacklist so it wont be used again
    used_words.append(wordle)

    #Play again section

    #If there are words in the wordle dictionary yet to be guseed then user is given option to play again
    if wordle_dict_len == len(used_words):
        print("You have exhausted the wordle dictionary!\n")
        wordle_turn=False
    else:
        #Play the game again?
        correct_input=True       

        while(correct_input):
            turn=input("Would you like another go? (Y/N)")
            turn=turn.upper()
            if turn == 'Y':
                correct_input = False
            elif turn == 'N':
                correct_input = False
                wordle_turn = False
                print()
