import pgzrun
from random import randint

score=0
message=""
gameover=False
apple=Actor("apple.png")

def draw():
    screen.clear()
    if gameover:
        screen.draw.text(message,(10,50),fontsize=30,color="white") #Gameover message print
    else:
        apple.draw()
        screen.draw.text(f"Score is: {score}",(10,10), fontsize=30, color="white")
        screen.draw.text(message,(10,50),fontsize=30,color="white") #good or bad shot in message
            

def place_apple():
    apple.x=randint(10,650)
    apple.y=randint(10,600)


clock.schedule_interval(place_apple,1.0)

def on_mouse_down(pos):
    global score,message,gameover
    if apple.collidepoint(pos):
        message="Good shot"
        score+=1
        print("good shot")
        place_apple()
    else:
        print("game over","Your score is:",score)
        message="You missed"
        score-=1
        place_apple()
        if score<0:
            gameover=True
            message="Game over"
            # print("Game over")
        
    
        
place_apple()
pgzrun.go()
        



