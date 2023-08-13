from objects import *


def find_first_horizon_edge(q: Point3D):
    """
    :param q: point that currently we added to the space
    :return: horizon edge represented by 2 POINTS in LIST
    """
    for f in q.conflictsList:
        if f.active:
            for f_neighbour in f.facetNeighbours:
                if orient_f(f_neighbour, q) == 1:
                    return Edge(f, f_neighbour)


def find_all_horizon_edges(q: Point3D, first_edge: Edge) -> list[Edge]:
    """
    :param q: point added to space and in conflict with the polytope
    :param first_edge: hold the data of start, end points of edge
                        where one of the facets is in conflict with q
                            the other not.
    :return: list of edge that represent the horizon from q to on the polytope
                edge represents as pair of 2 points
    """
    list_of_horizon = [first_edge]
    curr_facet = first_edge.f_conf
    start_point, end_point = first_edge.start, first_edge.end

    # our term is - stop when our pivot point closing cycle with the first_edge we started with
    while (end_point != first_edge.start):

        # our next point which makes edge (pivot_p, next_p)
        #   will be the substract between curr_facet \ {pivot_p, before_p}
        next_p = curr_facet.sub_points(end_point, start_point).pop()

        # we look for the neighbour facet of the edge (pivot_p, next_p)
        #   we coming from curr_facet
        #   candidate means - the candidate facet to hold our next Horizon edge
        candidate_facet = facet_neighbour(curr_facet, end_point, next_p)

        if (orient_f(candidate_facet, q)) == 1:
            # we found new horizon edge
            temp_edge = Edge(curr_facet, candidate_facet)
            temp_edge.start = end_point
            temp_edge.end = next_p
            list_of_horizon.append(temp_edge)
            start_point = end_point
            end_point = next_p
        else:
            # the new facet is still conflict
            curr_facet = candidate_facet
            start_point = next_p
    return list_of_horizon


def construct_facets(q: Point3D, list_of_horizon: list[Edge], helper_p: Point3D) -> list[Facet]:
    """
    :param q: our new point to build facet with the edges of horizon
    :param list_of_horizon: all edges
    :param helper_p: point inside the polytope s.t we can construct the facet in the right order
    :return: list of facets s.t they initialized to their facetNeighbours and their conflicts
    """
    ans = []
    # construct facets and set one neighbour
    # to be the neighbour of the edge which not in conflict with q
    for edge_t in list_of_horizon:
        if orient(edge_t.start, edge_t.end, q, helper_p) == 1:
            facet_t = Facet(edge_t.start, edge_t.end, q)
        else:
            facet_t = Facet(edge_t.end, edge_t.start, q)
        facet_t.facetNeighbours.append(edge_t.f_not_conf)
        edge_t.f_not_conf.facetNeighbours.append(facet_t)
        ans.append(facet_t)

        # updating conflicts
        for p in edge_t.f_conf.conflictsList:
            if orient_f(facet_t, p) == -1:
                facet_t.conflictsList.append(p)
                p.conflictsList.append(facet_t)
        for p in edge_t.f_not_conf.conflictsList:
            if (orient_f(facet_t, p) == -1) and (p not in facet_t.conflictsList):
                facet_t.conflictsList.append(p)
                p.conflictsList.append(facet_t)

    # run over the new facets and set them as facetNeighbours
    count = 0
    for f in ans:
        f.facetNeighbours.append(ans[count - 1 % len(ans)])
        f.facetNeighbours.append(ans[(count + 1) % len(ans)])
        count = count + 1

    return ans


def cal_mid_point(points: list[Point3D]):
    """
    helper function that calculate the middle point of the poytope
    :param points: list of points
    :return: middle point
    """
    l = len(points)
    x_ans = 0
    y_ans = 0
    z_ans = 0
    for p in points:
        x_ans = x_ans + p.x
        y_ans = y_ans + p.y
        z_ans = z_ans + p.z

    return Point3D(x_ans / l, y_ans / l, z_ans / l, 1)


def init_3d_polytope(poly_points: list[Point3D]) -> list[Facet]:
    q0, q1, q2, q3 = poly_points[0], poly_points[1], poly_points[2], poly_points[3]
    for q in [q0, q1, q2, q3]:
        q.still_out = False
    # helpful later, this point always inside polytope so we can build our facet in currect way
    q_mid = cal_mid_point(poly_points)

    if orient(q0, q1, q2, q3) == 1:
        f0 = Facet(q0, q1, q2)
        f1 = Facet(q0, q3, q1)
        f2 = Facet(q0, q2, q3)
        f3 = Facet(q1, q3, q2)
    else:
        f0 = Facet(q1, q0, q2)
        f1 = Facet(q0, q1, q3)
        f2 = Facet(q0, q3, q2)
        f3 = Facet(q1, q2, q3)

    f0.facetNeighbours = [f1, f2, f3]
    f1.facetNeighbours = [f0, f2, f3]
    f2.facetNeighbours = [f0, f1, f3]
    f3.facetNeighbours = [f0, f1, f2]
    return q_mid, [f0, f1, f2, f3]


def construct_3d_polytope(points: list[Point3D]) -> list[Facet]:
    """
    Constructs a 3D polytope (polygon or polyhedron) from a set of points in 3D space using the random incremental algorithm.

    :param points: List of all the points in 3D space.
    :param poly_size: Number of points we want to use for constructing the polytope.
    :return: List of facets representing the constructed 3D polytope.
    """
    # init default phase, 4 first points -> base polytope
    q_mid, curr_polytope = init_3d_polytope([points.pop(0) for _ in range(4)])
    init_conflict(curr_polytope, points)
    # ---------------------------- end of first phase (initialize the base state) ------------------- #

    # ---------------------------- running the algorithm from i = 4 -> n ----------------------------
    for q in points:
        # if q doesn't have any facets to conflict with, q inside the polytope!
        # count_conflicts: we need facet in conflict but ALSO ACTIVE, the function verify that
        if count_conflicts(q) > 0:
            # Found conflict: q is outside of the polytope

            edge_h = find_first_horizon_edge(q)
            list_of_horizon = find_all_horizon_edges(q, edge_h)
            # constructs facets and remove old ones
            new_facets = construct_facets(q, list_of_horizon, q_mid)
            for f in q.conflictsList:
                if f in curr_polytope and f.active:
                    disable_facet(f)
                    curr_polytope.remove(f)
            curr_polytope = curr_polytope + new_facets

    return curr_polytope
