import math

def target (x_ , y_):

    x = int(x_)
    y = int(y_)

    angleX = 0
    angleY = 0

    height = (480 - y) / 40

    if (x > 320):
         width = (x- 320) / 25
         angleX = 100 - math.asin(width / (math.sqrt(math.pow(14, 2) + math.pow(width, 2)))) * 180 / 3.14
    if (x < 320):
         width = (320 - x) / 25
         angleX = 100 + math.asin(width / (math.sqrt(math.pow(14, 2) + math.pow(width, 2)))) * 180 / 3.14
    angleY = 130 + math.asin(height/(math.sqrt(math.pow(14, 2) + math.pow(height, 2)))) * 180/3.14

    return (angleX, angleY)
