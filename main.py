import tkinter as tk
import random
import time
import simpleaudio as sa

GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 70
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

def gethighscore():
    with open("highscore.txt", "r") as f:
        return int(f.read())

def sethighscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def eatsound():
    file = "eat.wav"
    wave_obj = sa.WaveObject.from_wave_file(file)
    play_obj = wave_obj.play()

class Snake:
    def __init__(self):
        self.body = [
            [0, 0],
            [0, 1],
            [0, 2]
        ]
        self.direction = "RIGHT"
        self.changeDirectionTo = self.direction
        self.score = 0
        self.food = self.generateFood()
        self.gameOver = False
        self.paused = False
        self.speed = SPEED
        
    def generateFood(self):
        return [random.randrange(1, GAME_WIDTH // SPACE_SIZE - 1) * SPACE_SIZE, random.randrange(1, GAME_HEIGHT // SPACE_SIZE - 1) * SPACE_SIZE]

    def draw(self, canvas):
        for i in range(0, len(self.body)):
            if i == 0:
                canvas.create_rectangle(self.body[i][0], self.body[i][1], self.body[i][0] + SPACE_SIZE, self.body[i][1] + SPACE_SIZE, fill=SNAKE_COLOR, outline=SNAKE_COLOR)
            else:
                canvas.create_rectangle(self.body[i][0], self.body[i][1], self.body[i][0] + SPACE_SIZE, self.body[i][1] + SPACE_SIZE, fill=SNAKE_COLOR, outline=SNAKE_COLOR)
        canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + SPACE_SIZE, self.food[1] + SPACE_SIZE, fill=FOOD_COLOR, outline=FOOD_COLOR)

    def move(self):
        if self.paused:
            return
        if self.direction == "RIGHT":
            self.body.insert(0, [self.body[0][0] + SPACE_SIZE, self.body[0][1]])
        elif self.direction == "LEFT":
            self.body.insert(0, [self.body[0][0] - SPACE_SIZE, self.body[0][1]])
        elif self.direction == "UP":
            self.body.insert(0, [self.body[0][0], self.body[0][1] - SPACE_SIZE])
        elif self.direction == "DOWN":
            self.body.insert(0, [self.body[0][0], self.body[0][1] + SPACE_SIZE])
        if self.body[0] == self.food:
            eatsound()
            self.score += 1
            self.food = self.generateFood()
        else:
            self.body.pop()
        if self.body[0][0] > GAME_WIDTH or self.body[0][0] < 0 or self.body[0][1] > GAME_HEIGHT or self.body[0][1] < 0:
            self.gameOver = True
        for i in range(1, len(self.body)):
            if self.body[0] == self.body[i]:
                self.gameOver = True
        if self.gameOver:
            self.paused = True
            return
        self.direction = self.changeDirectionTo
        self.changeDirectionTo = self.direction

    def changeDirection(self, event):
        if event.keysym == "Up" and self.direction != "DOWN":
            self.changeDirectionTo = "UP"
        elif event.keysym == "Down" and self.direction != "UP":
            self.changeDirectionTo = "DOWN"
        elif event.keysym == "Left" and self.direction != "RIGHT":
            self.changeDirectionTo = "LEFT"
        elif event.keysym == "Right" and self.direction != "LEFT":
            self.changeDirectionTo = "RIGHT"
        elif event.keysym == "p":
            self.paused = not self.paused

    def reset(self):
        if self.score > gethighscore():
            sethighscore(self.score)
        self.__init__()

    def getScore(self):
        return self.score

    def getGameOver(self):
        return self.gameOver

    def getPaused(self):
        return self.paused

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed


class Food:
    def __init__(self):
        self.x = random.randint(0, GAME_WIDTH // SPACE_SIZE - 1)
        self.y = random.randint(0, GAME_HEIGHT // SPACE_SIZE - 2)
        self.draw(canvas)

    def draw(self, canvas):
        food_rect = canvas.create_rectangle(
            self.x * SPACE_SIZE,
            self.y * SPACE_SIZE,
            self.x * SPACE_SIZE + SPACE_SIZE,
            self.y * SPACE_SIZE + SPACE_SIZE,
            fill=FOOD_COLOR
        )

curtime = time.time()
formatedtime = time.strftime("%H:%M:%S", time.localtime(curtime))

print("[INFO] Initializing game... (" + str(formatedtime) + ")")
window = tk.Tk()
window.title("Snake")
window.resizable(False, False)
window.configure(background=BACKGROUND_COLOR)
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
print("[INFO] Game initialized! (" + str(formatedtime) + ")")

score = 0
direction = "right"

label = tk.Label(window, text=f"Score: {score}", font=("consolas", 20), bg=BACKGROUND_COLOR, fg="white")
label.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window.width = window.winfo_width()
window.height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{window.width}x{window.height}+{(screen_width - window.width) // 2}+{(screen_height - window.height) // 2}")

Snake = Snake()
Food = Food()

try:
    while True:
        if Snake.getGameOver():
            print("[INFO] Game over! (" + str(formatedtime) + ")")
            canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, text="Game Over", font=("consolas", 30), fill="white")
            canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 30, text=f"Score: {Snake.getScore()}", font=("consolas", 20), fill="white")
            canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 60, text=f"Highscore: {gethighscore()}", font=("consolas", 20), fill="white")
            window.update()
            time.sleep(1)
            Snake.reset()
            print("[INFO] Game reset! (" + str(formatedtime) + ")")
            continue
        else:
            window.bind("<KeyPress>", Snake.changeDirection)

            if Snake.getPaused == True:
                window.update()
                time.sleep(0.1)
                continue

            Snake.move()
            canvas.delete("all")
            Snake.draw(canvas)
            label.configure(text=f"Score: {Snake.getScore()}")
            window.update()
            time.sleep(SPEED/1000)

except Exception as e:
    print(e)
    exit()

window.mainloop()