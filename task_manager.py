# Note use the following username and password to access the admin rights 
# username: admin
# password: password
#=====importing libraries===========
import os
from datetime import datetime, date
import math

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file.
    - Use a while loop to validate your user name and password.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#menu options separated into distinct functions
def reg_user():
    '''In this block you will write code to add a new user to the user.txt file
    - You can follow the following steps:'''
    # - Request input of a new username
    while True:
        new_username = input("New Username: ")
        if new_username not in username_password:
            break
        print("Username already exists. Please enter a new username. ")


    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        username_password[new_username] = new_password
        #if username is in username_password dictionary, prints that it already exists. username and password is added to file
        if new_username in username_password:
            print("Username already exists. Please Enter a new username")
        else:
            print("New user added")
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")           



def add_task():
    '''In this block you will put code that will allow a user to add a new task to task.txt file
    - You can follow these steps:'''
    # - Prompt a user for the following: 
    #     - A username of the person whom the task is assigned to,
    #     - A title of a task,
    #     - A description of the task and 
    #     - the due date of the task.
    while True:
        task_username=get_username()
        if task_username in username_password.keys():
            break
        print("User does not exist. Please enter a valid username")

    task_title=get_title()
    task_description=get_discription()
    due_date_time=get_due_date()
    # - Then get the current date.
    curr_date = date.today()
    # - Add the data to the file task.txt and
    # - You must remember to include the 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    save_tasks(task_list)
    print("Task successfully added.")

def get_username():     #   functions separated from add_task block to allow for use in other sections
    return input("Name of person assigned to task: ")

def get_title():    
    return input("Title of Task: ")
    
def get_discription():    
    return input("Description of Task: ")
    
def get_due_date():  
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            return datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
    
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    
#   function to write to task file when requested
def save_tasks(task_list):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

def view_all():
    '''In this block you will put code so that the program will read the task from task.txt file and
        print to the console in the format of Output 2 presented in the task pdf (i.e. include spacing and labelling) 
        You can do it in this way:
        - Read a line from the file.
        - Split that line where there is comma and space.
        - Then print the results in the format shown in the Output 2 
        - It is much easier to read a file using a for loop.'''
    print("-----------------------------------")
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print("-----------------------------------")

def view_mine():
    '''In this block you will put code the that will read the task from task.txt file and
        print to the console in the format of Output 2 presented in the task pdf (i.e. include spacing and labelling)
        You can do it in this way:
        - Read a line from the file
        - Split the line where there is comma and space.
        - Check if the username of the person logged in is the same as the username you have
        read from the file.
        - If they are the same you print the task in the format of output 2 shown in the pdf '''
    print("-----------------------------------")
    filtered_task_list=[]                       #empty list for tasks with username
    for t in task_list:                         #for loop if tasks in task list 
        if t['username'] == curr_user:          #if the tasks' username is the same as the current user
            filtered_task_list.append(t)        #tasks get added to filtered list
    for i in range(len(filtered_task_list)):    #for loop along list of staks
        task=filtered_task_list[i]              #task is selected
        disp_str=f"Task no: \t {i+1}\n"         #number task number of determined and formatted correctly
        disp_str += f"Task: \t\t {task['title']}\n" #prints rest of task in correct format
        disp_str += f"Assigned to: \t {task['username']}\n"
        disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {task['description']}\n"
        print(disp_str)                          #string printed
        print("-----------------------------------")
    
    while True:     #option to allow user to select task or return to menu
        try:
            task_selection=int(input("Select task number or select -1 to go back: ")) 
            if task_selection==-1:              # returns to menu
                return
            if task_selection<1 or task_selection> len(filtered_task_list):
                print("Invalid Selection")          #if entered value is less than 1 or more than the length of user task list
            else:
                break                               #else breaks out of loop
        except ValueError:                          #if error occurs- invalid selection
            print("Invalid Selection")
    task=filtered_task_list[task_selection-1]       #chooses correct task no in list 


    while True:     #option to mark selected task as complete
        mark=input("Mark as complete?(Y/N): ").lower()
        if mark=="y":
            task["completed"]=True
            save_tasks(task_list)
            print("Task successfully amended.")
            break
        if mark=="n":
            break
        else:
            print("Invalid Selection")


    if task["completed"]:
        return

    while True:     #option to mend task if incomplete
        amend=input("Amend task? (Y/N): ").lower()
        if amend=="n":
            return
        if amend=="y":
            break
        else:
            print("Invalid Selection")


    while True: #option to change username. uses get username fuction 
        amend_username=input("Change username? (Y/N): ").lower()
        if amend_username=="n":
            break            
        if amend_username=="y":
            while True:
                task_username=get_username()
                if task_username in username_password.keys():
                    break
                print("User does not exist. Please enter a valid username")
            task["username"]=task_username
            save_tasks(task_list)
            print("Username successfully amended.")
            break
        else:
            print("Invalid Selection")


    while True: #option to change due date or return to menu. uses get get due date fuction 
        amend_due_date=input("Change due date? (Y/N): ").lower()
        if amend_due_date=="n":
            break            
        if amend_due_date=="y":
            due_date=get_due_date()
            task["due_date"]=due_date
            save_tasks(task_list)
            print("Task successfully amended.")
            break
        else:
            print("Invalid Selection")


