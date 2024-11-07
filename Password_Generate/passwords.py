#Module contains function for generating complex passwords
#User can import module and use function 'generator' for defining options to generate a password

#By Miles Hammond

from random import *
from os import system

gen_pw=[] #Generated Password 
counter=0

def character_choice(duplicate,char_choice):
    #Function generates a character for the password
    #Takes list parameter containing ASCII character range used for generating a character
    #Randomly chooses character from the list parameter

    global gen_pw,counter
    
    #Don't use function if character list parameter is empty and no characters left to generate
    if len(char_choice) == 0 or counter == 0:
        return
    else:
        # Allows duplicates if user selected this option
        if duplicate:
            #Adds character to password list by converting randomly choosen ASCII number from range
            #to the character equivalent
            gen_pw.append(chr(choice(char_choice))) 
            counter-=1
        else:
            loop=True
            #If user didnt allow duplicates then print single character
            while(loop): 
                #Converts randomly choosen ASCII number from range
                #to the character equivalent
                chosen=chr(choice(char_choice))
                
                #Add randomly chosen character to the password if it isnt already included
                #Otherwise loop around and try again!
                if chosen not in gen_pw:
                    gen_pw.append(chosen) #Adds character to password

                    #Removes character from list to prevent issues with generating larger password sizes
                    #Converts character back to ASCII number so it can be removed from the character list
                    char_choice.remove(ord(chosen)) 
                    counter-=1
                    loop=False                

def generator(size=12,duplicate=True,numbers=True,upper=True,lower=True,special=True):  
    '''       Password generator. 

       Default parameters produce a 12 character password potentially mixed with the following:

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
                    character_choice(duplicate,numerical) #Generates a number character
                if upper:
                    character_choice(duplicate,letters_upper) #Generates a uppercase character
                if lower:
                    character_choice(duplicate,letters_lower) #Generates a lowercase character
                if special:
                    character_choice(duplicate,special_char) #Generates a special character
                                
        shuffle(gen_pw) #Shuffles generated password to provide final effect of random generation
        return ''.join(gen_pw) #Convert the generated password list to a string and return to main GUI program

   