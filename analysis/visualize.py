import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
import math

from simulation.block import SignalState


def visualize(model, steps, title):
    rail_length = model.signalling_control.length

    R = 5
    fig, ax = plt.subplots(figsize=(6,6))
    dpi = 240
    ax.set_xlim(-R-1, R+1)
    ax.set_ylim(-R-1, R+1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title)

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
        line, = ax.plot([], [], linewidth=8, color="blue", zorder=5)
        line.set_solid_capstyle('butt')
        train_patches.append((train, line))

        line, = ax.plot([], [], linewidth=6, alpha=1, zorder=4)
        line.set_solid_capstyle('butt')
        brake_patches.append((train, line))

    def update(frame):
        model.step()
        rail_circle = patches.Circle((0, 0), R, edgecolor='gray', facecolor='none', linewidth=2, zorder=0)
        ax.add_patch(rail_circle)

        for block, wedge in block_patches:
            if block.signal.is_station:
                wedge.set_facecolor("black")
            elif block.signal.max_speed == 0:
                wedge.set_facecolor("red")
            elif block.signal.max_speed_next == 0:
                wedge.set_facecolor("orange")
            else:
                wedge.set_facecolor("green")


        for train, line in train_patches:
            start = train.position.start % rail_length
            end = train.position.end % rail_length

            theta0 = (train.position.bounds[0] / rail_length) * 2 * np.pi
            theta1 = ((train.position.bounds[0] + train.position.length) / rail_length) * 2 * np.pi

            thetas = np.linspace(theta0, theta1, 40)
            xs = R * np.cos(thetas)
            ys = R * np.sin(thetas)

            line.set_data(xs, ys)

        for train, line in brake_patches:
            brake_dist = train.brake_distance(0, 1)
            brake_dist_vis = max(brake_dist, 30)

            theta0 = (train.position.bounds[1] / rail_length) * 2 * np.pi
            theta1 = ((train.position.bounds[1] + brake_dist) / rail_length) * 2 * np.pi

            thetas = np.linspace(theta0, theta1, 40)
            xs = R * np.cos(thetas)
            ys = R * np.sin(thetas)

            line.set_data(xs, ys)
            line.set_color('#00e2d3')

        return (
            [w for _, w in block_patches]
            + [l for _, l in train_patches]
            + [l for _, l in brake_patches]
        )

    ani = FuncAnimation(fig, update, frames=steps, interval=50)
    plt.show()
    ani.save(f"{title}.mp4", fps=30)

