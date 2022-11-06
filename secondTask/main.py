
import numpy as np
import matplotlib.pyplot as plt

def parseLine(line, dots_list, facets_list):
    arr = line.split()
    if len(arr) > 0:
        if arr[0] == 'v':
            dots_list.append(list(np.float_(arr[1:])))
        elif arr[0] == 'f':
            facets_list.append(list(map(lambda i: i - 1, list(np.int_(arr[1:])))))

def readFile(filename, dots_list, facets_list):
    with open(filename, "r") as f:
        for line in f.readlines():
            parseLine(line, dots_list, facets_list)


def printPixel(x, y, img, color):
    for i in range(3):
        img[x, y, i] = color[i] #x и y перепутаны, а y сверху вниз


def printLine(x1, y1, x2, y2, img, color):
    dx = x2 - x1
    dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y = x1, y1
    error, t = el / 2, 0
    printPixel(x, y, img, color)
    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        printPixel(x, y, img, color)


def printAllGrani(dots, facets, img, color):
    for i in range(np.shape(facets)[0]):
        printLine(dots[facets[i, 0]][0], dots[facets[i, 0]][1],
                  dots[facets[i, 1]][0], dots[facets[i, 1]][1],
                  img, color)
        printLine(dots[facets[i, 2]][0], dots[facets[i, 2]][1],
                  dots[facets[i, 1]][0], dots[facets[i, 1]][1],
                  img, color)
        printLine(dots[facets[i, 2]][0], dots[facets[i, 2]][1],
                  dots[facets[i, 0]][0], dots[facets[i, 0]][1],
                  img, color)


def draw_circle(img, x, y, r, color):
    disp_x = x
    disp_y = y
    x = 0
    y = r
    delta = (1 - 2 * r)
    error = 0
    while y >= 0:
        printPixel(disp_x + x, disp_y + y, img, color)
        printPixel(disp_x + x, disp_y - y, img, color)
        printPixel(disp_x - x, disp_y + y, img, color)
        printPixel(disp_x - x, disp_y - y, img, color)

        error = 2 * (delta + y) - 1
        if ((delta < 0) and (error <= 0)):
            x += 1
            delta = delta + (2 * x + 1)
            continue
        error = 2 * (delta - x) - 1
        if ((delta > 0) and (error > 0)):
            y -= 1
            delta = delta + (1 - 2 * y)
            continue
        x += 1
        delta = delta + (2 * (x - y))
        y -= 1

def printBackground(img, dots, x, y):
    max_x = 0
    max_y = 0
    for i in range(np.shape(dots)[0]):
        if max_x < dots[i][0]:
            max_x = dots[i][0]
        if max_y < dots[i][1]:
            max_y = dots[i][1]
    radius = int(min(max_x, max_y) / 2)
    color = np.array([0, 0, 0], dtype=np.uint8)
    colorShift = 255 / radius
    for i in range(radius):
        # color[0] = i * colorShift
        color[1] = i * colorShift
        color[2] = i * colorShift
        draw_circle(img, x, y, i, color)


def mkWindow(dots, facets, height, width):
    img = np.zeros((width, height, 3), dtype=np.uint8)
    color = np.array([255, 255, 255], dtype=np.uint8)
    # printBackground(img, dots, int(width/2), int(height/2))
    printAllGrani(dots, facets, img, color)
    plt.figure()
    plt.imshow(img)
    plt.show()


def toScaleDots(dots, windowHeight, windowWidth):
    result = min(windowHeight, windowWidth) / 3
    maximumValue = abs(np.amax(dots))
    scale = result / maximumValue
    dots = np.array(np.int_(dots*scale))
    for i in range(np.shape(dots)[0]):
        dots[i][0] += (windowHeight / 2)
        dots[i][1] += (windowWidth / 2)
    return dots


dots_list = []
facets_list = []
width = 640#plt.get_current_fig_manager().window.winfo_screenheight()
height = 640#plt.get_current_fig_manager().window.winfo_screenwidth()


if __name__ == '__main__':
    readFile("../firstTask/teapot.obj", dots_list, facets_list)
    dots = np.array(dots_list)
    facets = np.array(facets_list)
    dots = toScaleDots(dots, height, width)
    #print(dots, "\n", facets)
    print(dots)
    mkWindow(dots, facets, height, width)


