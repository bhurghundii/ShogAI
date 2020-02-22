'''
This file is the initial entry point for Shogi AI
Access is done through the bash file outside src startgame.sh
'''

from tkinter import Radiobutton, IntVar, filedialog, Label, W, CENTER, Button, PanedWindow, BOTH, SW, HORIZONTAL, E, PhotoImage, Frame
import tkinter as tk
from gameinitializer import GameInitializer
#What to do if the user sets themselves as black
#Basically, just sets one of the parameters as Black
def blackSelect(root2):
    print('Going black')
    root2.destroy()
    GameInitializer().run(False, True, 'Black')



#What to do if the user sets themselves as white
#Basically, just sets one of the parameters as White
def WhiteSelect(root2):
    print('Going white')
    root2.destroy()
    GameInitializer().run(False, True, 'White')

# Depending on which option the user chooses, we define different modes


def mode_selection():
    # 1 chooses to play against the AI
    if (selectionChoice.get() == 1):
        #GameInitializer().run(False, True)
        root.destroy()
        root2 = tk.Tk()
        root2.title("ShogAI: A Dissertation by Vikram Chhapwale")
        root2.geometry('800x550')

        sidebar = tk.Frame(root2, width=60, bg='white', height=500, relief='sunken', borderwidth=0)
        sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        #Assign background colors
        sidebar["bg"] = "#4ca64c"

        #Assign background colors
        root2["bg"] = "#303030"
        colorSelection = IntVar()

        T0 = Label(root2, text="Choose your color", 
            fg="white",
            bg="#303030",
            padx=10)

        T0.config(font=("Arial", 36))
        T0.pack(anchor=W)

        R1 = Radiobutton(
            root2,
            text="Black",
            variable=colorSelection,
            value=1,
            command=lambda:blackSelect(root2),
            highlightthickness = 0,
            fg='white',
            bg="#303030",
            padx=10,
            activebackground="#303030")
        R1.config(font=("Arial", 22))
        R1.pack(anchor=W)

        R2 = Radiobutton(
            root2,
            text="White",
            variable=colorSelection,
            value=2,
            command=lambda:WhiteSelect(root2),
            highlightthickness = 0,
            fg='white',
            bg="#303030",
            padx=10,
            activebackground="#303030")
        R2.config(font=("Arial", 22))
        R2.pack(anchor=W)

        root2.mainloop()
    # 2 chooses to play against another human player
    if (selectionChoice.get() == 2):
        # GameInitializer object where is where the game board and interactions
        # are instantiated
        GameInitializer().run(False, False)
    # 3 chooses to load a game and play from it
    if (selectionChoice.get() == 3):
        # FIXME: I don't like initialdir ... find a more universal method
        root.filename = filedialog.askopenfilename(
            initialdir="/home/ubuntu/Documents/Shogi-DISS/src/records/",
            title="mode_selectionect file",
            filetypes=(
                ("txt files",
                 "*.txt"),
                ("all files",
                 "*.*")))
        print('Preparing to load from ' + root.filename)
        # Read the game we want to load
        loadFile = open(root.filename, "r")
        replaygame = loadFile.read()
        loadFile.close()

        # Store the game we want to load into a temporary file we can access easily and manipulate
        # We load this into load_game, stored in ext_data
        # FIXME: In the future, this may be better written as some kind of
        # temporary file object.
        loadFile = open('ext_data/load_game.txt', "w")
        loadFile.write(replaygame)
        loadFile.close()
        # GameInitializer object where is where the game board and interactions
        # are instantiated
        GameInitializer().run(True, False, None, root.filename)

#This function erases the contents of the file in the directory ext_data
def reset_ext_data_file(FILENAME):
    resetFile = open('ext_data/' + FILENAME, "w", encoding='utf-8')
    resetFile.write('')
    resetFile.close

def writeALine(linetext, size):
    Tintro = Label(
        root,
        text=linetext,
        fg="white",
        bg="#303030",
        padx=20)
        
    Tintro.config(font=("Arial", size))
    Tintro.pack(anchor=W)

if __name__ == "__main__":
    try:
        # Reset the files that hold data which are games to load and the
        # immediate move to play
        reset_ext_data_file('load_game.txt')
        reset_ext_data_file('movetoplay.txt')    

        # Draw the menu user is greeted with when starting the program
        root = tk.Tk()
        root.title("ShogAI: A Dissertation by Vikram Chhapwale")
        root.geometry('800x550')
        selectionChoice = IntVar()

        sidebar = tk.Frame(root, width=50, bg='white', height=500, relief='sunken', borderwidth=0)
        sidebar.pack(expand=False, fill='both', side='left', anchor='nw')

        #Assign background colors
        root["bg"] = "#303030"
        sidebar["bg"] = "#4ca64c"

        #path = "assets/INTRO.png"
        #image = tk.PhotoImage(file=path)
        #label = tk.Label(image=image)
        #label.pack()

        T0 = Label(
            root,
            text="> Welcome to ShogAI",
            fg="white",
            bg="#303030",
            padx=20)
            
        T0.config(font=("Arial", 44))
        T0.pack(anchor=W)

        Tintro = Label(
            root,
            text="A framework to test and develop Shogi AI \n",
            fg="white",
            bg="#303030",
            padx=20)
            
        Tintro.config(font=("Arial", 20))
        Tintro.pack(anchor=W)

        writeALine('Version 0.3.0. New features include:', 16)
        writeALine('Framework to load models ', 12)
        writeALine('Revamped UI', 12)
        writeALine('Please support the work on the GitHub page! Provide your own models and use the API', 12)
        
        writeALine('\n', 40)

        T1 = Label(root, text="Pick a Game Mode", fg="white", bg="#303030", padx=20)

        T1.config(font=("Arial", 22))
        T1.pack(anchor=W)

        # Buttons the user can interact with are drawn
        R1 = Radiobutton(
            root,
            text="VS AI",
            variable=selectionChoice,
            value=1,
            command=mode_selection,
            highlightthickness = 0,
            fg='white',
            bg="#303030",
            activebackground="#303030",
            padx=20
            )
        R1.config(font=("Arial", 22))
        R1.pack(anchor=W)

        R2 = Radiobutton(
            root,
            text="VS Another Player",
            variable=selectionChoice,
            value=2,
            command=mode_selection,
            highlightthickness = 0,
            fg='white',
            bg="#303030",
            activebackground="#303030",
            padx=20)
        R2.config(font=("Arial", 22))
        R2.pack(anchor=W)

        R3 = Radiobutton(
            root,
            text="Load a game",
            variable=selectionChoice,
            value=3,
            command=mode_selection,
            highlightthickness = 0,
            fg='white',
            bg="#303030",
            activebackground="#303030",
            padx=20)
        R3.config(font=("Arial", 22))
        R3.pack(anchor=W)

        R4text = tk.StringVar()

       


        # Set up the activity loop
        root.mainloop()
    except Exception as errormessage:
        print(errormessage)
        print('Caught exception CTRL-C: Terminating ShogAI gracefully')
