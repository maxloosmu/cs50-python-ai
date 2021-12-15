#!/usr/bin/env python3
# https://github.com/nahueespinosa/ai50/blob/master/degrees/degrees.py

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    If no possible path, returns None.
    """

    # Initialize frontier to just the starting position
    # Our states are people and our actions are movies, which take us from
    # one actor to another.
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            return None

        # Choose a node from the frontier
        node = frontier.remove()

        # Add neighbors to frontier
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)

                # If node is the goal, then we have a solution
                if child.state == target:
                    path = []
                    while child.parent is not None:
                        path.append((child.action, child.state))
                        child = child.parent
                    path.reverse()
                    return path
                else:
                    frontier.add(child)

        # Mark node as explored
        explored.add(node.state)
