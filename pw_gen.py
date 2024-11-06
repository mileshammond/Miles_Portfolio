#GUI frontend utilses bespoke module to generate complex password

#By Miles Hammond

from passwords import generator # Imports 'Generator' function from 'passwords' module to generate password
from tkinter import *
from tkinter import ttk
import pyperclip 

top = Tk()
number_checkbox = BooleanVar()  
upper_checkbox = BooleanVar()
lower_checkbox = BooleanVar()
duplicate_checkbox = BooleanVar()
special_checkbox = BooleanVar()
password_size=IntVar()
sizes=[]

#Generate number range for the password size combo box
for size in range(6,41):
     sizes.append(size)

top.geometry("720x320")
top.title("Security")
top.config(bg="lightyellow")

def begin():
     #Function calls module to generate password based on the GUI chosen options
     t1.delete("1.0", END)
     t1.insert(END,generator(size=password_size.get(),lower=lower_checkbox.get(),upper=upper_checkbox.get(),numbers=number_checkbox.get(),duplicate=duplicate_checkbox.get(),special=special_checkbox.get()))
     t1.tag_configure("tag_name", justify='center')
     t1.tag_add("tag_name", "1.0", "end")

def copy():
     #Function copies the generated password to the system clipboard
     pyperclip.copy(t1.get('1.0', 'end-1c'))

#Display GUI layout to select options for generating a complex password
t1 = Text(top,  height = 1, width = 50,font=("Arial",16))   
t1.place(x=70,y=100)  
title = Label(top,text="Generate a strong password!",font=("Arial",25),bg="lightyellow",fg="black") 
title.place(x=160,y=30)

#Buttons
B = Button(top, width = 15, text ="Generate password", command = begin)
B.place(x=230,y=250)
copy = Button(top, width = 15, text ="Copy to clipboard", command = copy)
copy.place(x=400,y=250)

#Checkboxes
numerical = Checkbutton(top, text = "Numbers", variable = number_checkbox, font=("Arial",12),bg="lightyellow",fg="black",height = 2, width = 10)  
numerical.place(x=200,y=150)
lowerletters = Checkbutton(top, text = "Lowercase", variable = lower_checkbox, font=("Arial",12),bg="lightyellow",fg="black",height = 2, width = 10)  
lowerletters.place(x=320,y=150)
upperletters = Checkbutton(top, text = "Uppercase", variable = upper_checkbox, font=("Arial",12),bg="lightyellow",fg="black",height = 2, width = 10)  
upperletters.place(x=430,y=150)
duplicates = Checkbutton(top, text = "Duplicate", variable = duplicate_checkbox, font=("Arial",12),bg="lightyellow",fg="black",height = 2, width = 10)  
duplicates.place(x=203,y=180)
special = Checkbutton(top, text = "Special", variable = special_checkbox, font=("Arial",12),bg="lightyellow",fg="black",height = 2, width = 10)  
special.place(x=310,y=180)

#Combo box
sizecombo = ttk.Combobox(state="readonly",textvariable=password_size, width=4)
sizecombo.set('6')
sizecombo['values']=sizes
sizecombo.place(x=440, y=190)
sizelabel = Label(text="Size",font=("Arial",12),bg="lightyellow",fg="black")
sizelabel.place(x=490,y=190)
top.mainloop()
