import random as r
from PIL import Image

main = []

# || initial setup ||
# Playing with these numbers will alter the shape of the map
sizeX = 640
sizeY = 480
numSmoothingPasses = 50
mNum = 4.5

# Used to blend the values of each pixel to those that surround it. Increasing the radius increases the complexity n^2
def smoothPass(map, sizeX, sizeY, radius):
    rd = radius
    newMap = []
    for x in range(sizeX):
        newMap.append([])
        for y in range(sizeY):
            count = 0
            countDif = 0
            newMap[x].append(0)
            for i in range((rd*-1)+1,rd):
                for j in range((rd*-1)+1,rd):
                    if i+x > -1 and j+y > -1:
                        try:
                            countDif += map[i+x][j+y]
                            count += 1
                        except:
                            pass
            countAvg = countDif/count
            newMap[x][y] = countAvg

    return newMap

def detectBorder(map, sizeX, sizeY, radius, random = False):
    rd = radius
    global mNum
    newMap = []
    for x in range(sizeX):
        newMap.append([])
        for y in range(sizeY):
            newMap[x].append(11)
            if random:
                rd = r.randint(radius-1,radius+1)
            found = False
            for i in range((rd*-1)+1,rd):
                for j in range((rd*-1)+1,rd):
                    if i+x > -1 and j+y > -1:
                        try:
                            if not found:
                                if map[x][y] >= mNum and map[x+i][y+j] < mNum:
                                    newMap[x][y] = 10
                                    found = True
                                else:
                                    newMap[x][y] = map[x][y]
                        except:
                            pass

    return newMap

def assignColor(map, sizeX, sizeY):
    global mNum
    for x in range(sizeX):
        for y in range(sizeY):
            if map[x][y] < mNum:
                map[x][y] = (19, 118, 171) #Blue
            elif map[x][y] == 10:
                map[x][y] = (245, 239, 218) #Sand
            elif map[x][y] == 11:
                map[x][y] = (255,0,0) # Debug Red
            else:
                map[x][y] = (90, 222, 75) # Green
    return map

def newImg(map, sizeX, sizeY):
    img = Image.new(mode = "RGB", size = (sizeX,sizeY))
    pixels = img.load()
    for x in range(sizeX):
        for y in range(sizeY):
            pixels[x,y] = map[x][y]
    img.show()

# initial map setup
for x in range(sizeX):
    main.append([])
    for y in range(sizeY):
        main[x].append(r.randint(0,9))

main = smoothPass(main,sizeX,sizeY, 6)
for i in range(numSmoothingPasses):
    main = smoothPass(main,sizeX,sizeY, 3)

main = detectBorder(main,sizeX,sizeY, 2)
main = assignColor(main,sizeX,sizeY)

newImg(main, sizeX,sizeY)
