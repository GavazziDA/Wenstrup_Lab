#########################################################################################
#   This program was made to help analyze mouse audio channel information. To use, the  #
# file must start with "logfile-" and have the mouse name using 4 characters directly   #
# after. The file format is as follows:                                                 #
# _____________________________________________________________________________________ #
# \                                                                                   / #
# /                                                                                   \ #
# \                                                                                   / #
# /                                                                                   \ #
#                                                                                       #
#                                    Written by Daniel Gavazzi 8/11/2018                #
#########################################################################################

#The following are libraries that are to be used, if "import ... as [name]" is used, the
#library can be called using [name].function() 

import numpy as np                        #numpy is used for variouse array manipulation and math
import pylab as pyl                       #can be used like numpy, but mostly used to import data
import math as math                       #math is used for, well math(mostly exp or ln if needed)

import tkinter.filedialog as tk           #tkinter is used to create windows for a simple GUI(graphic user interface)
from tkinter import *
from tkinter import ttk         
from tkinter import messagebox

import sys 
import os                               #sys is used to run system comands/ exiting the program if needed
import re

col_chk = -2

folder_in = ''
file_out = ''  #File name to save data using

root = Tk()            #Creating a window environment to use

def check_in(*args):   
    #This function determines what happens when a button assigned this function is clicked
    global col_chk, folder_in, file_out    #Stating that these variables are used outside this function so that we can change them inside the function

    try:   #We are going to try the following
        #Getting the column information entered in the text boxes and converting them to integers 
        col_chk = int(C_x.get())-1 
        file_out = f_o.get()
        folder_in = tk.askdirectory(title="Folder To Save In")          #Folder to save data to 
        root.destroy()    #This will close out of the root window if the variables were successfully taken
    except ValueError:  #If what we tried failed, what is to be returned
        comment.set('Check your input')   #Changing the text to say 'Check your input'
        pass
   
root.title("Confirm column numbers")   #Setting the title of the window

#Making a frame to add the text/button to: mainframe is the window area that we will use, it's added to the root window 
#and has padding from top bottom left and right set to 4.  The grid is added to the mainframe such that there is only 1
#grid to worry about and it is mounted to all sides of the window (North, South, East, and West sides)

mainframe = ttk.Frame(root, padding="4 4 4 4")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#Adding variables that we will be able to use as text input
C_x = StringVar()
f_o = StringVar()  #File name to save data using

comment = StringVar()

#Adding text boxes to take the information and placing them in rows/columns of our grid

col_x_entry = ttk.Entry(mainframe, width=20, textvariable=C_x)
col_x_entry.grid(column=2, row=1, sticky=(W, E))

f_o_entry = ttk.Entry(mainframe, width=20, textvariable=f_o)
f_o_entry.grid(column=2, row=2, sticky=(W, E))

#Adding labels to the left of our text boxes to identify what input it's for

ttk.Label(mainframe, text="Column # to Check",width=20).grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Output File Name",width=20).grid(column=1, row=2, sticky=E)

#Adding an extra label for feedback if the entry fails

ttk.Label(mainframe, textvariable = comment).grid(column=1,row=4, sticky=W)

#Adding a button that assigns our 'check_in' function to be called

ttk.Button(mainframe, text="Submit", command=check_in).grid(column=2, row=4, sticky=W)

#Assigning everything that was just made to their propper spot in the window

for child in mainframe.winfo_children(): child.grid_configure(padx=4, pady=4)

col_x_entry.focus()  #Places the curser in the r_fr_entry text box
root.bind('<Return>', check_in)  #Assigns the function for pressing the 'Enter'/'Return' key

root.mainloop()  #Runs a loop that waits for the root window to close before continuing

#Making sure correct information was entered before root closed

#And now the program

files = os.listdir(folder_in)
files.sort()

nChan = 0

os.chdir(folder_in)

Mouse_name = ''

