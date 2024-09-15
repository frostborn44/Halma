from tkinter import *
import time

def main():
    global status
    global plyrCnt
    global clickCnt
    global movingCrds
    global lastCrds
    global destCrds
    global root
    global btnList
    global boardDim
    global redCamp
    global grnCamp
    global endRoot
    global leftLabel
    global rightLabel
    global timer
    global remTime
    global entry
    global tlimit

    '''
    Checks Win Status after each turn
    based on opposite colored peices on home squares
    '''
    def checkWin():
        global redCamp
        global grnCamp
        global plyrCnt
        global status
        global endRoot
        score = 0
        winner = ""
        #check red win
        if plyrCnt == 1:
            for rbtn in grnCamp:
                if rbtn.button.cget("background") != "red":
                        return False
            winner = "Red Wins!"
        #check green win
        elif plyrCnt == 0:
            for gbtn in redCamp:
                if gbtn.button.cget("background") != "green":
                        return False
            winner = "Green Wins!"
        status.configure(text="Game Over!")
        endRoot = Tk()
        Label(endRoot, text=winner).pack(side=TOP)
        Button(endRoot, text="New Game",command=lambda: newGame()).pack(side=LEFT)
        Button(endRoot, text="Exit",command=lambda: quitGame()).pack(side=RIGHT)

    '''
    Depending on the input time counts down players turn
    Switches turns when timer runs out
    '''
    def countDown():
        global remTime
        global timer

        if remTime <= 0:
            timer.configure(text="Time's up! Lost a Turn...")
             #unselect any selected pieces
            changeTurn()
            root.after(1000,countDown)
        elif remTime <= 4:
            timer.configure(text=str(remTime))
            if root.cget("background") == "white":
                root.configure(bg="misty rose")
            elif root.cget("background") == "misty rose":
                root.configure(bg="white")
            remTime = remTime - 1
            root.after(1000,countDown)
        else:
            timer.configure(text=str(remTime))
            remTime = remTime - 1
            root.after(1000,countDown)

    '''
    Runs new game
    '''
    def newGame():
        global endRoot
        global root
        endRoot.destroy()
        root.destroy()
        main()

    '''
    ends all board loops and quits program
    '''
    def quitGame():
        global endRoot
        global root
        endRoot.destroy()
        root.destroy()
        quit()

    '''
    Checks if attempting to move outside opposite home base
    Checks if move space directly next to start space
    Using DFS search checks if space is jumpable
    '''
    def canMove():
        global movingCrds
        global destCrds
        global boardDim
        global btnList
        global plyrCnt

        if plyrCnt == 0: # red
            # if green H and red bg, cant leave
            if ((btnList[(((movingCrds[1]-1)*boardDim.get())+movingCrds[0])-1].button.cget("text") == "H") and
            (btnList[(((movingCrds[1]-1)*boardDim.get())+movingCrds[0])-1].button.cget("foreground") == "lime green") and
            (btnList[(((destCrds[1]-1)*boardDim.get())+destCrds[0])-1].button.cget("text") != "H")):
                return False
        if plyrCnt == 1: # green
            # if red H and green bg, cant leave
            if ((btnList[(((movingCrds[1]-1)*boardDim.get())+movingCrds[0])-1].button.cget("text") == "H") and
            (btnList[(((movingCrds[1]-1)*boardDim.get())+movingCrds[0])-1].button.cget("foreground") == "dark red") and
            (btnList[(((destCrds[1]-1)*boardDim.get())+destCrds[0])-1].button.cget("text") != "H")):
                return False

        # find immediate neighbors of movingCrds
        jumps = [movingCrds]
        neighbors = [[-1,1], [0,1], [1,1],
                     [-1,0],        [1,0],
                     [-1,-1],[0,-1],[1,-1]]
        for neighbor in neighbors:
            if (movingCrds[0]+neighbor[0]) == destCrds[0] and (movingCrds[1]+neighbor[1]) == destCrds[1]:
                return True
        loopCntr = 0
        # Checks if first jumpable space is the goal
        # If not adds it to jumps queue to expand later
        # Checks all jumpable spaces, returning true if goal is found, else returning false
        while len(jumps) > 0:
            for crds in jumps:
                loopCntr += 1
                for neighbor in neighbors:
                    if ((crds[1]+neighbor[1]) > 0 and (crds[1]+neighbor[1]) <= boardDim.get()
                        and (crds[0]+neighbor[0]) > 0 and (crds[0]+neighbor[0]) <= boardDim.get()):
                        if (btnList[((((crds[1]+neighbor[1])-1)*boardDim.get())+
                                     (crds[0]+neighbor[0]))-1].button.cget("background") == "red" or
                        btnList[((((crds[1]+neighbor[1])-1)*boardDim.get())+
                                 (crds[0]+neighbor[0]))-1].button.cget("background") == "green"):
                            if (((((crds[1]+(2*neighbor[1]))-1)*boardDim.get())+
                                         (crds[0]+(2*neighbor[0])))-1 < len(btnList) and
                                ((btnList[((((crds[1]+(2*neighbor[1]))-1)*boardDim.get())+
                                         (crds[0]+(2*neighbor[0])))-1].button.cget("background") == "white" or
                            btnList[((((crds[1]+(2*neighbor[1]))-1)*boardDim.get())+
                                     (crds[0]+(2*neighbor[0])))-1].button.cget("background") == "gray"))):
                                if ((crds[0]+(2*neighbor[0])) == destCrds[0] and
                                (crds[1]+(2*neighbor[1])) == destCrds[1]):
                                    return True
                                if loopCntr > 100: return False
                                jumps.append([crds[0]+(2*neighbor[0]),crds[1]+(2*neighbor[1])])
                jumps.pop(0)

    '''
    Moves the current player's peice to the selected square if the move is valid
    Makes previous square grey
    '''
    def move():
        global btnList
        global plyrCnt
        global destCrds
        global lastCrds
        global movingCrds
        if lastCrds != [0,0]:
            btnList[(((lastCrds[1]-1)*boardDim.get())+lastCrds[0])-1].drawState(0)
        lastCrds = movingCrds
        if plyrCnt == 0:
            newPiece = 1
        if plyrCnt == 1:
            newPiece = 2
        btnList[(((destCrds[1]-1)*boardDim.get())+destCrds[0])-1].drawState(newPiece)
        btnList[(((movingCrds[1]-1)*boardDim.get())+movingCrds[0])-1].drawState(3)

    '''
    Changes player turn
    '''
    def changeTurn():
        global plyrCnt
        global leftLabel
        global rightLabel
        global clickCnt
        global remTime
        global tlimit

        if plyrCnt == 0:
            plyrCnt = 1
            rightLabel.configure(bg="white")
            leftLabel.configure(bg="yellow")
        elif plyrCnt == 1:
            plyrCnt = 0
            rightLabel.configure(bg="yellow")
            leftLabel.configure(bg="white")
        remTime = tlimit
        clickCnt = 0

    '''
    Decides what clicking each button does
    First decides who's turn it is
    If it's their turns first click, check if it is their piece
    If it's their turns second click, check to see if white/grey movable space
    Then run canMove() to check if valid
    '''
    def click(button): # remember, comp can use this
        global plyrCnt      # check for configure.bg
        global clickCnt
        global root
        global movingCrds
        global destCrds
        
        if plyrCnt == 0:
            movingPiece = "red"
            tmpMovePiece = "red4"
            nextPlyr = "Green"
        if plyrCnt == 1:
            movingPiece = "green"
            tmpMovePiece = "green2"
            nextPlyr = "Red"
        if clickCnt == 0:
            if button.button.cget("background") != movingPiece: # illegal: cant select nonpiece
                if button.button.cget("background") != tmpMovePiece:
                    status.configure(text="Illegal move! Select your piece.")
            if button.button.cget("background") == movingPiece or button.button.cget("background") == tmpMovePiece: # legal piece sel.
                if plyrCnt == 1: button.button.configure(bg="green2")
                if plyrCnt == 0: button.button.configure(bg="red4")
                status.configure(text="Select your move...")
                clickCnt = 1
                movingCrds = [button.getX(),button.getY()]
                return
        if clickCnt == 1:
            if button.getX() == movingCrds[0] and button.getY() == movingCrds[1]:
                clickCnt = 0
                button.button.configure(bg=movingPiece)
                return
            if button.button.cget("background") != "white" or button.button.cget("background") != "gray": # illegal: cant select nonempty
                status.configure(text="Illegal move! Select move.")
            if button.button.cget("background") == "white" or button.button.cget("background") == "gray": # legal move sel.
                destCrds = [button.getX(),button.getY()]
                if canMove():
                    move()
                    changeTurn()
                    checkWin()
                    status.configure(text="Nice move!")
                    root.update()
                    time.sleep(1)
                    status.configure(text=nextPlyr + "'s move")
        return

    '''
    Button class to hold extra placement variables
    Creates a button object for board, and assigns X and Y values to it
    '''
    class Btn:
        state = 0 # states: 0 = empty, 1 = red, 2 = green, 3 = gray
        x = 0
        y = 0
        button = None
        plyrCnt=0

        '''
        Initializes button
        '''
        def __init__(self,x,y,state,root):
            self.x = x
            self.y = y
            self.state = state
            if boardDim.get() == 16:
                self.button = Button(root, width=4,height=2, command=lambda: click(self))
            else:
                self.button = Button(root, width=6,height=3, command=lambda: click(self))
            self.button.grid(row=y,column=x)
            self.drawState(state)

        '''
        Draws button with correct color
        '''
        def drawState(self,state):
            if state == 0:
                self.state = 0
                self.button.configure(bg="white",activebackground="white")
            if state == 1:
                self.state = 1
                self.button.configure(bg="red",activebackground="red4")
            if state == 2:
                self.state = 2
                self.button.configure(bg="green",activebackground="green2")
            if state == 3:
                self.state = 3
                self.button.configure(bg="gray",activebackground="gray")

        '''
        Getters and Setters for coordinates
        '''
        def getX(self):
            return self.x

        def getY(self):
            return self.y

        def changePos(self,newX,newY):
            self.x = newX
            self.y = newY

    '''
    Initializes Play board based on user input
    '''
    def play(): # update with new starting amounts
        global status
        global root
        global btnList
        global boardDim
        global redCamp
        global grnCamp
        global leftLabel
        global rightLabel
        global timer
        global remTime
        global entry
        global tlimit

        remTime = entry.get()
        startRoot.destroy()
        root = Tk()
        root.title("Welcome to Halma!")
        root.configure(background="white")
        print("made root")
        letters = [" a "," b "," c "," d "," e "," f "," g "," h "," i "," j "," k "," l "," m "," n "," o "," p "," q "," r "," s "," t "," u "," v "," w "," x "," y "," z "]
        numbers = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26"] 

        # check if boardDim is unchecked
        if boardDim.get() == 0:
            boardDim.set(8)

        # Adds letters and numbers to side of board
        for x, letter in enumerate(letters):
            if x < boardDim.get():
                Label(root, text=letter).grid(row=0, column=(x+1))
                Label(root, text=letter).grid(row=(boardDim.get()+1), column=(x+1))
        for y, number in enumerate(numbers):
            if y == boardDim.get():
                break
            Label(root, text=number).grid(row=y+1, column=0)
            Label(root, text=number).grid(row=y+1, column=(boardDim.get()+1))
        print("made labels")

        # Places buttons on board, assinging them colors/letters depending on team/home base
        btnList = []
        for y in range(1,boardDim.get()+1):
            for x in range(1,boardDim.get()+1):
                tempState = 0
                bd = boardDim.get()
                # green places for 8x8, printed no matter what
                if (y==1 and x>(bd-4)) or (y==2 and x>(bd-3)) or (y==3 and x>(bd-2)) or (y==4 and x==bd):
                    tempState = 1
                # red places for 8x8, printed no matter what
                if (y==(bd-3) and x==1) or (y==(bd-2) and x<3) or (y==(bd-1) and x<4) or (y==bd and x<5):
                    tempState = 2
                # if boardDim>=10, color these buttons green
                if bd>=10 and ((x==1 and y==(bd-4)) or (x==2 and y==(bd-3)) or (x==3 and y==(bd-2)) or (x==4 and y==(bd-1)) or (x==5 and y==bd)):
                    tempState = 2
                # if boardDim>=10, color these buttons red
                if bd>=10 and ((x==(bd-4) and y==1) or (x==(bd-3) and y==2) or (x==(bd-2) and y==3) or (x==(bd-1) and y==4) or (x==bd and y==5)):
                    tempState = 1
                # if boardDim>=16, color these buttons green
                if bd>=16 and ((x==2 and y==(bd-4)) or (x==3 and y==(bd-3)) or (x==4 and y==(bd-2)) or (x==5 and y==(bd-1))):
                    tempState = 2
                # if boardDim>=16, color these buttons red
                if bd>=16 and ((x==(bd-4) and y==2) or (x==(bd-3) and y==3) or (x==(bd-2) and y==4) or (x==(bd-1) and y==5)):
                    tempState = 1
                btn = Btn(x,y,tempState,root)
                if tempState == 2:
                    btn.button.configure(text="H",fg ='lime green' ,relief=GROOVE)
                    grnCamp.append(btn)
                elif tempState == 1:
                    btn.button.configure(text="H",fg ='dark red' ,relief=GROOVE)
                    redCamp.append(btn)
                btnList.append(btn)
        print("made board buttons")

        # Sets player positions
        if humanCol.get() == 1:
            tempStrRight = "Player1"
            tempStrLeft = "Player2"
        else:
            tempStrRight = "Player2"
            tempStrLeft = "Player1"
        if remTime == "":
            remTime = "10"
        # Displays player turn and time limit
        leftLabel = Label(root,text=tempStrLeft,bg="yellow")
        leftLabel.grid(row=boardDim.get()+2,column=0,columnspan=3)
        rightLabel = Label(root,text=tempStrRight,bg="white")
        rightLabel.grid(row=boardDim.get()+2,column=boardDim.get()-1,columnspan=3)
        status = Label(root,text="Welcome to Halma!")
        status.grid(row=(boardDim.get()+3),columnspan=boardDim.get()+2)
        remTime = int(remTime)
        tlimit = remTime
        timer = Label(root,text=str(remTime),fg="red")
        timer.grid(row=boardDim.get()+4,columnspan=boardDim.get()+2)
        countDown()
        root.update()
        time.sleep(1)

        status.configure(text="Green's move...")

        root.mainloop()

    # start of main()
    startRoot = Tk()
    boardDim = IntVar()
    boardDim.set(0)
    humanCol = IntVar()
    remTime = ""
    tlimit = 0
    status = None
    btns = None
    clickCnt = 0 # piece selection is 0, move selection is 1
    plyrCnt = 1 # 0 is red turn, 1 is green turn
    lastCrds = [0,0]
    movingCrds = [0,0] # 1st click
    destCrds = [0,0] # 2nd click
    grnCamp = []
    redCamp = []
    endRoot = None
    leftLabel = None
    rightLabel = None
    entry = None

    # Initialize window for user to input game specifications
    Label(startRoot, text="Welcome to Halma!").grid(row=0,column=0)
    Label(startRoot, text="Choose Board Dimension:").grid(row=1, column=0)
    Radiobutton(startRoot, text="8X8", variable=boardDim, value=8).grid(row=1,column=1)
    Radiobutton(startRoot, text="10X10", variable=boardDim, value=10).grid(row=2,column=1)
    Radiobutton(startRoot, text="16X16", variable=boardDim, value=16).grid(row=3,column=1)
    Label(startRoot, text="Enter Time Per Turn:").grid(row=4, column=0)
    entry = Entry(startRoot)
    entry.grid(row=4, column = 1)
    Label(startRoot, text="Player1 Choose your color:").grid(row=5, column=0)
    Radiobutton(startRoot, text="Red", variable=humanCol, value=1).grid(row=5, column=1)
    Radiobutton(startRoot, text="Green", variable=humanCol, value=2).grid(row=6, column=1)
    Button(startRoot, text="Play Halma", command=lambda: play()).grid(row=7, column=0)

    startRoot.mainloop()

if __name__ == '__main__':
    main()
