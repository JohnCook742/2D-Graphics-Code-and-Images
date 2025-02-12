import math

# Angle between two points

Ax = 105
Ay = 10

Bx = 25
By = 35

answer = math.atan2(Ay-By, Ax-Bx)
print(answer)

# Arbitrary rotation of a single point 
# by defined angle in degrees

Ax = 40
Ay = -65
dist = math.sqrt(Ax**2+Ay**2)
print(dist)

angleDif = 20 * math.pi/180
print(angleDif)


angle = math.atan2(Ay, Ax)
print(angle)
newAngle = angle + angleDif
print(newAngle)
Bx = math.cos(newAngle) * dist
By = math.sin(newAngle) * dist
answer = (Bx, By)
print(answer)
answer = (int(Bx), int(By))
print(answer)