from turtle import *
from random import randint, choice

# Налаштування екрану — фіксований розмір, не на весь екран
screen = getscreen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Спіймай Яблуко — Красива гра")
speed(0)
hideturtle()
tracer(0)

# Правила гри — виводимо зліва, не перекриваючи поле
rules = [
    "Правила гри СПІЙМАЙ ЯБЛУКО:",
    "1. Лови яблука кошиком унизу.",
    "2. Керуй стрілками ← та →.",
    "3. У тебе є 3 життя.",
    "4. Злови 5 яблук на рівні.",
    "5. Чорні яблука — мінус очки.",
    "6. Якщо яблуко торкнеться трави — програш."
]

# Виводимо правила зліва
for i, line in enumerate(rules):
    t = Turtle()
    t.hideturtle()
    t.penup()
    t.goto(-380, 250 - i * 30)
    t.color("white")
    t.write(line, font=("Arial", 14, "normal"))

# Допоміжні функції
def go_xy(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

def create_platform(x, y):
    parts = []
    for i in range(-2, 3):  # 5 частин
        t = Turtle()
        t.speed(0)
        t.shape("square")
        t.color("brown")
        t.shapesize(1, 2)  # ширша платформа
        t.penup()
        t.goto(x + i * 40, y)
        parts.append(t)
    return parts

def create_label(x, y, cl, text):
    t = Turtle()
    t.speed(0)
    go_xy(t, x, y)
    t.color(cl)
    t.write(text, font=("Arial", 18, "bold"))
    t.hideturtle()
    return t

def create_field():
    # фон — більший розмір
    color("#D6EAF8")
    go_xy(getpen(), -300, -250)
    begin_fill()
    for _ in range(2):
        forward(600)
        left(90)
        forward(500)
        left(90)
    end_fill()
    # трава — більша
    color("#229954")
    go_xy(getpen(), -300, -250)
    begin_fill()
    for _ in range(2):
        forward(600)
        left(90)
        forward(50)
        left(90)
    end_fill()

def is_collide(t1, t2):
    dif_x = abs(t1.xcor() - t2.xcor())
    dif_y = abs(t1.ycor() - t2.ycor())
    return dif_x <= 20 and dif_y <= 20

# Змінні гри
apples = []
loop_counter = 0
score = 0
lives = 3
level = 1
level_score = 0
game_running = True
levelLabel = None

# Створення об’єктів гри
create_field()
livesLabel = create_label(-280, 220, "red", "❤️❤️❤️")
scoreLabel = create_label(100, 220, "green", f"Зібрано: {score}")
platform = create_platform(0, -200)

def update_hearts():
    livesLabel.clear()
    livesLabel.write("❤️" * lives, font=("Arial", 18, "bold"))

def create_apple(level):
    apple = Turtle()
    if level >= 4 and randint(1,3) == 1:
        apple.color("black")
        apple.bad = True
    else:
        apple.color(choice(["red","green","yellow"]))
        apple.bad = False
    apple.shape("circle")
    apple.shapesize(1.5, 1.5)  # більші яблука
    apple.penup()
    apple.goto(randint(-280,280),220)
    apple.setheading(-90)
    apple.wind = choice([-1,1]) if level==3 else 0
    return apple

def move_platform(dx):
    for p in platform:
        new_x = p.xcor() + dx
        if -280 < new_x < 280:
            p.setx(new_x)

def move_right():
    if game_running:
        move_platform(40)

def move_left():
    if game_running:
        move_platform(-40)

def remove_apple(apple):
    if apple in apples:
        apple.hideturtle()
        apples.remove(apple)

def end_game(victory):
    global game_running
    game_running = False
    for p in platform:
        p.hideturtle()
    info = Turtle()
    info.penup()
    info.goto(-150,0)
    if victory:
        info.color("green")
        info.write("ПЕРЕМОГА!", font=("Arial", 40, "bold"))
    else:
        info.color("red")
        info.write("ПРОГРАШ!", font=("Arial", 40, "bold"))
        # Мигаючий текст
        def flash_text():
            if info.color() == "red":
                info.color("white")
            else:
                info.color("red")
            screen.ontimer(flash_text, 500)
        flash_text()
    info.hideturtle()
    update()

# Функція показу рівня
def show_level(level):
    global levelLabel
    if levelLabel:
        levelLabel.clear()
    levelLabel = Turtle()
    levelLabel.hideturtle()
    levelLabel.penup()
    levelLabel.goto(-50, 180)
    levelLabel.color("yellow")
    levelLabel.write(f"Рівень {level}", font=("Arial", 24, "bold"))
    screen.ontimer(lambda: levelLabel.clear(), 1500)

# Клавіші
screen.onkey(move_left,"Left")
screen.onkey(move_right,"Right")
screen.listen()

# Основна функція гри
def game_update():
    global score, lives, loop_counter, level, level_score, game_running

    if not game_running:
        return

    speed_factor = 1.5*(1+level)
    for apple in list(apples):
        apple.setx(apple.xcor()+apple.wind)
        apple.forward(speed_factor)

        caught = False
        for part in platform:
            if is_collide(apple,part):
                caught = True
                if apple.bad:
                    score = max(0, score-1)
                else:
                    score +=1
                    level_score +=1
                scoreLabel.clear()
                scoreLabel.write(f"Зібрано: {score}", font=("Arial", 18, "bold"))
                remove_apple(apple)
                break

        # якщо впало на траву
        if not caught and apple.ycor() < -200:
            end_game(False)
            return

    # перехід на наступний рівень
    if level_score >=5:
        level_score = 0
        level +=1
        for apple in list(apples):
            remove_apple(apple)
        if level >5:
            end_game(True)
            return
        show_level(level)

    # генеруємо нове яблуко через цикл
    loop_counter +=1
    if loop_counter > max(10,80-level*10):
        apples.append(create_apple(level))
        loop_counter =0

    update()
    screen.ontimer(game_update,50)

# Запуск гри
game_update()
screen.mainloop()