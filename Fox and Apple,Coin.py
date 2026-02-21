import pgzrun
from random   import randint

score = 0
gameover = False
timer=15

wolf=Actor("fox.png")
wolf.x=100
wolf.y=100

coin=Actor("coin.png")
coin.x=200
coin.y=200

apple=Actor("apple.png")
apple.x=300
apple.y=300


def draw():
    if gameover:
        screen.clear()
        screen.draw.text("Gameover", center=(400, 50), fontsize=40, color="yellow")
        screen.draw.text(f"Final Score: {score}", center=(400, 150), fontsize=50, color="white")
        screen.draw.text("Click Anywhere to start again", center=(400, 80), fontsize=40, color="yellow")

    else:
         screen.clear()
         wolf.draw()
         coin.draw()
         apple.draw()
         screen.draw.text(f"Score: {score}", topleft=(10,10), fontsize=30, color="white")
    
def timeup():
    global gameover
    gameover = True

def place_coin():
    coin.x=randint(20,500)
    coin.y=randint(20,400)

def place_apple():
    apple.x=randint(20,500)
    apple.y=randint(20,400)


def update():
    global score                                                                 
    if keyboard.left:
        wolf.x = wolf.x-5
    elif keyboard.right:
        wolf.x = wolf.x+5
    elif keyboard.up:
        wolf.y = wolf.y-5
    elif keyboard.down:
        wolf.y = wolf.y+5

    coincollected= wolf.colliderect(coin)
    applecollected=wolf.colliderect(apple)

    if coincollected:
        score += 10
        place_coin()
    elif applecollected:
        score+=20
        place_apple()

def on_mouse_down(pos):
    global gameover,score,timer
    if gameover:
        gameover=False
        score=0
        clock.schedule(timeup,timer)

        





clock.schedule(timeup,timer)
pgzrun.go()