MainTxt = open('{0}-Combined-All.txt'.format(file_out),'w')
for n in range(len(files)):
    if not(files[n].startswith('logfile-')):
        continue

    nxt_file = files[n]
    if nChan == 0:
        if (Mouse_name != nxt_file[8:12]):
            if(Mouse_name != ''):
                txt.close()
                txt1.close()
                txt2.close()
            New_mouse = True
            Mouse_name = nxt_file[8:12]

        strt_found = False
        prop = 0
        strt = 0
        T_ind = [0,0] 
        B_ind = [0,0]
        for i in range(12,len(nxt_file)):
            if nxt_file[i] == '-':
                if strt_found:
                    if prop == 0:
                        Time_int = nxt_file[strt:i]
                        T_ind = [strt,i]
                        prop += 1
                        strt = i+1
                    else: 
                        Mouse_behave = nxt_file[strt:i]
                        B_ind = [strt,i]
                        break
                else:
                    strt_found = True
                    strt = i+1
        nChan = 1
    elif nChan == 1:
        if nxt_file[8:12] != Mouse_name:
            messagebox.showerror(title="Problem Has Happened",message="Could not find a pair for {0}".format(Mouse_name))
            nChan = 0
            continue
        if nxt_file[T_ind[0]:T_ind[1]] != Time_int:
            messagebox.showerror(title="Problem Has Happened",message="Could not find a pair for {0} due to Time Interval".format(Mouse_name))
            nChan = 0
            continue
        if nxt_file[B_ind[0]:B_ind[1]] != Mouse_behave:
            messagebox.showerror(title="Problem Has Happened",message="Could not find a pair for {0}-{1}".format(Mouse_name,Mouse_behave))
            nChan = 0
            continue
        nChan = 0
        if files[n-1].endswith('Ch1.txt'):
            file1 = '{0}'.format(files[n-1])
            file2 = '{0}'.format(files[n])
        else:
            file2 = '{0}'.format(files[n-1])
            file1 = '{0}'.format(files[n])
            
        EXIT_PRGM = False

        try:
            data1 = pyl.genfromtxt(file1, delimiter="\t")
        except:
            messagebox.showerror(title="Problem Has Happened",message="Could not import data from Channel 1\nMouse: {0}\n Behaviour: {1}\n Time Interval: {2}\n Exiting Program" \
                               .format(Mouse_name,Mouse_behave,Time_int))
            EXIT_PRGM = True
        try:
            data2 = pyl.genfromtxt(file2, delimiter="\t")
        except:
            messagebox.showerror(title="Problem Has Happened",message="Could not import data from Channel 2\nMouse: {0}\n Behaviour: {1}\n Time Interval: {2}\n Exiting Program" \
                               .format(Mouse_name,Mouse_behave,Time_int))
            EXIT_PRGM = True

        if EXIT_PRGM:
            messagebox.showerror(title="Problem Has Stopped The Program", message="Data Could Not Be Extracted As A Data Table, Stopping Program.")
            sys.exit()

        if New_mouse:
            txt = open('{0}-{1}-{2}.txt'.format(file_out,Mouse_name,Time_int),'w')
            txt1 = open('{0}-{1}-{2}-Ch1.txt'.format(file_out,Mouse_name,Time_int),'w')
            txt2 = open('{0}-{1}-{2}-Ch2.txt'.format(file_out,Mouse_name,Time_int),'w')
            New_mouse = False

        line_num = 0
        for Ch1_line, Ch2_line in zip(open(file1),open(file2)):
            l1 = Ch1_line.strip().split("\t")
            l2 = Ch2_line.strip().split("\t")
            behave = re.sub(r'[0-9]+','',(l1[-1].strip().split("-")[1]).split(".")[0])
            
            if data1[line_num,0]!=data2[line_num,0]:
                if data1[line_num,0]>data2[line_num,0]:
                    ErrorMsg = " Ch1 Has Extra Data:\n Mouse: {0}\n Behaviour: {1}\n Time Interval: {2}\n Wave File: '{3}'\n Exiting Program" \
                               .format(Mouse_name,Mouse_behave,Time_int,l1[-1])
                else:
                    ErrorMsg = " Ch2 Has Extra Data:\n Mouse: {0}\n Behaviour: {1}\n Time Interval: {2}\n Wave File: '...{3}'\n Exiting Program" \
                               .format(Mouse_name,Mouse_behave,Time_int,l2[-1])
                messagebox.showerror(title="Problem Has Happened",message=ErrorMsg)
                sys.exit()
            if data1[line_num,col_chk] > data2[line_num,col_chk]:
                txt.write('{0}\t{1}\t{2}\t{3}'.format(Mouse_name,behave,'Ch1',Ch1_line))
                MainTxt.write('{0}\t{1}\t{2}\t{3}'.format(Mouse_name,behave,'Ch1',Ch1_line))
            elif data1[line_num,col_chk] < data2[line_num,col_chk]:
                txt.write('{0}\t{1}\t{2}\t{3}'.format(Mouse_name,behave,'Ch2',Ch2_line))
                MainTxt.write('{0}\t{1}\t{2}\t{3}'.format(Mouse_name,behave,'Ch2',Ch2_line))
            else:
                txt.write('{0}\t{1}\t{2}\t{3}'.format(Mouse_name,behave,'Equal',Ch1_line))
                MainTxt.write('{0}\t{1}\t{2}\t{3}'.format(Mouse_name,behave,'Equal',Ch1_line))
            txt1.write('{0}\t{1}\t{2}\t{3}'.format(Mouse_name,behave,'Ch1',Ch1_line))
            txt2.write('{0}\t{1}\t{2}\t{3}'.format(Mouse_name,behave,'Ch2',Ch2_line))
            line_num += 1
MainTxt.close()
