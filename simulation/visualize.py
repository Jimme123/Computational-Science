import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

from model import Railroad
from block import Color
from staticBlockSignalling import *
from movingBlockSignalling import *

rail_length = 12000
model = Railroad(rail_length, MovingBlockSignalling, sight=300, dt=1, wait_time=10)
model.add_train(Position(3000, 3100, rail_length), 25, 1.3, 1.1)
model.add_train(Position(0, 100, rail_length), 55, 1.3, 1.1)

# n = 8
# positions = np.linspace(0, rail_length, n + 1)
# stations = [2, 4]
# for i in range(n):
#     if i in stations:
#         model.add_station(Position(positions[i], positions[i]+10, rail_length))
#         model.add_block(Position(positions[i]+10, positions[i+1], rail_length))
#     else:
#         model.add_block(Position(positions[i], positions[i+1], rail_length))

n = 4
positions = np.linspace(0, rail_length, n + 1)
print(positions)
for i in range(n):
    model.add_station(Position(positions[i], positions[i] + 10, rail_length))

R = 5
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-R-1, R+1)
ax.set_ylim(-R-1, R+1)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Circular Railway Simulation")

train_patches = []
block_patches = []

for block in model.signalling_control.blocks:
    start_angle = (block.position.start / rail_length) * 360
    end_angle = (block.position.end / rail_length) * 360
    wedge = patches.Wedge(center=(0,0), r=R, theta1=start_angle, theta2=end_angle, width=0.5, facecolor="green")
    block_patches.append((block, wedge))
    ax.add_patch(wedge)

for train in model.trains:
    circle = plt.Circle((0,0), 0.2, color="blue")
    train_patches.append((train, circle))
    ax.add_patch(circle)

def update(frame):
    model.step()

    for block, wedge in block_patches:
        if block.signal == Color.GREEN:
            wedge.set_facecolor("green")
        elif block.signal == Color.ORANGE:
            wedge.set_facecolor("orange")
        elif block.signal == Color.RED:
            wedge.set_facecolor("red")
        elif block.signal == Color.STATION:
            wedge.set_facecolor("cyan")

    for train, circle in train_patches:
        theta = (train.position.start / rail_length) * 2 * np.pi
        x = R * np.cos(theta)
        y = R * np.sin(theta)
        circle.center = (x, y)

    return [w for _, w in block_patches] + [c for _, c in train_patches]

ani = FuncAnimation(fig, update, frames=500, interval=50)
plt.show()
ani.save("test.mp4")
