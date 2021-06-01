import random as r
import perlin as p
from PIL import Image

n = p.SimplexNoise() # Noise maker!
n.randomize()
sizeX, sizeY = 960, 540
main = []
mNum = 128 # This is the water height

def perlinPass(octaves,x,y, lac =1 , persistence=1):
    # freq = lac
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

def limit(val):
    if val > 1:
        return 1
    elif val < -1:
        return -1
    else:
        return val

def fullMap(map,sizeX,sizeY):
    maNum = 1
    # lac = 1.3
    for x in range(sizeX):
        map.append([])
        for y in range(sizeY):
            noise_val = perlinPass(3,x/(sizeX/maNum),y/(sizeY/maNum),1.3)
            noise_val = limit(noise_val)
            noise_val += .5 * perlinPass(6,x/(sizeX/maNum),y/(sizeY/maNum),1.4)
            noise_val = limit(noise_val)
            noise_val += .25 * perlinPass(12,x/(sizeX/maNum),y/(sizeY/maNum),1.5)
            noise_val = limit(noise_val)
            noise_val += .125 * perlinPass(24,x/(sizeX/maNum),y/(sizeY/maNum),1.6)
            map[x].append(noise_val)
    return map

def assignColorGray(map, sizeX, sizeY):
    for x in range(sizeX):
        for y in range(sizeY):
            map[x][y] = (round((map[x][y]*127)+128),round((map[x][y]*127)+128),round((map[x][y]*127)+128))
    return map

def assignColor(map, sizeX, sizeY):
    global mNum
    for x in range(sizeX):
        for y in range(sizeY):
            if map[x][y] == 999:
                # map[x][y] = (245, 239, 218) # Sand
                map[x][y] = (1, 1, 40)
            elif round((map[x][y]*127)+128) < mNum:
                map[x][y] = (19, 118, 171) # Blue
            else:
                map[x][y] = (90, 222, 75) # Land
    return map

def detectBorder(map, sizeX, sizeY, radius = 2, random = False):
    rd = radius
    global mNum
    newMap = []
    for x in range(sizeX):
        newMap.append([])
        for y in range(sizeY):
            newMap[x].append(11)
            found = False
            for i in range((rd*-1)+1,rd):
                for j in range((rd*-1)+1,rd):
                    if i+x > -1 and j+y > -1:
                        try:
                            if not found:
                                if round((map[x][y]*127)+128) >= mNum and round((map[x+i][y+j]*127)+128) < mNum:
                                    newMap[x][y] = 999
                                    found = True
                                else:
                                    newMap[x][y] = map[x][y]
                        except:
                            pass

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
main = assignColor(main,sizeX,sizeY)

newImg(main, sizeX,sizeY)
