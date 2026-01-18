import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

from simulation.block import Color


def visualize(model, steps):
    rail_length = model.signalling_control.length

    R = 5
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(-R-1, R+1)
    ax.set_ylim(-R-1, R+1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Circular Railway Simulation")

    train_patches = []
    block_patches = []
    brake_patches = []

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

        line, = ax.plot([], [], linewidth=2.5, alpha=0.8, zorder=4)
        brake_patches.append((train, line))

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
                wedge.set_facecolor("black")

        for train, circle in train_patches:
            theta = (train.position.bounds[1] / rail_length) * 2 * np.pi
            x = R * np.cos(theta)
            y = R * np.sin(theta)
            circle.center = (x, y)
        
        for train, line in brake_patches:
            brake_dist = train.braking_distance_to_zero()
            brake_dist_vis = max(brake_dist, 30)

            theta0 = (train.position.bounds[1] / rail_length) * 2 * np.pi
            theta1 = ((train.position.bounds[1] + brake_dist) / rail_length) * 2 * np.pi

            thetas = np.linspace(theta0, theta1, 40)
            xs = R * np.cos(thetas)
            ys = R * np.sin(thetas)

            line.set_data(xs, ys)
            line.set_color("red")

        return (
            [w for _, w in block_patches]
            + [c for _, c in train_patches]
            + [l for _, l in brake_patches]
        )
    ani = FuncAnimation(fig, update, frames=steps, interval=50)
    plt.show()
    ani.save("test.mp4")
