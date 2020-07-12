from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import random

class Snake:
    def __init__(self):
        self.head = [random.randint(left, right), random.randint(bottom, top)]
        self.direct = [1, 0]
        self.len = 1
        self.size = size
        self.body = [self.head]
        self.food = self.getFood()
        self.prev_key = GLUT_KEY_RIGHT

    def getFood(self):
        food = [random.randint(left, right), random.randint(bottom, top)]
        while food in self.body:
            food = [random.randint(left, right), random.randint(bottom, top)]
        return food

    def drawFood(self):
        glColor3f(174/255, 234/255, 0/255)
        glBegin(GL_POINTS)
        if(self.head == self.food):
            self.food = self.getFood()
        glVertex2iv(self.food)
        glEnd()

    def drawSnake(self):
        glPointSize(self.size)
        glColor3f(38/255, 50/255, 56/255)
        glBegin(GL_POINTS)
        for i in self.body:
            glVertex2fv(i)
        glEnd()

        glPointSize(self.size-2)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        for i in self.body:
            glVertex2fv(i)     
        glEnd()

    def animateSnake(self, timer):
        if(not self.isSelfHit() and self.inBoundry()):
            self.head[0] += self.direct[0]
            self.head[1] += self.direct[1]

            self.body.append(self.head.copy())
            self.body = self.body[1:]

            glutPostRedisplay()
            glutTimerFunc(TIMERSECS, self.animateSnake, 1)

    def isSelfHit(self):
        if(self.len > 4 and self.head in self.body[:-2]):
            return True
        return False
    
    def inBoundry(self):
        if( (self.head[0] < left) or (self.head[1] < bottom) or (self.head[0] > right) or (self.head[1] > top)):
            return False
        return True

    def control(self, key, x, y):
        if(key == GLUT_KEY_UP and self.prev_key != GLUT_KEY_DOWN):
            self.prev_key = GLUT_KEY_UP
            self.direct[0] = 0
            self.direct[1] = 1
        
        elif(key == GLUT_KEY_DOWN and self.prev_key != GLUT_KEY_UP):
            self.prev_key = GLUT_KEY_DOWN
            self.direct[0] = 0
            self.direct[1] = -1
        
        elif(key == GLUT_KEY_LEFT and self.prev_key != GLUT_KEY_RIGHT):
            self.prev_key = GLUT_KEY_LEFT
            self.direct[0] = -1
            self.direct[1] = 0
        
        elif(key == GLUT_KEY_RIGHT and self.prev_key != GLUT_KEY_LEFT):
            self.prev_key = GLUT_KEY_RIGHT
            self.direct[0] = 1
            self.direct[1] = 0

        glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    if(snake.head == snake.food):
        snake.body.append(snake.food)
        snake.len += 1
    snake.drawFood()
    snake.drawSnake()

    glutSwapBuffers()


def myinit():
    glClearColor(38/255, 50/255, 56/255, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(left, right, bottom, top)
    glMatrixMode(GL_MODELVIEW)
    

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowPosition(0,0)
    glutInitWindowSize(width, height)
    glutCreateWindow(b'Snake')
    glutDisplayFunc(display)
    myinit()
    glutSpecialFunc(snake.control)
    glutTimerFunc(TIMERSECS, snake.animateSnake, 1)
    glutMainLoop()


width, height = 200, 200
size = 20
left, right, bottom, top = 0.0, width/size, 0.0, height/size
TIMERSECS = 1000//5

snake = Snake()
main()