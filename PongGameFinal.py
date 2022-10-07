import turtle
import random


class QLearningPlayer():

    def __init__(self, epsilon=0.2, alpha=0.3, gamma=0.9):
        self.breed = "Qlearner"
        self.harm_humans = False
        self.q = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def available_moves(self, enviroment):
        return [0, 1, -1]

    def start_game(self, char):
        self.last_enviroment = (' ',) * 5
        self.last_move = None

    def getQ(self, state, action):
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 1.0
        return self.q.get((state, action))

    def move(self, enviroment):
        self.last_enviroment = tuple(enviroment)
        actions = self.available_moves(enviroment)

        if random.random() < self.epsilon:
            self.last_move = random.choice(actions)
            return self.last_move

        qs = [self.getQ(self.last_enviroment, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        self.last_move = actions[i]
        return actions[i]

    def reward(self, value, enviroment):
        if self.last_move:
            self.learn(self.last_enviroment, self.last_move,
                       value, tuple(enviroment))

    def learn(self, state, action, reward, result_state):
        prev = self.getQ(state, action)
        maxqnew = max([self.getQ(result_state, a)
                      for a in self.available_moves(state)])
        self.q[(state, action)] = prev + self.alpha * \
            ((reward + self.gamma*maxqnew) - prev)


p1 = QLearningPlayer()

# VENTANA:
ventana = turtle.Screen()  # Declaracion de la variable tipo ventana
# Nombre del titulo de la ventana
ventana.title("Pong Game por Brandon David Alvarez. ")
ventana.bgcolor("black")  # Color del fondo
ventana.setup(width=800, height=600)  # Tamaño de ventana
ventana.tracer(0)  # Hace que se vea todo más fluido

# Marcador(intentos):
intentos = 0
aciertos = 0
#marcador2 = 0

# Jugador 1:
jugador1 = turtle.Turtle()  # Crear Figura en el modulo Turtle
jugador1.speed(0)  # Aparece de manera instantanea
jugador1.shape("square")  # Forma del jugador u objeto
jugador1.color("white")  # Color del jugador u objeto
jugador1.penup()  # Evitar que se cree una linea en el rastro del objeto
jugador1.goto(-390, 0)  # Posicion inicial del jugador 1
# Tamaño del jugador u objeto
jugador1.shapesize(stretch_wid=5, stretch_len=1.5)

# Pelota:
pelota = turtle.Turtle()  # Crear Figura en el modulo Turtle
pelota.speed(0)  # Aparece de manera instantanea
pelota.shape("circle")  # Forma del jugador u objeto
pelota.color("red")  # Color del jugador u objeto
pelota.penup()  # Evitar que se cree una linea en el rastro del objeto
pelota.goto(0, 0)  # Posicion inicial del objeto
# Tamaño del jugador u objeto
pelota.shapesize(stretch_wid=0.8, stretch_len=0.8)

# Mover pelota:
pelota.dx = 0.3  # Cambio en X cada 3 pixeles.
pelota.dy = 0.3  # Cambio en y cada 3 pixeles.

# Texto de jugadores:
pen = turtle.Turtle()
pen.speed(0)
pen.color("lightgrey")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player QLearning, Fallas: {}".format(
    intentos, aciertos), align="center", font=("Lucida Console", 24, "normal"))

# Funciones para dar movimiento a los jugadores

def movement(move):
    y = jugador1.ycor()  # Obtencion de la coordeanada del jugador
    y += 5 * move  # Cada que se aumenta la Y en positivo se va hacia arriba
    jugador1.sety(y)  # Actualiza la coordenada en el eje Y
    # Actualiza la coordenada en el eje Y

while True:  # Bucle principal para evitar que la ventana se cierre automaticamente tan pronto se ejecute e juego
    ventana.update()

    # Aumentando coordenada X de la pelota por los 3 pixeles definidos arriba
    pelota.setx(pelota.xcor() + pelota.dx)
    # Aumentando coordenada X de la pelota por los 3 pixeles definidos arriba
    pelota.sety(pelota.ycor() + pelota.dy)

    enviroment = (int(pelota.xcor()), int(pelota.ycor()), int(jugador1.ycor()))
    movement(p1.move(enviroment))
    # Bordes:
    if pelota.ycor() > 290:
        pelota.dy *= -1
    if pelota.ycor() < -290:
        pelota.dy *= -1

    if (jugador1.ycor() + 5) > 290:
        # Asegura que el jugador no se salga de la pantalla.
        jugador1.sety(290)

    if (jugador1.ycor() + 5) < -290:
        # Asegura que el jugador no se salga de la pantalla.
        jugador1.sety(-290)

    # Bordes derecha/izquierda:

    if pelota.xcor() < -390:
        pelota.goto(0, 0)
        pelota.dx *= -1  # Hace que la pelota cuando pierde se vaya en direcciones invertidas
        intentos += 1
        pen.clear()  # Evita que se sobreescriba los datos impresos en pantalla
        pen.write("Player QLearning, Fallas: {}".format(
            intentos, aciertos), align="center", font=("Lucida Console", 24, "normal"))

    # Condiciones para el choque con las barras jugador 1 y jugador 2:
    if (pelota.xcor() > 340 and pelota.xcor() < 350):
        pelota.dx *= -1

    if (pelota.xcor() < -340 and pelota.xcor() > -350) and (pelota.ycor() < jugador1.ycor() + 50 and pelota.ycor() > jugador1.ycor() - 50):
        aciertos += 1
        pen.clear()
        pen.write("Player QLearning, Fallas: {}".format(
            intentos, aciertos), align="center", font=("Lucida Console", 24, "normal"))
        pelota.dx *= -1
