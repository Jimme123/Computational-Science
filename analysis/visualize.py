import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

from simulation.block import Color


def visualize(model, steps):
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

    ani = FuncAnimation(fig, update, frames=steps, interval=0)
    plt.show()
    ani.save("test.mp4")