def get_completed_tasks(task_list): #function to filter task list for completed tasks
    filter_list_comp=[]
    for task in task_list:                   
        if task['completed']:        
            filter_list_comp.append(task) 
    return filter_list_comp

def get_incomplete_tasks(task_list):    #function to filter task list for incomplete tasks
    filter_list_incomp=[]                  
    for task in task_list: 
        if not task['completed']:        
            filter_list_incomp.append(task) 
    return filter_list_incomp

def get_overdue_tasks(task_list):       #function to filter task list for overdue tasks
    filter_list_overd=[]
    for task in task_list:
        if task['due_date']> datetime.today():
            filter_list_overd.append(task) 
    return filter_list_overd

def get_overdue_incomplete_tasks(task_list):    #function to filter task list for overdue incomplete tasks
    filter_list_overd=get_overdue_tasks(task_list)
    filter_list_incomp_overd=[]
    for task in filter_list_overd:
        if not task['completed']:        
            filter_list_incomp_overd.append(task) 
    return filter_list_incomp_overd

#   task_overview.txt
#   total number of tasks generated
#   total number of completed tasks
#   total number of incomplete tasks
#   total number of overdue incomplete tasks
#   % incomplete tasks
#   % overdue incomplete tasks
def task_overview():                                #calls previous functions and returns as string of suitable format
    completed_tasks=get_completed_tasks(task_list)
    incomplete_tasks=get_incomplete_tasks(task_list)
    overdue_tasks=get_overdue_tasks(task_list)
    overdue_incomplete_tasks=get_overdue_incomplete_tasks(task_list)

    disp_str_TO="-----------------------------------"
    disp_str_TO+="\nTask overview\n"
    disp_str_TO+=f"Total number of tasks generated:\t\t{len(task_list)}\n"
    disp_str_TO+=f"Total number of completed tasks:\t\t{len(completed_tasks)}\n"
    disp_str_TO+=f"Total number of incomplete tasks:\t\t{len(incomplete_tasks)}\n"
    disp_str_TO+=f"Total number of overdue tasks:\t\t\t{len(overdue_tasks)}\n"
    disp_str_TO+=f"Total number of overdue incomplete tasks:\t{len(overdue_incomplete_tasks)}\n"
    disp_str_TO+=f"Percentage of incomplete tasks:\t\t\t{round((len(incomplete_tasks)*100)/(len(task_list)),2)}%\n"
    disp_str_TO+=f"Percentage of overdue incomplete tasks:\t\t{round((len(overdue_incomplete_tasks)*100)/(len(task_list)),2)}%\n"
    disp_str_TO+="-----------------------------------\n"
    return disp_str_TO

#   user_overview.txt
#   total number of regestered users
#   total number of tasks generated
#   for each user
#       total number assigned to user
#       % of tasks assigned to user
#       % of tasks completed
#       % of tasks to be completed
#       % of overdue incomplete tasks 
    
def user_overview():                    #calls previous functions and returns as string of suitable format
    disp_str_UO="-----------------------------------"   
    disp_str_UO+="\nUser overview\n"
    disp_str_UO+=f"Total number of regestered users:\t{len(username_password.keys())}\n"
    disp_str_UO+=f"Total number of tasks generated:\t{len(task_list)}\n"  
    disp_str_UO+="-----------------------------------"

# creats a filtered list for each user and runs it as a variable for each function

    for username in username_password.keys():
        disp_str_UO+=f"\nFor user- {username}:\n"
        filtered_list=[]
        for task in task_list:
            if task["username"]==username:
                filtered_list.append(task)
        completed_tasks=get_completed_tasks(filtered_list)
        incomplete_tasks=get_incomplete_tasks(filtered_list)
        overdue_incomplete_tasks=get_overdue_incomplete_tasks(filtered_list)
        
        disp_str_UO+=f"Total number of tasks assigned to {username}: \t\t\t{len(filtered_list)}\n"
        disp_str_UO+=f"Percentage of completed tasks assigned to {username}:\t\t{round((len(completed_tasks)*100)/(len(filtered_list)),2)}%\n"
        disp_str_UO+=f"Percentage of tasks to be completed assigned to {username}:\t\t{round((len(incomplete_tasks)*100)/(len(filtered_list)),2)}%\n"
        disp_str_UO+=f"Percentage of overdue incomplete tasks assigned to {username}:\t{round((len(overdue_incomplete_tasks)*100)/(len(filtered_list)),2)}%\n"
        disp_str_UO+="-----------------------------------"
    return disp_str_UO
user_overview()

def generate_reports(): #generates separate txt files for each overview in suitable format
    print("Reports successfully generated.")
    with open("task_overview.txt","w") as task_overview_file:
        task_overview_file.write(task_overview())
    with open("user_overview.txt","w") as user_overview_file:
        user_overview_file.write(user_overview())

def display_statistics():   #prints each overview in suitable format
    print(task_overview()+user_overview())


while True:
    #presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
: ''').lower()           

#   for tasks with same username with current user
    if menu=="r":       #user enters codeword which calls the correct function
        reg_user()
    elif menu=="a":
        add_task()
    elif menu=="va":
        view_all()
    elif menu=="vm":
        view_mine()
    elif menu=="gr":
        generate_reports()
    elif menu=="ds":
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")



