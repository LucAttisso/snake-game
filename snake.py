import turtle, time, random

turtle.TurtleScreen._RUNNING = True

# Creation of the screen
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(600, 600)
screen.tracer(0)

# Creation of the snake head
head = turtle.Turtle()
head.shape("square")
head.shapesize(1.2, 1.2)
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"  # the attribute must exist before the first move()

# Creation of the body and the food
body = []
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Pen used for the game over message
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")

# Pen dedicated to the score display
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.color("white")
score_pen.goto(0, 260)

# Score and speed settings
score = 0
START_DELAY = 0.15  
MIN_DELAY = 0.04    
SPEED_STEP = 0.005 
delay = START_DELAY


def update_score():
    score_pen.clear()
    score_pen.write(f"Score: {score}",
                    align="center", font=("Arial", 16, "normal"))


# Moving and direction functions
# The snake cannot reverse onto itself
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

def random_food_position():
    # The food never appears on the snake
    while True:
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        if head.distance(x, y) >= 20 and all(p.distance(x, y) >= 20 for p in body):
            return x, y

screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

game_over = False
update_score()

while not game_over:
    screen.update()

    # Wall collision
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        game_over = True
        break

    # Eating the food
    if head.distance(food) < 20:
        food.goto(*random_food_position())
        part = turtle.Turtle()
        part.shape("square")
        part.color("green")
        part.penup()
        body.append(part)

        # Update the score and the speed
        score += 10
        delay = max(MIN_DELAY, delay - SPEED_STEP)
        update_score()

    # The body follows the head, from the tail to the front
    for i in range(len(body) - 1, 0, -1):
        body[i].goto(body[i - 1].xcor(), body[i - 1].ycor())

    if body:
        body[0].goto(head.xcor(), head.ycor())

    move()

    # Collision with the body
    for part in body:
        if head.distance(part) < 20:
            game_over = True
            break

    time.sleep(delay)  # NEW: the delay shrinks as the score grows

# Write the message once, refresh the screen, and keep the window open
pen.goto(0, 0)
pen.write("GAME OVER", align="center", font=("Arial", 24, "bold"))
screen.update()
screen.mainloop()