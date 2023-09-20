import pygame
import random
from tkinter import Tk, filedialog
import time

time.sleep(5)


class Button:
    def __init__(self, rect, text, textSize) -> None:
        self.rect = rect
        self.text = text
        self.textSize = textSize
        self.font = pygame.font.Font(None, self.textSize)
        self.text1 = self.font.render(self.text, True, pygame.Color("Black"))
        self.text_rect = self.text1.get_rect(
            center=(
                self.rect.x + self.rect.width / 2,
                self.rect.y + self.rect.height / 2,
            )
        )

    def update(self, mouseB, mousePos):
        if (
            mousePos[0] > self.rect.x
            and mousePos[0] < self.rect.x + self.rect.width
            and mousePos[1] > self.rect.y
            and mousePos[1] < self.rect.y + self.rect.height
            and mouseB[0] == True
        ):
            return True
        return False

    def draw(self, window, activity, color=pygame.Color("Blue")):
        if activity == True:
            pygame.draw.rect(window, color, self.rect)
        window.blit(self.text1, self.text_rect)


class Button2:
    def __init__(self, rect, text, textSize) -> None:
        self.rect = rect
        self.text = text
        self.textSize = textSize

    def update(self, mouseB, mousePos):
        if (
            mousePos[0] > self.rect.x
            and mousePos[0] < self.rect.x + self.rect.width
            and mousePos[1] > self.rect.y
            and mousePos[1] < self.rect.y + self.rect.height
            and mouseB[0] == True
        ):
            return True
        return False

    def draw(self, window):

        pygame.draw.rect(window, pygame.Color("White"), self.rect)
        pygame.draw.rect(window, pygame.Color("Black"), self.rect, 2)
        font = pygame.font.Font(None, self.textSize)
        text1 = font.render(self.text, True, pygame.Color("Black"))
        text_rect = text1.get_rect(
            center=(
                self.rect.x + self.rect.width / 2,
                self.rect.y + self.rect.height / 2,
            )
        )
        window.blit(text1, text_rect)


def quickCollide(pos, rect):
    if (
        pos[0] > rect.x
        and pos[0] < rect.x + rect.w
        and pos[1] > rect.y
        and pos[1] < rect.y + rect.h
    ):
        return True
    return False


