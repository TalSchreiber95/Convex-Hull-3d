"""
Yuval ben yaakov: 315341552
Tal Schreiber 313264947
"""
import random

from objects import Point3D
from algo import construct_3d_polytope
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def custom_sort_key(point):
    # Sort first by x, then by y, and finally by z
    return (point[0], point[1], point[2])

# Sort the points using the custom key function
def read_input(filename):
    with open(filename, 'r') as file:
        n = int(file.readline())
        points = []
        count = 0
        for _ in range(n):
            x, y, z = map(int, file.readline().split())
            points.append(Point3D(x, y, z,count))
            count += 1
        print(len(points))
    return points

def plot_polytope(ans,points):
    fig = plt.figure()  # Adjust the figure size as per your preference
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot of the input points
    points_array = np.array([[p.x, p.y, p.z] for p in points])
    ax.scatter(points_array[:, 0], points_array[:, 1], points_array[:, 2])

    # Plot the edges of the facets forming the polytope
    for f in ans:
        x = [f.p1.x, f.p2.x, f.p3.x, f.p1.x]
        y = [f.p1.y, f.p2.y, f.p3.y, f.p1.y]
        z = [f.p1.z, f.p2.z, f.p3.z, f.p1.z]
        ax.plot(x, y, z, 'k-')

    # Fill the polytope facets with color
    for f in ans:
        x = [f.p1.x, f.p2.x, f.p3.x, f.p1.x]
        y = [f.p1.y, f.p2.y, f.p3.y, f.p1.y]
        z = [f.p1.z, f.p2.z, f.p3.z, f.p1.z]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts, facecolors='steelblue', alpha=0.3, linewidths=1, edgecolors='k'))

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_title('Constructed Polytope')

    plt.show()

def main():
    file_name = "input1 (1).txt"
    points = read_input(file_name)

    seed = int(random.random() * 100) # for shuffle
    random.seed(seed)
    random.shuffle(points)

    ans = construct_3d_polytope(points)

    total_poly = []
    for f in ans:
        to_print = [f.p1.id, f.p2.id, f.p3.id]
        index = to_print.index(min(to_print))
        to_ans = []
        to_ans.append(to_print[index])
        to_ans.append(to_print[(index + 1) % 3])
        to_ans.append(to_print[(index + 2) % 3])
        total_poly.append(to_ans)

    sorted_points = sorted(total_poly, key=custom_sort_key)

    # Create the output.txt
    with open('output.txt', 'w') as fp:
        for item in sorted_points:
            # print(item)
            fp.write(f"{item[0]} {item[1]} {item[2]}\n")
    print("output.txt:")
    print(sorted_points)
    # Create a 3D plot
    plot_polytope(ans,points)

if __name__ == '__main__':
    main()