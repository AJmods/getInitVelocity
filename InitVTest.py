import math
import matplotlib.pyplot as plt
import numpy as np

gravity = -386.09
x1 = int(input("Enter x1 (anything that is not 0 will break it)"))
y1 = int(input("Enter y1 (typically 18)"))
x2 = int(input("Enter x2 (distance from robot to goal"))
y2 = int(input("Enter y2 (goal height, typically 36"))
# x1 = 0
# y1 = 18
# x2 = 96
# y2 = 36

startingAngle = 1
maxAngle = 89
maxFeet = 60
maxLaunchLengthX = 144


def evalQuadratic(x, a, b, c):
    return (a * pow(x, 2)) + (b * x) + c


def solveQuadratic(a, b, c):
    result = b * b - 4.0 * a * c
    if result > 0.0:
        r1 = (-b + math.pow(result, .5)) / (2.0 * a)
        r2 = (-b - math.pow(result, .5)) / (2.0 * a)
        if r1 > r2:
            return r1
        else:
            return r2
    elif result == 0:
        r1 = -b / (2 * a)
        return r1
    else:
        return float("NaN")


def getMaxY(a, b, c):
    x = -b / (2 * a)
    return evalQuadratic(x, a, b, c)


def getVI(x1, y1, x2, y2, angle):
    numDigits = 10
    startNumber = 1000

    deltaX = abs(x2 - x1)
    vi = 0

    for i in range(0, numDigits):
        # print("Testing " + str(startNumber))

        for j in range(1, 11):
            testInitV = (j * startNumber) + vi
            testInitX = testInitV * math.cos(math.radians(angle))
            testInitY = testInitV * math.sin(math.radians(angle))

            xTime = deltaX / testInitX
            # if angle == 40:
            #     print("DELTA X: " + str(deltaX) + ", testINITX " + str(testInitX) + ", Xtime " + str(xTime))

            yAtXtime = evalQuadratic(xTime, gravity / 2, testInitY, y1)

            if yAtXtime >= y2:
                vi += (j - 1) * startNumber
                startNumber /= 10
                # print("Ending Loop")
                break
            elif j == 11:
                startNumber *= 10
    startNumber /= 10
    if vi == 0:
        return 1e10
    return vi


def graphThing(vi2, angle):
    x = []
    y = []

    vy = vi2 * math.sin(math.radians(angle))
    vx = vi2 * math.cos(math.radians(angle))

    detlaX = abs(x2 - x1)
    xTime = solveQuadratic(gravity / 2, vy, y1)
    #xTime = 144 / vx
    print("DELTA X: " + str(detlaX) + ", VX: " + str(vx))
    # print(xTime)
    endX = xTime * vx

    maxX = 0
    maxY = 0

    for i in np.arange(0, xTime, .01):
        tempX = i * vx
        tempY = evalQuadratic(i, gravity / 2, vy, y1)
        x.append(tempX)
        y.append(tempY)
        if tempY > maxY:
            maxX = tempX
            maxY = tempY

    xThing = [x1, x2, endX, maxX]
    yThing = [y1, y2, 0, maxY]

    plt.plot(x, y, 'k')
    plt.scatter(xThing, yThing)
    plt.xlabel("Inches X")
    plt.ylabel("Inches Y")
    plt.title("Disc Launch X vs Y (not to scale)")
    plt.text(x1, y1, "Launch Pos (" + str(x1) + ", " + str(y1) + ")")
    plt.text(x2, y2, "Goal Pos (" + str(x2) + ", " + str(y2) + ")")
    plt.text(endX-45, 1, "LANDS AT (" + '{:3.3f}'.format(endX) + ",0)")
    plt.text(0, 3,
             "Vi = " + '{:6.3f}'.format(vi2) + " in/sec, ANGLE = " + str(angle) + " degrees\nTIME TO GET TO GOAL = " + '{:3.3f}'.format(detlaX/vx))
    plt.text(maxX - 13, maxY - 3, "Max (" + '{:3.1f}'.format(maxX) + ", " + '{:3.1f}'.format(maxY) + ")")
    plt.grid(True)
    plt.show()


if __name__ == '__main__':

    initVelocities = []
    initDegrees = []

    for i in range(startingAngle, maxAngle + 1):
        vi = getVI(x1, y1, x2, y2, i)
        vy = vi * math.sin(math.radians(i))
        vx = vi * math.cos(math.radians(i))
        max = getMaxY(gravity / 2, vy, y1)
        validIndexes = []

        if max < maxFeet:
            print("MIN ANGLE " + str(i) + "GOES TO A MAX OF " + str(max))
            break;

    for i in range(startingAngle, maxAngle + 1):
        vi = getVI(x1, y1, x2, y2, i)
        vy = vi * math.sin(math.radians(i))
        vx = vi * math.cos(math.radians(i))
        max = getMaxY(gravity / 2, vy, y1)

        initVelocities.append(vi)
        initDegrees.append(i)

        print("Vi = " + str(vi) + ", Vx = " + str(vx) + ", Vy = " + str(vy) + ", angle = " + str(i))

        if max < maxFeet:
            timeAtZero = solveQuadratic(gravity / 2, vy, y1)
            distanceAtGround = timeAtZero * vx

            if distanceAtGround < maxLaunchLengthX:
                validIndexes.append(i)
                # print("Vi = " + str(vi) + ", Vx = " + str(vx) + ", Vy = " + str(vy) + ", angle = " + str(i))
            else:
                print("AT ANGLE " + str(i) + "LAUNCHES BALL TO FAR")
        else:
            print("AT ANGLE " + str(i) + " GOES TOO HIGH WITH A MAX OF " + str(max))

    maxIndex = 0
    maxThing = 0
    minIndex = 0
    minThing = 1000
    print(len(validIndexes))
    for i in range(validIndexes[0], validIndexes[len(validIndexes) - 1]):
        tempMax = getMaxY(gravity / 2,
                          initVelocities[i - 1] * math.sin(math.radians(initDegrees[i - 1])), y1)
        print(str(i) + ": " + str(tempMax))
        if maxThing < tempMax:
            maxThing = tempMax
            maxIndex = i - 1
        if minThing > tempMax:
            minThing = tempMax
            minIndex = i - 1

    for i in range(0, len(initVelocities)):
        print(str(initDegrees[i]) + ": " + str(initVelocities[i]))

    print(
        "At " + str(initDegrees[maxIndex]) + " degrees, the disk will go " + str(
            maxThing) + " inches high then go down "
        + "to the goal of " + str(y2) + " inches")
    print(
        "At " + str(initDegrees[minIndex]) + " degrees the disk will go as low as possible (" + str(
            minThing) + "inches) in order to get in the goal of " + str(y2) + "inches")
    print("VALID ANGLES: " + str(validIndexes[0]) + " to " + str(validIndexes[len(validIndexes)-1]))
    bestAngle = (validIndexes[0] + validIndexes[len(validIndexes)-1]) / 2
    print("BEST ANGLE: " + str(int(bestAngle)))
    index = int(input("Enter Angle to plot"))
    print("USING " + str(initVelocities[index - 1]) + " AT ANGLE " + str(index))
    graphThing(initVelocities[index - 1], index)
