import random as r
import perlin as p
from PIL import Image

n = p.SimplexNoise() # Noise maker!
n.randomize()
main = [] # Array to contain map values

# :: Changeable values to alter the outcome ::
mNum = 0 # This is the water height. Must be between -1 and 1
gradient = False
sizeX, sizeY = 960,540 # Final pixel sizes

# :: colors ::
_LIGHTBLUE = (27, 133, 191)
_DARKBLUE = (10, 96, 143)
_BORDER = (2, 27, 41)
_LIGHTGREEN = (90, 222, 75)
_DARKGREEN = (67, 176, 55)
_BLUEDIFF = tuple(map(lambda i, j: i - j, _LIGHTBLUE, _DARKBLUE))
_GREENDIFF = tuple(map(lambda i, j: i - j, _LIGHTGREEN, _DARKGREEN))

def perlinPass(octaves,x,y, lac =1 , persistence=1):
    """
    Taking in the x and y coordinates and produces the value after cycling through the all of the octaves.

    This process is super slow, especially when the pixel size is super high.

    Also, for some reason, the final image was getting weird patterns. This patterns emanating from the top left corner until
    I put in the '-freq' into the noise2 function. /shrug.
    """
    freq = 1
    amp = 1
    max = 0
    total = 0
    for i in range(octaves):
        freq *= lac
        total += n.noise2(x*freq-freq,y*freq-freq)
        max += amp
    final = total/max
    return final

def fullMap(map,sizeX,sizeY):
    """
    The maNum values determine how 'zoomed in' the result produces.
    The lower the number, the further zoomed out it will be.
    """
    maNum1 = 600
    maNum2 = 400
    maNum3 = 200
    maNum4 = 100
    for x in range(sizeX):
        map.append([])
        for y in range(sizeY):
            noise_val = perlinPass(3,x/(maNum1),y/(maNum1),1.3)
            noise_val += .5 * perlinPass(6,x/(maNum2),y/(maNum2),1.4)
            noise_val += .25 * perlinPass(12,x/(maNum3),y/(maNum3),1.5)
            noise_val += .125 * perlinPass(24,x/(maNum4),y/(maNum4),1.6)
            map[x].append(noise_val)
    return map

def assignColor(map, sizeX, sizeY):
    global mNum, _LIGHTBLUE, _LIGHTGREEN, _BORDER
    for x in range(sizeX):
        for y in range(sizeY):
            if map[x][y] == 999:
                map[x][y] = _BORDER
            elif map[x][y] < mNum:
                map[x][y] = _LIGHTBLUE # Blue
            else:
                map[x][y] = _LIGHTGREEN # Land
    return map

def assignGradient(Omap, sizeX, sizeY):
    global mNum, _GREENDIFF,_LIGHTGREEN,_BLUEDIFF,_LIGHTBLUE
    for x in range(sizeX):
        for y in range(sizeY):
            gradientPercent = abs(Omap[x][y])
            if Omap[x][y] == 999:
                Omap[x][y] = (1, 1, 40)
            elif Omap[x][y] >= mNum:
                DiffVector = (round(_GREENDIFF[0] * gradientPercent), round(_GREENDIFF[1] * gradientPercent), round(_GREENDIFF[2] * gradientPercent))
                Omap[x][y] = tuple(map(lambda i, j: i - j, _LIGHTGREEN, DiffVector))
            else:
                DiffVector = (round(_BLUEDIFF[0] * gradientPercent), round(_BLUEDIFF[1] * gradientPercent), round(_BLUEDIFF[2] * gradientPercent))
                Omap[x][y] = tuple(map(lambda i, j: i - j, _LIGHTBLUE, DiffVector))
    return Omap

def detectBorder(map, sizeX, sizeY, radius = 2, random = False):
    """
    Runs through each pixel and looks around itself according to the radius variable for a value less than the 'water level', setting it as a border
    """
    rd = radius
    global mNum
    newMap = []
    for x in range(sizeX):
        newMap.append([])
        for y in range(sizeY):
            newMap[x].append(11)
            found = False
            if map[x][y] >= mNum:
                for i in range((rd*-1)+1,rd):
                    for j in range((rd*-1)+1,rd):
                        if i+x > -1 and j+y > -1:
                            try:
                                if not found:
                                    if map[x+i][y+j] < mNum:
                                        newMap[x][y] = 999
                                        found = True
                                    else:
                                        newMap[x][y] = map[x][y]
                            except:
                                pass
            else:
                newMap[x][y] = map[x][y]

    return newMap

def newImg(map, sizeX, sizeY):
    img = Image.new(mode = "RGB", size = (sizeX,sizeY))
    pixels = img.load()
    for x in range(sizeX):
        for y in range(sizeY):
            pixels[x,y] = map[x][y]
    img.show()

main = fullMap(main,sizeX,sizeY)
main = detectBorder(main,sizeX,sizeY)
if gradient:
    main = assignGradient(main,sizeX,sizeY)
else:
    assignColor(main,sizeX,sizeY)

newImg(main, sizeX,sizeY)
