'''
This file is the initial entry point for Shogi AI
Access is done through the bash file outside src startgame.sh
'''

from tkinter import Radiobutton, IntVar, filedialog, Label, W, CENTER, Button, S, SW
import tkinter as tk
from gameinitializer import GameInitializer

# Depending on which option the user chooses, we define different modes


def mode_selection():
    # 1 chooses to play against the AI
    if (selectionChoice.get() == 1):
        #GameInitializer().run(False, True)
        import aisettings
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

if __name__ == "__main__":
    try:
        # Reset the files that hold data which are games to load and the
        # immediate move to play
        reset_ext_data_file('load_game.txt')
        reset_ext_data_file('movetoplay.txt')

        # Draw the menu user is greeted with when starting the program
        root = tk.Tk()
        root.title("ShogAI: A Dissertation by Vikram Chhapwale")
        root.geometry('600x550')
        selectionChoice = IntVar()

        path = "assets/INTRO.png"
        image = tk.PhotoImage(file=path)
        label = tk.Label(image=image)
        label.pack()

        T0 = Label(
            root,
            text="Welcome to ShogAI, a Dissertation by Vikramaditya Chhapwale from Nottingham \n")
        T0.pack(anchor=CENTER)

        T1 = Label(root, text="Pick a Game Mode")
        T1.pack(anchor=CENTER)

        # Buttons the user can interact with are drawn
        R1 = Radiobutton(
            root,
            text="VS AI",
            variable=selectionChoice,
            value=1,
            command=mode_selection)
        R1.pack(anchor=CENTER)
        R2 = Radiobutton(
            root,
            text="VS Another Player",
            variable=selectionChoice,
            value=2,
            command=mode_selection)
        R2.pack(anchor=CENTER)

        R3 = Radiobutton(
            root,
            text="Load a game",
            variable=selectionChoice,
            value=3,
            command=mode_selection)
        R3.pack(anchor=CENTER)

        R4 = Button(
            root,
            text="Language Options")
        R4.pack(anchor=SW)

        

        label = Label(root)
        label.pack()
        # Set up the activity loop
        root.mainloop()
    except Exception as errormessage:
        print(errormessage)
        print('Caught exception CTRL-C: Terminating ShogAI gracefully')
