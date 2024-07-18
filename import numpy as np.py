import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_tetrahedron(vertices):
    return [[vertices[j] for j in i] for i in [
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3],
    ]]

def generate_64_tetrahedron_grid():
    base_length = 1
    tetrahedrons = []
    offsets = [
        np.array([0, 0, 0]),
        np.array([base_length, 0, 0]),
        np.array([0, base_length, 0]),
        np.array([0, 0, base_length])
    ]

    for x in range(4):
        for y in range(4):
            for z in range(4):
                origin = np.array([x * base_length, y * base_length, z * base_length])
                for offset in offsets:
                    vertices = [
                        origin,
                        origin + np.array([base_length, 0, 0]),
                        origin + np.array([0, base_length, 0]),
                        origin + np.array([0, 0, base_length])
                    ]
                    tetrahedrons.append(create_tetrahedron(vertices))

    return tetrahedrons

def generate_points_and_labels():
    points = []
    labels = []
    label_counter = 0

    for x in range(5):
        for y in range(5):
            for z in range(5):
                points.append((x, y, z))
                labels.append(f"P{label_counter:03}")
                label_counter += 1

    return points, labels

def plot_tetrahedrons_and_points(tetrahedrons, points, labels):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plot tetrahedrons
    for tetra in tetrahedrons:
        verts = [list(zip(*[vertex for vertex in tetra]))]
        poly3d = Poly3DCollection(verts, alpha=.25, linewidths=1)
        poly3d.set_facecolor('cyan')
        ax.add_collection3d(poly3d)

    # Plot points
    xs, ys, zs = zip(*points)
    ax.scatter(xs, ys, zs, color='red')

    # Label points
    for point, label in zip(points, labels):
        ax.text(point[0], point[1], point[2], label)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('64-Tetrahedron Grid with Unique Points')

    plt.show()

if __name__ == "__main__":
    tetrahedrons = generate_64_tetrahedron_grid()
    points, labels = generate_points_and_labels()
    plot_tetrahedrons_and_points(tetrahedrons, points, labels)
