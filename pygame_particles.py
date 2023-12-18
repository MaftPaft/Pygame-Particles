import pygame as pg
import random

pg.init()

# screen display
w,h=400,300
win=pg.display.set_mode((w,h))

fps=120
# particle objects
class objs(object):
    def __init__(self,*args):
        self.args = list(args)

white,black=(255,255,255),(0,0,0)
# particles and data
ps=[]
data={}

run=True
clock=pg.time.Clock()
while run:
    # get mouse positions
    mx,my=pg.mouse.get_pos()
    # pygame events
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
        
        if i.type == pg.MOUSEBUTTONUP:
            if i.button == pg.BUTTON_LEFT:
                # object appending (vector x and y, velx, vely, lifespan) 100 times
                ps.extend(objs(pg.Vector2(mx,my),random.uniform(-1,1),random.uniform(-1,1),random.randint(2,5)) for x in range(100))
    win.fill(black)
    # delta time for the simulation to run a lot smoother
    dt=fps/(1+clock.get_fps())
    
    # particles loop
    for point in ps:
        p = point.args
        # data collected for drawing the particles
        if point not in data:
            data[point] = []

        # particle positions are changing by velocities multiplied by deltatime
        p[0].x += p[1]*dt
        p[0].y += p[2]*dt
        # particle gravity
        p[2] += 0.1
        # particle lifespan decreasing
        p[3]-=0.05
        # boundary collisions
        if p[0].x >= w-p[3] or p[0].x <= p[3]:
            p[1] *= -0.9
            if p[0].x > w-p[3]:
                p[0].x = w-p[3]
            elif p[0].x < p[3]:
                p[0].x = p[3]
        # boundary collisions
        if p[0].y >= h-p[3] or p[0].y <= p[3]:
            p[2] *= -0.9
            if p[0].y > h-p[3]:
                p[0].y = h-p[3]
            elif p[0].y < p[3]:
                p[0].y = p[3]
        # if lifespan <= 0 then remove particle
        if p[3] <= 0:
            ps.remove(point)
            data.pop(point)
    # drawing the particle, with lines from the data dict
    for a,b in data.items():
        p=a.args
        # append particles
        b.append([pg.Vector2(p[0].x,p[0].y),p[3]])
        for i in range(1,len(b)):
            # drawing particles
            pg.draw.line(win,white,(b[i][0].x,b[i][0].y),(b[i-1][0].x,b[i-1][0].y),int(b[i][1]))
            if b[i][1] > 0:
                b[i][1] -= 0.1

    pg.display.update()
    clock.tick(fps)
pg.quit()
