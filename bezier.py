import matplotlib.pyplot as plt
import numpy as np
import pygame as pg

pg.init()
screen = pg.display.set_mode((1500, 900))
pg.display.set_caption("Bezier Curves")

points = []
g_plus = []
g_minus = []
dragging = False


def drawPoint(screen, x, y, color="white"):
    pg.draw.circle(screen, color, (x, y), 3)

def drawLine(screen, p, q, color="white"):
    pg.draw.line(screen, color, p, q)

def drawCurve(screen, x_t, y_t, t0=0, t1=1):
    pts = [[x_t(t/100), y_t(t/100)] for t in range(t0*100, t1*100+1)]
    pg.draw.lines(screen, "white", False, pts, 3)

def drawSingleBezier(screen, p0, p1, g0, g1):
    # Draw curve and guide lines for the first two points
    x_t, y_t = getBezierFunction(p0, p1, g0, g1)
    drawCurve(screen, x_t, y_t)
    # Draw curve points
    drawPoint(screen, p0[0], p0[1])
    drawPoint(screen, p1[0], p1[1])
    # Draw first guide point and line
    drawPoint(screen, g0[0], g0[1], "red")
    drawLine(screen, p0, g0, (255, 100, 100))
    # Draw second guide point and line
    drawPoint(screen, g1[0], g1[1], "blue")
    drawLine(screen, p1, g1, (100, 100, 255))

def drawBezier(screen, points, g_plus, g_minus):
    if not points:
        return
    if len(points) == 1:
        drawPoint(screen, points[0][0], points[0][1])
        return
    # Get the first two points and guide points
    p0, p1, g0, g1 = points[0], points[1], g_plus[0], g_minus[1]
    drawSingleBezier(screen, p0, p1, g0, g1)
    # Draw the rest with a for loop for all points
    for i in range(2, len(points)):
        p0, p1, g0, g1 = points[i-1], points[i], g_plus[i-1], g_minus[i]
        drawSingleBezier(screen, p0, p1, g0, g1)

def getBezierCoefficients(p0, p1, g0, g1):
    x0, y0 = p0
    x1, y1 = p1
    gx0, gy0 = g0
    gx1, gy1 = g1
    a1, b1 = 3*(gx0 - x0), 3*(gy0 - y0)
    a2, b2 = 3*(x0 + gx1 - (2*gx0)), 3*(y0 + gy1 - (2*gy0))
    a3, b3 = x1 - x0 + (3*gx0) - (3*gx1), y1 - y0 + (3*gy0) - (3*gy1)
    return (x0, a1, a2, a3, y0, b1, b2, b3)

def getBezierFunction(p0, p1, g0, g1):
    a0, a1, a2, a3, b0, b1, b2, b3 = getBezierCoefficients(p0, p1, g0, g1)
    # print(f"x(t) = {a0} + {a1}t + {a2}t^2 + {a3}t^3")
    # print(f"y(t) = {b0} + {b1}t + {b2}t^2 + {b3}t^3")
    x = lambda t: a0 + (a1*t) + (a2*(t**2)) + (a3*(t**3))
    y = lambda t: b0 + (b1*t) + (b2*(t**2)) + (b3*(t**3))
    return x, y

def getClicked(pos):
    for i, (x, y) in enumerate(points):
        if abs(x - pos[0]) + abs(y - pos[1]) < 10:
            return ("p", i)
    for i, (x, y) in enumerate(g_plus):
        if abs(x - pos[0]) + abs(y - pos[1]) < 10:
            return ("gp", i)
    for i, (x, y) in enumerate(g_minus):
        if abs(x - pos[0]) + abs(y - pos[1]) < 10:
            return ("gm", i)
    return (None, None)

while True:
    screen.fill("black")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            kind, ind = getClicked(pos)
            if kind is None:
                gp = (pos[0] + 5, pos[1] + 5)
                gm = (pos[0] - 5, pos[1] - 5)
                if points:
                    px, py = points[-1]
                    d = ((pos[0] - px)**2 + (pos[1] - py)**2)**0.5
                    a, b = 100*(pos[0] - px) / d, 50*(pos[1] - py) / d
                    gm = (pos[0] - a, pos[1] - b)
                    gp = (pos[0] + a, pos[1] + b)
                g_plus.append(gp)
                g_minus.append(gm)
                points.append(pos)
            else:
                dragging = True
        if event.type == pg.MOUSEBUTTONUP:
            dragging = False
    if dragging and kind == "p":
        pos = pg.mouse.get_pos()
        x_diff = points[ind][0] - pos[0]
        y_diff = points[ind][1] - pos[1]
        g_minus[ind] = (g_minus[ind][0] - x_diff, g_minus[ind][1] - y_diff)
        g_plus[ind] = (g_plus[ind][0] - x_diff, g_plus[ind][1] - y_diff)
        points[ind] = pg.mouse.get_pos()
    elif dragging and kind == "gp":
        pos = pg.mouse.get_pos()
        p = points[ind]
        g_plus[ind] = pos
        x_diff = p[0] - pos[0]
        y_diff = p[1] - pos[1]
        g_minus[ind] = (p[0] + x_diff, p[1] + y_diff)
    elif dragging and kind == "gm":
        pos = pg.mouse.get_pos()
        p = points[ind]
        g_minus[ind] = pos
        x_diff = p[0] - pos[0]
        y_diff = p[1] - pos[1]
        g_plus[ind] = (p[0] + x_diff, p[1] + y_diff)
    drawBezier(screen, points, g_plus, g_minus)
    pg.display.update()






# def graphBezier(p0, p1, g0, g1):
#     a0, a1, a2, a3, b0, b1, b2, b3 = getBezierCoefficients(p0, p1, g0, g1)
#     print(f"x(t) = {a0} + {a1}t + {a2}t^2 + {a3}t^3")
#     print(f"y(t) = {b0} + {b1}t + {b2}t^2 + {b3}t^3")
#     x = lambda t: a0 + (a1*t) + (a2*(t**2)) + (a3*(t**3))
#     y = lambda t: b0 + (b1*t) + (b2*(t**2)) + (b3*(t**3))
#     t_values = np.linspace(0, 1, 100)
#     x_values = [x(t) for t in t_values]
#     y_values = [y(t) for t in t_values]

#     plt.plot(x_values, y_values)
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.title('Bezier Test')
#     plt.grid(True)
#     plt.show()

# graphBezier((0, 0), (5, 2), (0.5, 0.5), (5.5, 1.5))