class inputBox:
    def __init__(self, rect, limit, defaultText="Ukucaj tekst") -> None:

        self.font = pygame.font.Font(None, 32)
        self.input_box = rect
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("dodgerblue2")
        self.color = self.color_inactive
        self.active = False
        self.text = ""
        self.lines = [""]
        self.limit = limit
        self.maxCD = 100
        self.cd = self.maxCD

    def update_text(self, text, font, box_width):
        words = text.split(" ")
        lines = [""]
        for word in words:
            temp_line = lines[-1] + " " + word if lines[-1] else word
            temp_text = font.render(temp_line, True, self.color)
            if temp_text.get_width() <= box_width:
                lines[-1] = temp_line
            else:
                lines.append(word)
        return lines

    def update(self, mouseState, events, alwaysReturn=True):
        self.cd -= 1
        if self.active == True:
            a = 2
        if self.active == False:
            self.color = self.color_inactive
        for event in events:
            if mouseState[0] == True:
                mPos = pygame.mouse.get_pos()
                if quickCollide(mPos, self.input_box) and self.cd < 0:
                    self.active = not self.active
                    self.cd = self.maxCD
                    self.color = self.color_active
                else:
                    self.active = False

            if event.type == pygame.KEYDOWN:
                print("KD")
                if self.active == True:
                    print("ACTIVE")
                    if event.key == pygame.K_RETURN:
                        print(self.text)
                        a = self.text
                        self.text = ""
                        self.lines = [""]
                        print(a)
                        return a

                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        print("Text added")
                        if len(self.text) < self.limit:
                            self.text += event.unicode
                            self.text = self.text.upper()
                    self.lines = self.update_text(
                        self.text, self.font, self.input_box.width - 10
                    )
                    text_surface = self.font.render(self.text, True, (0, 0, 0))
                    while text_surface.get_width() > self.input_box.width - 10:
                        # Remove the last character until it fits
                        self.text = self.text[:-1]
                        text_surface = self.font.render(self.text, True, (0, 0, 0))

                    # if len(self.text) > 16:
                    #    self.text = self.text[:-1]
        if alwaysReturn:
            return self.text

    def draw(self, window):
        if self.text == "":
            txt_surface = self.font.render("Ukucaj rec", True, self.color)
            window.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        for i, line in enumerate(self.lines):
            txt_surface = self.font.render(line, True, self.color)
            window.blit(
                txt_surface, (self.input_box.x + 5, self.input_box.y + 5 + i * 32)
            )
        self.input_box.h = max(32, len(self.lines) * 32)
        pygame.draw.rect(window, self.color, self.input_box, 2)


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
                newB = Button(pygame.Rect(j*size,i*size,size,size),let,size)
                fakeButtonList.append(newB)
                
    if mode == "cir":
        for i in range(len(board)):
            for j in range(len(board[i])):
                let = cirilicaString[random.randint(0,len(cirilicaString)-1)]
                board[i][j] = let
                newB = Button(pygame.Rect(j*size,i*size,size,size),let,size)
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
    if depth == 50 or len(word)>=800//size:
        butts = []
        board,butts = updateFakeButtons(board, [], size, mode)
        return [board,butts,protected_spots]
    dirWeights = [7,13,12,15,15,13,7,10]
    choice = random.randint(0,92)
    dirs = [[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
    cumulative_weight = 0
    for i, weight in enumerate(dirWeights):
        cumulative_weight += weight
        if choice <= cumulative_weight:
            selected_dir = dirs[i]
            break
    
    

    wordLength = len(word)
    selectedDir = dirs[random.randint(0,7)]
    dirX = selectedDir[0]
    dirY = selectedDir[1]
    print(selectedDir)
    if dirX == 0:
        startX = random.randint(0,len(board)-1)
    
    if dirX == 1:
        startX = random.randint(0,len(board)-(wordLength))
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
    
    
def save_img(window,size):
    rect_x, rect_y, rect_width, rect_height = 0, 0, 800//size*size, 800//size*size
    # Create a subsurface from the main surface
    subsurface = window.subsurface(pygame.Rect(rect_x, rect_y, rect_width, rect_height))

    # Save the subsurface as a PNG file
    pygame.image.save(subsurface, "puzzle.png")


    startX = 0
    startY = 0
    

def updateFakeButtons(board,fakeButtonList,size,mode):
    if mode == "lat":
        for i in range(len(board)):
            for j in range(len(board[i])):
                let = board[i][j]
                newB = Button(pygame.Rect(j*size,i*size,size,size),let,size)
                fakeButtonList.append(newB)
                
    if mode == "cir":
        for i in range(len(board)):
            for j in range(len(board[i])):
                let = board[i][j]
                newB = Button(pygame.Rect(j*size,i*size,size,size),let,size)
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
            if [y,x] in thing and showAnswers:
                button.draw(window,True, color=colors[protected_spots.index(thing)])
                counter+=1
            else:
                button.draw(window,False)
            


def get_file_path():
    root = Tk()
    root.withdraw()  # Hide the root window
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Text files", "*.png"), ("All files", "*.*")])
    return save_path

SIZE = 32



button_regenerateText = Button2(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,100,150,50),"Regenerisi tabelu", 26)
button_confirmSetValue = Button2(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,300,150,50),"Potvrdi izmenu karaktera", 18)
button_showAnswers = Button2(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,600,150,50), "Prikazi resenja", 24)
button_save = Button2(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,700,150,50), "Sacuvaj", 24)



