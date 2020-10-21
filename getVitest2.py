import math
import InitVTest
x1 = 0
y1 = 18
x2 = 96
y2 = 36
angle = 48
gravity = -386.09


def getVi(x1, y1, x2, y2, angle):
    deltaX = abs(x2 - x1)
    deltaY = abs(y2 - y1)
    angle = math.radians(angle)

    answer = deltaX / (math.cos(angle) * math.sqrt((deltaY - (deltaX * math.tan(angle))) / (gravity / 2)));
    return answer

def getAngle(vi, angle, y):
    # h = .01
    # vx = math.sin(math.radians(angle)) * vi
    # vy = math.cos(math.radians(angle)) * vi
    #
    # x = x1 * vx
    # xh = (x1 + h) * vx
    #
    # y = InitVTest.evalQuadratic(y1, InitVTest.gravity/2, vy, y1)
    # yh = InitVTest.evalQuadratic(y1 + h, InitVTest.gravity/2, vy, y1)
    #
    # return math.degrees(math.atan2(yh-y, xh - x))

if __name__ == '__main__':
    print(str(getVi(x1, y1, x2, y2, angle)))
