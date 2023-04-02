from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json

#----------------------------------------CONSTANTS-----------------------------------------------#
WHITE = "#FFFFFF"
DEFAULT_EMAIL = "my_name@email.com"

#-------------------------------------Declaring Window-------------------------------------------#
window = Tk()
window.title("Password Manager")
window.minsize(width=200,height=200)
window.config(padx=50,pady=50,bg=WHITE)

#---------------------------------------Setting Up UI----------------------------------------------#

#logo image
canvas = Canvas(width=200,height=200,bg=WHITE, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_image)
canvas.grid(column=1,row=0)

#entry boxes
website_input = Entry(width=34)
website_input.grid(column=1,row=1)
website_input.focus()

username_input = Entry(width=54)
username_input.grid(column=1,row=2, columnspan=2)
username_input.insert(0,DEFAULT_EMAIL)

password_input = Entry(width=34)
password_input.grid(column=1,row=3)

#labels
website_label = Label(text="Website:", font = ("Arial",10),bg=WHITE)
website_label.grid(column=0,row=1)

username_label = Label(text="Email/Username:", font = ("Arial",10),bg=WHITE)
username_label.grid(column=0,row=2)

password_label = Label(text="Password:", font = ("Arial",10),bg=WHITE)
password_label.grid(column=0,row=3)

#------------------------------------Defining Functions-------------------------------------------#
def is_valid():
    if len(website_input.get()) == 0 or len(username_input.get()) == 0 or len(password_input.get()) == 0:
        return False
    else:
        return True

def clear_form():
    website_input.delete(0,END)
    password_input.delete(0,END)
    username_input.delete(0,END)

def populate_form(website,user,pw):
    clear_form()
    website_input.insert(0,website)
    username_input.insert(0,user)
    password_input.insert(0,pw)

def generate_button_clicked():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*<>[]-+,.;:", k=20))
    pyperclip.copy(random_string)
    password_input.delete(0,END)
    password_input.insert(0,random_string)

def add_button_clicked():
    if is_valid():
        website = website_input.get()
        user = username_input.get()
        pw = password_input.get()
        #save_string = f"{website} | {user} | {pw}"
        new_data= {
            website: {
                "email": user,
                "password": pw,
            } 
        }
        is_ok = messagebox.askokcancel("Save?", f"Would you like to save?\n\nWebsite: {website}\nUser: {user}\nPassword: {pw}")
        if is_ok:
            try:
                with open("data.json", mode="r") as data_file:
                    #read data into a dictionary
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                #updating old data with new data
                data.update(new_data) 
                
                with open("data.json", mode="w") as data_file:
                    #update file
                    json.dump(data, data_file, indent=4)
            finally:
                clear_form()
                username_input.insert(0,DEFAULT_EMAIL)
    else:
        messagebox.showinfo("Something went wrong.", "Complete all fields.")
        
def search_button_clicked():
    website = website_input.get()
    print(website)
    try:
        with open("data.json", mode="r") as data_file:
            #read data into a dictionary
            data = json.load(data_file)
            print(data)
    except FileNotFoundError:
        messagebox.showinfo("Record not found.", "There are no records saved at this time.")
    else:
        if website in data:
            populate_form(website, data[website]["email"], data[website]["password"])
        else:
            messagebox.showinfo("Record not found.", f"{website} not found.")
    
#buttons
generate_button = Button(text="Generate Password", command=generate_button_clicked, width=15)
generate_button.grid(column=2,row=3)

add_button = Button(text="Add", command=add_button_clicked, width=45)
add_button.grid(column=1,row=4, columnspan=2)

clear_form_button = Button(text="Clear Form", command=clear_form, width=45)
clear_form_button.grid(column=1,row=5, columnspan=2)

search_button = Button(text="Search", command=search_button_clicked, width=15)
search_button.grid(column=2,row=1)

window.mainloop()    
