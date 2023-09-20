import pygame
import random
import Button
import Button1
import InputBox



pygame.init()

window = pygame.display.set_mode((1000,800))

def drawGrid(window,size=16, color=pygame.Color("Black")):
    for i in range(800//size):
        for j in range(800//size):
            pygame.draw.rect(window, color, pygame.Rect(j*size,i*size, size,size), 1)


board = []

def fillBoard(board,size):
    for i in range(800//size):
        board.append([])
        for j in range(800//size):
            board[i].append("O")
    return board


def randomFill(board, mode, fakeButtonList,size):
    fakeButtonList = []
    latinicaString = "ČĆĐŠŽABVGDEFIJKLMNOPRSTUFHC"
    cirilicaString = "АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ"
    if mode == "lat":
        for i in range(len(board)):
            for j in range(len(board[i])):
                let = latinicaString[random.randint(0,len(latinicaString)-1)]
                board[i][j] = let
                newB = Button.Button(pygame.Rect(j*size,i*size,size,size),let,size)
                fakeButtonList.append(newB)
                
    if mode == "cir":
        for i in range(len(board)):
            for j in range(len(board[i])):
                let = cirilicaString[random.randint(0,len(cirilicaString)-1)]
                board[i][j] = let
                newB = Button.Button(pygame.Rect(j*size,i*size,size,size),let,size)
                fakeButtonList.append(newB)              

            
    
    return [board,fakeButtonList]

fakeButtonList = []

def textOverlay(board,size):
    for i in range(800//size):
        for j in range(800//size):
            pass


def getTileClickedOn(mousePos,size):
    if mousePos[0] > 795//size*size:
        return [None,None]
    if mousePos[1] > 795//size*size:
        return [None,None]
    return [mousePos[0]//size,mousePos[1]//size]
    
    

def addWord(word,board,size,mode,protectedSpots,depth=0):
    if depth == 50:
        butts = []
        board,butts = updateFakeButtons(board, [], size, mode)
        return [board,butts,protected_spots]
    dirs = [[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    wordLength = len(word)
    selectedDir = dirs[random.randint(0,7)]
    dirX = selectedDir[0]
    dirY = selectedDir[1]
    print(selectedDir)
    if dirX == 0:
        startX = random.randint(0,len(board)-1)
    
    if dirX == 1:
        startX = random.randint(0,len(board)-(wordLength+1))
    if dirX == -1:
        startX = random.randint(wordLength,len(board)-1)
    
    if dirY == 0:
        startY = random.randint(0,len(board)-1)
    
    if dirY == 1:
        startY = random.randint(0,len(board)-(wordLength+1))

    if dirY == -1:
        startY = random.randint(wordLength,len(board)-1)
    
    for thing in protected_spots:
        for i in range(len(word)):
            if [startY+selectedDir[1]*i,startX+selectedDir[0]*i] in thing:
                return addWord(word,board,size,mode,protectedSpots,depth+1)
        
    
    
    protected_spots.append([])
    for i in range(len(word)):
        board[startY+selectedDir[1]*i][startX+selectedDir[0]*i] = word[i]
        protected_spots[-1].append([startY+selectedDir[1]*i,startX+selectedDir[0]*i])
    
    butts = []
    board,butts = updateFakeButtons(board, [], size, mode)
    
    return [board,butts,protected_spots]
    
    



    startX = 0
    startY = 0
    

def updateFakeButtons(board,fakeButtonList,size,mode):
    if mode == "lat":
        for i in range(len(board)):
            for j in range(len(board[i])):
                let = board[i][j]
                newB = Button.Button(pygame.Rect(j*size,i*size,size,size),let,size)
                fakeButtonList.append(newB)
                
    if mode == "cir":
        for i in range(len(board)):
            for j in range(len(board[i])):
                let = board[i][j]
                newB = Button.Button(pygame.Rect(j*size,i*size,size,size),let,size)
                fakeButtonList.append(newB)   
    return board,fakeButtonList
    


def drawFakeButtons(fakeButtonList,window,showAnswers,protected_spots):
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 255),  # Cyan
        (255, 0, 255),  # Magenta
        (128, 128, 128),# Grey
        (128, 0, 0),    # Maroon
        (0, 128, 0),    # Dark Green
        (0, 0, 128),    # Navy
        (128, 128, 0),  # Olive
        (0, 128, 128),  # Teal
        (128, 0, 128),  # Purple
        (192, 192, 192),# Silver
        (255, 165, 0),  # Orange
        (64, 224, 208), # Turquoise
        (210, 180, 140),# Tan
        (154, 205, 50), # Yellow Green
        (255, 192, 203),# Pink
        (148, 0, 211),  # Dark Violet
        (0, 206, 209),  # Dark Turquoise
        (255, 215, 0),  # Gold
        (255, 140, 0),  # Dark Orange
        (178, 34, 34),  # Firebrick
        (107, 142, 35), # Olive Drab
        (112, 128, 144),# Slate Grey
        (72, 61, 139)   # Dark Slate Blue
        ]
    counter = 0
    for button in fakeButtonList:
        x = button.rect.x//SIZE
        y = button.rect.y//SIZE
        for thing in protected_spots:
            if [y,x] in thing:
                button.draw(window,True, color=colors[protected_spots.index(thing)])
                counter+=1
            else:
                button.draw(window,False)
            



SIZE = 64
board = fillBoard(board,SIZE)
board,fakeButtonList = randomFill(board, "lat", [], SIZE)
selected_tile = [None,None]



#buttons
button_regenerateText = Button1.Button(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,100,150,50),"Regenerate", 32)
button_confirmSetValue = Button1.Button(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,300,150,50),"Confirm replace", 24)
button_addNewWord = Button1.Button(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,500,150,50),"Confirm replace", 24)


InputBox_valueToSet = InputBox.inputBox(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,200,SIZE//2,50), 1)
InputBox_newWord = InputBox.inputBox(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8),400,SIZE//2*6,50), 20)
setValue = ""
newWord = ""


protected_spots = []



board,fakeButtonList,protected_spots = addWord("almonijak",board,SIZE,"lat",protected_spots)
board,fakeButtonList,protected_spots = addWord("testing",board,SIZE,"lat",protected_spots)
board,fakeButtonList,protected_spots = addWord("religija",board,SIZE,"lat",protected_spots)
board,fakeButtonList,protected_spots = addWord("sahmatira",board,SIZE,"lat",protected_spots)
board,fakeButtonList,protected_spots = addWord("hemizar",board,SIZE,"lat",protected_spots)
board,fakeButtonList,protected_spots = addWord("sahmatira",board,SIZE,"lat",protected_spots)
board,fakeButtonList,protected_spots = addWord("hemizar",board,SIZE,"lat",protected_spots)
#board,fakeButtonList,protected_spots = addWord("hell",board,SIZE,"lat",protected_spots)
showAnswers = True

while True:
    window.fill("White")
    events = pygame.event.get()
    if selected_tile != [None,None]:
        pygame.draw.rect(window, pygame.Color("Blue"),pygame.Rect(selected_tile[0]*SIZE,selected_tile[1]*SIZE,SIZE,SIZE))
    mouseState = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    if mouseState[0]:
        res2 = getTileClickedOn(mousePos,SIZE)
        if res2 != [None,None]:
            selected_tile = res2

    drawFakeButtons(fakeButtonList,window,showAnswers,protected_spots)
    drawGrid(window,SIZE)
    
    # Buttons update
    res = InputBox_valueToSet.update(mouseState,events)
    res2 = InputBox_newWord.update(mouseState,events,False)
    if res != None and res != "":
        setValue = res
    if res2 != None and res2 != "":
        board,fakeButtonList,protected_spots = addWord(res2,board,SIZE,"lat",protected_spots)
    
        
        
    if button_confirmSetValue.update(mouseState,mousePos):
        if selected_tile != [None,None]:
            board[selected_tile[1]][selected_tile[0]] = setValue
            newB = Button.Button(pygame.Rect(selected_tile[0]*SIZE,selected_tile[1]*SIZE,SIZE,SIZE),setValue,SIZE)
            for button in fakeButtonList:
                if button.rect.x == selected_tile[0]*SIZE and button.rect.y == selected_tile[1]*SIZE:
                    fakeButtonList.remove(button)
            fakeButtonList.append(newB)
    
    
    
    #Buttons draw
    button_regenerateText.draw(window)
    button_confirmSetValue.draw(window)
    InputBox_valueToSet.draw(window)
    InputBox_newWord.draw(window)
    # End of draw
    
    #Button Update
    if button_regenerateText.update(mouseState,mousePos):
        pass
        # board,fakeButtonList = randomFill(board, "lat", [], SIZE)
    
    pygame.display.update()
    