class Point3D:
    """
    Class representing a point in 3D space.

    Attributes:
        x (int): x-coordinate of the point.
        y (int): y-coordinate of the point.
        z (int): z-coordinate of the point.
        conflictsList (list[Facet]): List of facets where the point is in conflict (orient(facet, point) == -1).
        id (int): Unique key representing the order of reading the input file.
    """

    def __init__(self, x, y, z, key):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.conflictsList = []
        self.id = int(key)  # unique key -> order of reading the input file


class Facet:
    """
    Class representing a facet (Triangle) in 3D space.

    Attributes:
        active (bool): Boolean indicating whether the facet is active.
        p1, p2, p3 (Point3D): Points representing the vertices of the facet.
        conflictsList (list[Point3D]): List of points in conflict with the facet (orient(this_facet, point) == -1).
        facetNeighbours (list[Facet]): List of facets that share an edge with this facet.
    """

    def __init__(self, p: Point3D, q: Point3D, r: Point3D):
        self.active = True
        self.p1 = p
        self.p2 = q
        self.p3 = r
        self.conflictsList = []
        self.facetNeighbours = []

    def sub_points(self, p: Point3D, q: Point3D) -> list[Point3D]:
        """
        Subtract two points from the facet and return the remaining points.
        :param p: Point3D
        :param q: Point3D
        :return: List of points after subtraction.
        """
        return [pnt for pnt in [self.p1, self.p2, self.p3] if pnt != p and pnt != q]

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 and self.p3 == other.p3

def intersection(f1: Facet, f2: Facet) -> list[Point3D]:
    """
    Find the points that intersect between two facets.
    :param f1: First facet (Triangle).
    :param f2: Second facet (Triangle).
    :return: List of points (1, 2, or 3 points) that intersect between f1 and f2.
    """
    return [pnt for pnt in [f1.p1, f1.p2, f1.p3] if pnt in [f2.p1, f2.p2, f2.p3]]


class Edge:
    """
    Class representing an edge formed by two facets.

    Attributes:
        f_conf (Facet): Facet that is in conflict with a point.
        f_not_conf (Facet): Facet that is not in conflict with a point.
        start (Point3D): Starting point of the edge.
        end (Point3D): Ending point of the edge.
    """

    def __init__(self, f: Facet, g: Facet):
        self.f_conf = f
        self.f_not_conf = g
        pair_of_points = intersection(f, g)
        self.start = pair_of_points[0]
        self.end = pair_of_points[1]


def two_dim_det(a: tuple, b: tuple):
    """
    Calculate the 2x2 determinant from two points (represented as tuples).

    :return: Determinant value.
    """
    return a[0] * b[1] - a[1] * b[0]


def three_dim_det(a: Point3D, b: Point3D, c: Point3D):
    """
    Calculate the determinant of a 3x3 matrix formed by three points.

    :return: Determinant value.
    """
    return a.x * two_dim_det((b.y, b.z), (c.y, c.z)) \
        - b.x * two_dim_det((a.y, a.z), (c.y, c.z)) \
        + c.x * two_dim_det((a.y, a.z), (b.y, b.z))


def orient(p, q, r, t):
    """
    Calculate the orientation of four points in 3D space.

    :return: 1 for counter-clockwise, 0 for coplanar, -1 for clockwise.
    """
    four_dim_det = three_dim_det(q, r, t) - three_dim_det(p, r, t) \
        + three_dim_det(p, q, t) - three_dim_det(p, q, r)
    return 1 if four_dim_det > 0 \
        else -1 if four_dim_det < 0 else 0

def orient_f(f: Facet, q: Point3D):
    """ Helper function to calculate the orientation of a facet and a point. """
    return orient(f.p1, f.p2, f.p3, q)


def init_conflict(polytope: list[Facet], points: list[Point3D]) -> None:
    """
    Initialize the conflicts list for all points in the polytope.

    :param polytope: List of facets representing the polytope.
    :param points: List of points in 3D space.
    :return: None
    """
    for f in polytope:
        for p in points:
            if orient_f(f, p) == -1:
                p.conflictsList.append(f)
                f.conflictsList.append(p)


def has_points(f: Facet, p: Point3D, q: Point3D) -> bool:
    """
    Check if p and q are points of the given facet.

    :param f: Facet.
    :param p: Point3D.
    :param q: Point3D.
    :return: True if p and q are points of f, otherwise False.
    """
    return (f.p1 == p or f.p2 == p or f.p3 == p) and  \
          (f.p1 == q or f.p2 == q or f.p3 == q)


def disable_facet(f: Facet) -> None:
    """
    Disable a facet which means:
        1. Set f inactive.
        2. Update all its neighbour facets to remove f from their neighbour list.

    :param f: Facet to be disabled.
    :return: None
    """
    f.active = False
    for f_neighbour in f.facetNeighbours:
        f_neighbour.facetNeighbours.remove(f)



def count_conflicts(q: Point3D) -> int:
    """
    Returns the number of active facets in conflict with point "q".

    :param q: Point in 3D space.
    :return: Number of active facets in conflict with "q".
    """
    return sum(1 for f in q.conflictsList if f.active)


def facet_neighbour(curr_facet: Facet, u: Point3D, v: Point3D):
    """
    Returns the neighbor facet of curr_facet that shares the edge (u,v).

    :param curr_facet: Facet.
    :param u: Point.
    :param v: Point.
    :return: Neighbour facet of curr_facet that shares the edge (u,v).
    """
    for f in curr_facet.facetNeighbours:
        if has_points(f, u, v):
            return f
    return None
