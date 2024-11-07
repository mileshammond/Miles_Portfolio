#Module contains function for generating complex passwords
#User can import module and use function 'generator' for defining options to generate a password

#By Miles Hammond

from random import *
from os import system

gen_pw=[] #Generated Password 
counter=0

def character_choice(char_choice,use_duplicate=False):
    #Function generates a character for the password
    #The 'Char_choice' takes list parameter containing ASCII character range used for generating a single character
    #Randomly chooses character from the list parameter
    
    #The 'use_duplicate' is set to False by default. If True is provided as an argument then a character will be
    #duplicated from the password list and appended to it.

    global gen_pw,counter
    
    #Don't use function if character list parameter is empty or there are no characters left to generate...
    if len(char_choice) == 0 or counter == 0:
        return
    else:
    #...Otherwise generate a character
         if use_duplicate:
            #If duplicate is required then a character will be copied from the password list and appended to it...
            char_choice.append(choice(char_choice))
            counter-=1   
         else:
            #...Otherwise generate a unique character
            loop=True
            
            while(loop): 
                #Converts randomly choosen ASCII number from range
                #to the character equivalent
                chosen=chr(choice(char_choice))
                
                #Add randomly chosen character to the password if it isnt already included. Otherwise loop around and try again!
                if chosen not in gen_pw:
                    gen_pw.append(chosen) #Adds character to password

                    #Removes character from list to prevent issues with generating larger password sizes
                    #Converts character back to ASCII number so it can be removed from the character list
                    char_choice.remove(ord(chosen)) 
                    counter-=1
                    loop=False                

def generator(size=12,duplicate=True,numbers=True,upper=True,lower=True,special=True):  
    '''       Password generator. 

       Default parameters produce a 12 character password mixed with the following:

       Duplicate characters
       Numbers (0-9)
       Uppercase letters (A-Z)
       Lowercase letters (a-z)
       Special characters (!@#$%^&*()+) 

       Can manually set any of the parameters: 
       
       Password size
       Duplicate characters
       Numbers
       Uppercase letters
       Lowercase letters
       Special characters

       Example:

       size=15,duplicate=False,numbers=True,upper=True,lower=False,special=False
    '''
    global gen_pw,counter
    gen_pw=[]
    counter=0 
    counter=size
    char_total=0

    #Defining character lists (ASCII numbers represent screen character)
    numerical=list(range(48,58)) # 0 to 9
    letters_upper=list(range(65,91)) # A to Z
    letters_lower=list(range(97,123)) # a to z
    special_char=[33,64,35,36,37,94,38,42,40,41,43] # !@#$%^&*()+

    system("cls") # Clears terminal screen
    
    #Checks to see how many characters are available from the users requirements given
    if numbers: char_total+=len(numerical)
    if upper: char_total+=len(letters_upper)
    if lower: char_total+=len(letters_lower)
    if special: char_total+=len(special_char)

    #Checks user has selected minimum options for generating password
    if numbers == False and upper == False and lower == False and special == False:
        return "Please select at least one character option!"
    else:
        #Checks the chosen options are sufficient to generate the desired password size
        if size > char_total and not duplicate:
            return "Not enough characters for password without using duplicates!"
        else:       
            #Generate the password to match the size and character requirements specified by the user
            #Makes sure there is a fair distribution of character requiremnts with the generated password
            #Loop continues untill all characters for password have been generated

            while(counter>0):  
                if numbers:       
                    character_choice(numerical) #Generates a number character
                if upper:
                    character_choice(letters_upper) #Generates a uppercase character
                if lower:
                    character_choice(letters_lower) #Generates a lowercase character
                if special:
                    character_choice(special_char) #Generates a special character
                if duplicate:
                    character_choice(gen_pw,True) #Generates a duplicate character
                                
        shuffle(gen_pw) #Shuffles generated password to provide final effect of random generation
        return ''.join(gen_pw) #Convert the generated password list to a string and return to main GUI program

   