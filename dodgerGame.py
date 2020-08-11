
import Draw
import time
import random
import math

Draw.setCanvasSize(550, 550)    # create the size of the game board itself
Draw.setBackground(Draw.BLACK)  # draw backdrop of gameboard

# create a list that represents the five parameters for each bad guy:
# its location(x,y), size, speed, and color
def addGuys(num, guys): 
    # create a list of random color options
    colors = [Draw.RED, Draw.GREEN, Draw.BLUE, Draw.WHITE, Draw.VIOLET, Draw.YELLOW]
    
    for i in range(num):
        guys.append( [ random.randint(0,505), # x coord
                     0,                       # y coord 
                     random.randint(8,30),    # size 
                     random.random() +.5,     # speed
                     random.choice(colors)] ) # colors 
    return guys

# draw the bad guy using parameters from the list 'guys'
def drawGuys(guys):
    for g in guys:                           # for each bad guy in the list of 'guys'
        Draw.setColor(g[4])                  # choose a random color
        Draw.filledOval(g[0],g[1],g[2],g[2]) # draw the circle
        
# draw the clown on the canvas, at (x,y):
def drawPlayer(playerX,playerY):
    Draw.picture("clown.gif",playerX,playerY)

# update the list of 'guys' by removing from the list all guys that reached 
# bottom of screen. Move bad guys down the screen as the game continues. 
def updateGuys(guys,score):
    # ans is the resulting list of the new bad guys
    ans = []
    
    # if the bad guy has not reached the end of screen, append to new list 
    for g in guys:     # for each bad guy in the list 'guys'
        if g[1]<= 549: ans.append(g)
            
# move bad guys down the screen by adding to the y coord
    for g in ans:
        g[1] += g[3]  # increment the y coord of the bad guy by a random speed
        if score >=10: g[1]+= g[3] +.1 # as game continues, increases speed 
        if score >=20: g[1]+= g[3] +.1
        if score >=30: g[1]+= g[3] +.1
        if score >=40: g[1]+= g[3] +.1
        if score >=50: g[1]+= g[3] +.1

    return ans
    
# Draw the score in the corner of gameboard
def drawScore(score, gameOver = False):
    Draw.setFontSize(20)
    Draw.setFontBold(True)
    Draw.setFontFamily("Futura")
    Draw.setColor(Draw.YELLOW)
    if gameOver: Draw.string("SCORE:" + str(score), 230,250) 
    else: Draw.string("SCORE:" + str(score), 10,10)
    
# Draw best score in the corner of gameboard
def drawBestScore(bestScore,gameOver =False):
    Draw.setFontSize(20)
    Draw.setFontBold(True)
    Draw.setFontFamily("Futura")
    Draw.setColor(Draw.YELLOW)
    if gameOver:
        Draw.string("BEST SCORE:" + str(bestScore), 200,270) 
    else: Draw.string("BEST SCORE:" + str(bestScore), 10,30)

# Draw the gameboard 
def redrawScreen (guys,playerX,playerY,score,bestScore):
    # clear the screen
    Draw.clear()  
    
    # draw the bad guys
    drawGuys(guys)
    
    # Draw the clown in its new position
    drawPlayer(playerX,playerY)
    
    # Display score and best score
    drawScore(score)
    drawBestScore(bestScore)
   
    Draw.show()
    
# Return True if the clown intersects any side of an incoming bad guy
# If True is returned, the game is over and a scoreboard is drawn
def gameOver(playerX, playerY, guys, score, bestScore):
    for g in guys:   
        radGuy = g[2]/2         # radius of bad guys
        radClown = 18           # radius of clown
        
        # calculate the distance between clown and bad guys
        d = math.sqrt(((g[0]+(g[2]/2))-(playerX+25))**2 + \
                      ((g[1]+(g[2]/2)-(playerY+25))**2))
        
        if d < radGuy + radClown:
            drawScoreBoard(score, bestScore)
            return True
    return False

# Draw scoreboard for the end of game
def drawScoreBoard(score,bestScore):
    drawBestScore(bestScore, True)
    drawScore(score,True)
    Draw.string("OOPS! GAME OVER :(",160,210)
    Draw.show()
    time.sleep(5)

def playGame(bestScore):
    
    # initialize the starting position of clown
    playerX= 225 
    playerY= 505
    
    # initialize the starting list of bad guys, falling 2 at a time
    guys = []
    num=2 
    
    score = 0
    curTime = time.time()     #current time that game began
    scoreTime = time.time()
    
    # display the entire gameboard
    redrawScreen(guys,playerX,playerY,score,bestScore)
    
    # so long as the clown and a bad guy have not intersected...
    while not gameOver(playerX, playerY, guys, score, bestScore):
        
        # if the user touched any arrow key ...
        if Draw.hasNextKeyTyped():
            
            newKey = Draw.nextKeyTyped() # save the key that was pressed
            # increment the clown's x or y coord by 15 when arrow is pressed
            increment = 15               
            
            if newKey == "Right":
                playerX += increment
                if playerX >= 505: playerX = 505  #don't let clown go off board
            elif newKey == "Left":
                playerX -= increment
                if playerX <= 0:playerX = 0            
            elif newKey == "Up":
                playerY -= increment
                if playerY <=1:playerY = 1           
            elif newKey == "Down":
                playerY += increment
                if playerY >= 505: playerY = 505 
                
        # for each second the game continues, add 3 bad guys to the list
        if time.time() - curTime >= 1:
            guys = addGuys(3, guys)
            curTime = time.time()
            
        # as time is increasing, increment the score by 1 point and redraw it 
        # in the top left corner
        if time.time() - scoreTime >= 1: 
            score+=1
            scoreTime = time.time()
            drawScore(score)
        
        # if player exceeds the best score, save the new best score
        if score >= bestScore:
            bestScore = score
        
        # move bad guys to their new location
        guys = updateGuys(guys,score) 
        
        # redraw the whole game board
        redrawScreen(guys,playerX,playerY,score,bestScore) 
           
    return bestScore

def main():
    bestScore = 0
    while True:
        bestScore = playGame(bestScore)
main()
