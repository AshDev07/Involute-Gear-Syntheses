# This code is written in python as I find it easier than cpp code
import matplotlib.pyplot as plt
import math
import numpy as npy


# Defining rotation matrix as a function
def rotation_matrix(th):
    return [[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]]


# Defining function to construct radial line from center
def radial_line(th, R1, R2):
    return [[R1 * math.cos(th), R2 * math.cos(th)], [R1 * math.sin(th), R2 * math.sin(th)]]


# Defining function to create an arc
def draw_arc(r, tht1, tht2):
    coords = npy.array([[], []])
    for th in npy.arange(tht1, tht2, 0.001):
        coords = npy.append(coords, [[r * math.cos(th)], [r * math.sin(th)]], axis=1)
    return coords


# Defining the parameters
N = 20  # no of teeth
m = 10  # module in mm
pr_angle = 20 * math.pi / 180  # pressure angle
Rp = m * N / 2  # pitch radius
Rd = Rp - (m * 1.25)  # dedendum radius
Ra = Rp + m  # addendum radius
Rb = Rp * math.cos(pr_angle)  # base circle radius
tooth_angle = 17.63 / Rb  # angle subtended by single tooth of base circle on center
right_profile = npy.array([[], []])  # right side profile of the tooth
left_profile = npy.array([[], []])  # left side profile of the tooth
gear_profile = npy.array([[], []])  # tooth profile between teeth
tooth_profile = npy.array([[], []])  # tooth profile on top which is an arc

# Involute Profile Construction
th = 0
while True:  # Right side of tooth
    x = Rb * (math.cos(th) + th * math.sin(th))
    y = Rb * (math.sin(th) - th * math.cos(th))
    if Rd * Rd <= x * x + y * y <= Ra * Ra:
        right_profile = npy.append(right_profile, [[x], [y]], axis=1)
    elif x * x + y * y > Ra * Ra:
        tht1 = math.atan(y / x)
        break
    th += 0.001

# Constructing left side of tooth profile by flipping right side
left_profile = npy.flip(npy.dot(rotation_matrix(tooth_angle), [right_profile[0], right_profile[1] * -1]), 1)

# Construction of tooth profile
if Rd < Rb:  # We can see that Rd is infact less than Rb
    tooth_profile = radial_line(0, Rd, Rb)

tooth_profile = npy.concatenate((tooth_profile, right_profile, draw_arc(Ra, tht1, tooth_angle - tht1), left_profile),
                                axis=1)  # Tooth

if Rd < Rb:
    tooth_profile = npy.concatenate((tooth_profile, radial_line(tooth_angle, Rd, Rb)),
                                    axis=1)  # line connecting dedendum circle and involute curve

tooth_profile = npy.concatenate((tooth_profile, draw_arc(Rd, tooth_angle, 2 * math.pi / 20)), axis=1)  # Dedendum arc

# Construction of N number of teeth
for i in range(N):
    th = i * 2 * math.pi / N
    gear_profile = npy.concatenate((gear_profile, npy.dot(rotation_matrix(th), tooth_profile)), axis=1)

# Plotting gear profile
plt.plot(gear_profile[0], gear_profile[1], color='darkblue')
plt.title('Involute Tooth Profile')
plt.show()
