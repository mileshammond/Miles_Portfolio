#Module contains function for generating passwords
#User can import module and use function 'generator' for defining options to generate a password

#By Miles Hammond

from random import *
from os import system
import string

def generator(size=12,numbers=True,upper=True,lower=True,special=True):  
    '''       Password generator. 

       Default parameters produce a 12 character password mixed with the following:

       Numbers (0-9)
       Uppercase letters (A-Z)
       Lowercase letters (a-z)
       Special characters !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

       Can manually set any of the parameters when invoking the function: 
       
       Password size
       Numbers
       Uppercase letters
       Lowercase letters
       Special characters

       Example:

       size=15,numbers=True,upper=True,lower=False,special=False
    '''

    char_range=""
    gen_pw=""

    #Defining character lists
    numerical=string.digits # 0 to 9
    letters_upper=string.ascii_uppercase # A to Z
    letters_lower=string.ascii_lowercase # a to z
    special_char=string.punctuation # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

    system("cls") # Clears terminal screen

    #Checks user has selected minimum options for generating password
    if numbers == False and upper == False and lower == False and special == False:
        return "Please select at least one character option!"
    else:
        #Based on users options, compile a string of characters that will be used to generate a password 
        if numbers: char_range+="".join(numerical)           
        if upper: char_range+="".join(letters_upper)  
        if lower: char_range+="".join(letters_lower) 
        if special: char_range+="".join(special_char) 

        #Repeat the loop until the password includes at least one character from each of the users character options
        while(True):
            #Gnerates a password
            gen_pw="".join(choice(char_range) for a in range(size))
           
            #If user chose numbers and password doesn't include a number then stay in loop and generate password again
            if numbers and any(char.isnumeric() for char in gen_pw) == False: pass

            #If user chose uppercase letters and password doesn't include a uppercase letter then stay in loop and generate password again
            elif upper and any(char.isupper() for char in gen_pw) == False: pass

            #If user chose lowercase letters and password doesn't include a lowercase letter then stay in loop and generate password again
            elif lower and any(char.islower() for char in gen_pw) == False: pass

            #If user chose special characters and password doesn't include a special character then stay in loop and generate password again
            elif special and any(char in "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~" for char in gen_pw) == False: pass
            
            #If password has at least one character from each of the users character options then break loop and return to GUI
            else: break
   
        return gen_pw 