InputBox_valueToSet = inputBox(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8)+10,200,SIZE//2,50), 1)
InputBox_newWord = inputBox(pygame.Rect(800//SIZE*SIZE+((1000-800//SIZE*SIZE)//8),400,SIZE//2*800//SIZE*SIZE,50), 800//SIZE*SIZE)
setValue = ""
newWord = ""


protected_spots = []


protected_spots = []





"""
board,fakeButtonList,protected_spots = addWord("almonijak",board,SIZE,"lat",protected_spots) 

board,fakeButtonList,protected_spots = addWord("almonijak",board,SIZE,"lat",protected_spots)

board,fakeButtonList,protected_spots = addWord("testing",board,SIZE,"lat",protected_spots)

board,fakeButtonList,protected_spots = addWord("religija",board,SIZE,"lat",protected_spots)

board,fakeButtonList,protected_spots = addWord("sahmatira",board,SIZE,"lat",protected_spots)

board,fakeButtonList,protected_spots = addWord("hemizar",board,SIZE,"lat",protected_spots)

board,fakeButtonList,protected_spots = addWord("sahmatira",board,SIZE,"lat",protected_spots)

board,fakeButtonList,protected_spots = addWord("hemizar",board,SIZE,"lat",protected_spots)
"""

submenu_button_32 = menu_button_novo = Button2(pygame.Rect(300,200,400,200),"Velicina svakog polja 32", 32)
submenu_button_16 = menu_button_novo = Button2(pygame.Rect(300,550,400,200),"Velicina svakog polja 64", 32)


showAnswers = True
showAnswersMAXCD = 100
showAnswersCD = 100
frame = 0
menu_button_novo = Button2(pygame.Rect(300,200,400,200),"Kreni", 32)
menu_button_exit = Button2(pygame.Rect(300,550,400,200),"Zatvori Aplikaciju", 32)
game = False
while True:
    window.fill("White")
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    mouseState = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    if menu_button_novo.update(mouseState,mousePos):
        game = True
    if menu_button_exit.update(mouseState,mousePos):
        exit()
    
    menu_button_exit.draw(window)
    menu_button_novo.draw(window)
    
    pygame.display.update()
    
    while game:
        if frame == 0:
            wasHolding = True
            while True:
                window.fill("White")
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        exit()
                mouseState = pygame.mouse.get_pressed()
                mousePos = pygame.mouse.get_pos()
                
                if mouseState[0] == False:
                    wasHolding = False
                
                if submenu_button_32.update(mouseState,mousePos) and wasHolding == False:
                    SIZE = 32
                    break
                if submenu_button_16.update(mouseState,mousePos) and wasHolding == False:
                    SIZE = 64
                    break
                
                submenu_button_32.draw(window)
                submenu_button_16.draw(window)
                
                pygame.display.update()
            
            board = fillBoard(board,SIZE)
            board,fakeButtonList = randomFill(board, "lat", [], SIZE)
            selected_tile = [None,None]
            board,fakeButtonList,protected_spots = addWord("",board,SIZE,"lat",protected_spots)
        frame +=1
        print(frame)
        
        # Add words slowly
        """
        if frame == 200:
        board,fakeButtonList,protected_spots = addWord("almonijak",board,SIZE,"lat",protected_spots) 
        if frame == 200*2:
            board,fakeButtonList,protected_spots = addWord("almonijak",board,SIZE,"lat",protected_spots)
        if frame == 200*3:
            board,fakeButtonList,protected_spots = addWord("testing",board,SIZE,"lat",protected_spots)
        if frame == 200*4:
            board,fakeButtonList,protected_spots = addWord("religija",board,SIZE,"lat",protected_spots)
        if frame == 200*5:
            board,fakeButtonList,protected_spots = addWord("sahmatira",board,SIZE,"lat",protected_spots)
        if frame == 200*6:
            board,fakeButtonList,protected_spots = addWord("hemizar",board,SIZE,"lat",protected_spots)
        if frame == 200*7:
            board,fakeButtonList,protected_spots = addWord("sahmatira",board,SIZE,"lat",protected_spots)
        if frame == 200*8:
            board,fakeButtonList,protected_spots = addWord("hemizar",board,SIZE,"lat",protected_spots)
        if frame == 200*9:
            rect_x, rect_y, rect_width, rect_height = 0, 0, 800//SIZE*SIZE, 800//SIZE*SIZE
            # Create a subsurface from the main surface
            subsurface = window.subsurface(pygame.Rect(rect_x, rect_y, rect_width, rect_height))

            # Save the subsurface as a PNG file
            pygame.image.save(subsurface, "puzzle.png")
        """
        showAnswersCD -=1
        
        window.fill("White")
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        
        
        if selected_tile != [None,None]:
            pygame.draw.rect(window, pygame.Color("Blue"),pygame.Rect(selected_tile[0]*SIZE,selected_tile[1]*SIZE,SIZE,SIZE))
        mouseState = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if mouseState[0]:
            res2 = getTileClickedOn(mousePos,SIZE)
            if res2 != [None,None]:
                selected_tile = res2

        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_ESCAPE]:
            break
        
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
                newB = Button(pygame.Rect(selected_tile[0]*SIZE,selected_tile[1]*SIZE,SIZE,SIZE),setValue,SIZE)
                for button in fakeButtonList:
                    if button.rect.x == selected_tile[0]*SIZE and button.rect.y == selected_tile[1]*SIZE:
                        fakeButtonList.remove(button)
                fakeButtonList.append(newB)
        
        res3 = button_showAnswers.update(mouseState,mousePos)
        if res3 and showAnswersCD<0:
            showAnswers = not showAnswers
            showAnswersCD = showAnswersMAXCD
        
        res4 = button_save.update(mouseState,mousePos)
        if res4:
            file_path = get_file_path()
            rect_x, rect_y, rect_width, rect_height = 0, 0, 800//SIZE*SIZE, 800//SIZE*SIZE
            # Create a subsurface from the main surface
            subsurface = window.subsurface(pygame.Rect(rect_x, rect_y, rect_width, rect_height))

            # Save the subsurface as a PNG file
            if file_path != "":
                pygame.image.save(subsurface, file_path)
        #Buttons draw
        button_regenerateText.draw(window)
        button_confirmSetValue.draw(window)
        InputBox_valueToSet.draw(window)
        InputBox_newWord.draw(window)
        button_showAnswers.draw(window)
        button_save.draw(window)
        # End of draw
        
        #Button Update
        if button_regenerateText.update(mouseState,mousePos):
            board,fakeButtonList = randomFill(board, "lat", [], SIZE)
            protected_spots = []
            board,fakeButtonList,protected_spots = addWord("",board,SIZE,"lat",protected_spots)
        
        pygame.display.update()