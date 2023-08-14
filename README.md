# 3D Convex Hull Algorithm
This repository showcases my self-implemented 3D Convex Hull algorithm, crafted during my studies in computational geometry. The Convex Hull, a cornerstone of computational geometry, emerges as the smallest convex polyhedron encompassing a collection of 3D points. Serving as a pivotal tool in diverse fields such as computer graphics, robotics, and simulations, this algorithm adeptly computes the Convex Hull, underscoring its significance in computational problem-solving.

In the realm of game graphics, consider an open-world video game where the landscape is populated with various objects, such as trees, rocks, and buildings. Determining what elements obstruct a player's view or movement is essential for creating realistic and immersive environments. By utilizing the Convex Hull algorithm, game developers can efficiently calculate simplified boundaries for these objects. These boundaries enable the game engine to optimize rendering, collision detection, and pathfinding, ultimately enhancing both the visual quality and the gameplay experience. <br/><br/>
Here's a simulation that illustrates the process of building a 3D Convex Hull:<br/><br/>
![Convex Hull GIF](https://user-images.githubusercontent.com/14288520/202849112-808c0f4c-9d96-44e6-a833-14a6dc886900.gif)

## Table of Contents

- [Introduction](#introduction)
- [Algorithm Overview](#algorithm-overview)
- [Usage](#usage)
- [Assignment Notes](#assignment-notes)
- [References](#references)

## Introduction

The Convex Hull of a set of points in three-dimensional space is the smallest convex polyhedron that encloses all the points. It has applications in various fields including computer graphics, robotics, and simulations. This implementation provides an efficient algorithm to compute the 3D Convex Hull.

## Algorithm Overview

The algorithm follows these main steps:

1. **Input**: Read the 3D points from an input source (file, user input, etc.).
2. **Pre-processing**: Perform any necessary pre-processing, sorting, or initial steps on the input points.
3. **Convex Hull Computation**: Apply the convex hull algorithm to compute the convex hull of the input points.
4. **Output**: Obtain the vertices and edges of the convex hull as the result.

## Usage

To use the 3D Convex Hull algorithm, follow these steps:

1. Clone this repository to your local machine:

   ```sh
   git clone https://github.com/TalSchreiber95/Convex-Hull-3d.git 

2. Compile the code if needed.

3. Run the program, providing the necessary input (input file, command line arguments, etc.).

4. The program will output the vertices and edges of the computed convex hull.


### Clone the repository
First clone the repository using:
  ```sh
 git clone https://github.com/TalSchreiber95/Convex-Hull-3d.git
   ```
then move to the main file to run the algo:
 ```sh 
cd main 
```



### Use appropriate compiler commands here and Run the program with input1 (1).txt as input in ./main.py
The program will read the points from ``` input1 (1).txt ``` (you can change it to other input files that in the project) and output the vertices and edges of the computed 3D convex hull.

## Assignment Notes
Please refer to the EX2 file in this repository for the specific assignment notes and guidelines provided as part of the computational geometry course. These notes will provide insights into the expectations for the assignment and might include additional details about the algorithm, input/output formats, and other relevant information.

## References
Provide any references you used while implementing the algorithm here. This could include textbooks, research papers, online resources, or any other relevant material that influenced your implementation.

## Collaborators
* [Tal Schreiber](https://github.com/TalSchreiber95)
* [Yuval Ben Yacov](https://github.com/yuvalbenya)

