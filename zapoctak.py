from Board import Board
from AIplayer import AIplayer
from tkinter import *
import tkinter.ttk as ttk

#create board
board = Board()

#create GUI
master = Tk(className="Zápočťák - ConnectFour")
master.geometry("600x550")                                          #set window size
master.resizable(0, 0)                                              #disable window resize
myCanvas = Canvas(master, width=600, height=450, bd=0)              #create canvas for the game
 
#create UI elements
circleMatrix = [[0 for x in range(0,6)] for y in range(0,7)]        #2D array for the ID's of the circles
frameBottom = Frame(master)
frameLeft = Frame(frameBottom, width=100)
frameRight = Frame(frameBottom)
frameP1 = Frame(frameRight)
frameP2 = Frame(frameRight)
gameMode = IntVar()
#text elements
text=Label(frameP1, text = "You're up!", font=("TkHeadingFont", 15))    
text1=Label(frameP1, text = "Player 1", font=("TkHeadingFont", 25), foreground="green") 
text2=Label(frameP2, text = "", font=("TkHeadingFont", 15)) 
text3=Label(frameP2, text = "Player 2", font=("TkHeadingFont", 25), foreground="red")

#helper function to create circle
def create_circle(x, y, r, canvasName, **kwargs):
    x0 = x - r
    x1 = x + r
    y0 = y - r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, **kwargs)

#get the index of the row where the player clicked
def getRow(xpos):
    closest = 0
    closestdist = 1000
    for x in range(0,7):  
        val = abs(xpos - (75 + x*75))
        if(val < closestdist):
            closest = x
            closestdist = val
    return closest
       
#function that handles column highlighting
def on_motion(event):
    closest = getRow(event.x)
    for id in myCanvas.gettags("line"):
        myCanvas.itemconfigure(id, fill="#3d3d3d")

    tag = "line"+str(closest)
    item = myCanvas.find_withtag(tag)
    myCanvas.itemconfigure(item, fill = "gray")

#turns off colum highlight after the cursor left
def on_leave(event):
    for id in myCanvas.gettags("line"):
        myCanvas.itemconfigure(id, fill="#3d3d3d")

#function that handles updates of the game elements
def updateGUI():
    for x in range(0,7):   
        for y in range(0,6):
            if(board.stones[x][y] == 0):
                myCanvas.itemconfigure(circleMatrix[x][y], fill="#d6d6d6") 
            elif(board.stones[x][y] == 1):
                myCanvas.itemconfigure(circleMatrix[x][y], fill="green")
            else: 
                myCanvas.itemconfigure(circleMatrix[x][y], fill="red")
    if(board.victory==1):
        text.configure(text="Winner!")
        text2.configure(text="")
    elif(board.victory==2):
        text.configure(text="")
        text2.configure(text="Winner!")
    else:
        if(board.playerturn==1):
            text.configure(text="You're up!")
            text2.configure(text="")
        elif(board.playerturn==2):
            text.configure(text="")
            text2.configure(text="You're up!")

#restart the game
def restart():
    board.reset()
    updateGUI()
    print(str(gameMode))

#handles clicks inside the game canvas
def on_click(event):
    if(board.victory!=0):                           #if someone won the game - reset it
        board.reset()
    closest = getRow(event.x)
    if(board.placeStone(closest)):
        updateGUI()
    if(board.victory==0 and gameMode.get() == 2):      #switching between PVP and AI game
        choice = AIplayer.play(board)
        if(board.placeStone(choice)):  
            updateGUI()

#Create game canvas elemenets
for x in range(0,7):    
    line = myCanvas.create_line(75 + x*75,50,75 + x*75,405, width=70, capstyle=ROUND, tags=[("line"+str(x)),"line"], fill="#3d3d3d")    #create column lines on the background
    for y in range(0,6):
        circleMatrix[x][5-y] = create_circle(75 + x*75, 50 + y*71, 30, myCanvas, fill="#d6d6d6", width=0, tags="circle")                #create circles
#bind inputs to functions
myCanvas.bind('<Motion>', on_motion)     
myCanvas.bind('<Button-1>', on_click)       
myCanvas.bind('<Leave>', on_leave)   
myCanvas.pack()

#place frames for controls
frameBottom.pack(side=BOTTOM, fill=BOTH, expand=1)
frameLeft.pack(side=LEFT, fill=BOTH, expand=False)
frameRight.pack(side=RIGHT, fill=BOTH, expand=1)
frameP1.pack(side=LEFT, fill=BOTH, expand=1)
frameP2.pack(side=RIGHT, fill=BOTH, expand=1)

#position buttons
R1 = Radiobutton(frameLeft, text="Player vs Player", variable=gameMode, value=1, command=restart)
R1.pack( anchor = W, padx=35)
R2 = Radiobutton(frameLeft, text="Player vs AI", variable=gameMode, value=2, command=restart)
R2.pack( anchor = W, padx=35)
R = Button(frameLeft,  text="Restart", command=restart)
R.pack()
gameMode.set(1)

#place text elements
text.pack(side=TOP, expand=NO)
text1.pack(side=TOP, expand=NO)
text2.pack(side=TOP, expand=NO)
text3.pack(side=TOP, expand=NO)

#run
mainloop()