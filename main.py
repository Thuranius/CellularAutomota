import random as r

# initial setup
main = []
sizeX = 120
sizeY = 39
numSmoothingPasses = 1000
smoothNum = .4

# initial map setup
for x in range(sizeX):
    main.append([])
    for y in range(sizeY):
        main[x].append(r.randint(0,1))

def smoothPass(map, sizeX, sizeY, soothNum):
    r = 2
    for x in range(sizeX):
        for y in range(sizeY):
            count = 0
            countDif = 0
            for i in range((r*-1)+1,r):
                for j in range((r*-1)+1,r):
                    if i+x > -1 and j+y > -1:
                        try:
                            if map[x][y] == map[i+x][j+y]:
                                count += 1
                                countDif += 1
                            else:
                                count += 1
                        except:
                            pass

            countPer = countDif/count
            if countPer < smoothNum:
                if map[x][y] == 0:
                    map[x][y] = 1
                else:
                    map[x][y] = 0
    return map

def cleanUp(map, sizeX, sizeY):
    for x in range(sizeX):
        for y in range(sizeY):
            if map[x][y] == 0:
                map[x][y] = "  "
            else:
                map[x][y] = "[]"
    return map

for i in range(numSmoothingPasses):
    main = smoothPass(main,sizeX,sizeY,smoothNum)

main = cleanUp(main,sizeX,sizeY)

print('')
for i in main:
    print(i)
