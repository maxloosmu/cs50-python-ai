#!/usr/bin/env python3
import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # 1. Extract person_id of source and target.
    print(source)
    print(target)
    # 1.1. Create QueueFrontier, explored.
    queue = QueueFrontier()
    explored = StackFrontier()

    # 2. Add person_id of source to Node and QueueFrontier.
    # 5. Move old person_id from QueueFrontier to explored.
    start = Node(source, None, get_next_person_id)
    queue.add(start)
    print(queue.contains_state(source))
    removed_node = queue.remove()
    if not explored.contains_state(removed_node.state):
        explored.add(removed_node)
    print(explored.contains_state(removed_node.state))
    start.action(start, explored)
    # print(people)
    # print()
    # print(movies)

    # 3. Create action function to extract list of movie_id
    # from movies dict's "stars" attribute based on person_id.
    # 4. Create action function to extract list of person_id
    # from people dict's "movies" attribute based on movie_id.

    # 6. Add new person_id list to QueueFrontier.
    # 7. Check each person_id to see if target person_id is found.
    # 8. If not found, repeat comments 3. to 7.
    # until all person_id checked.

    # TODO
    # raise NotImplementedError


def get_next_person_id(current_node, explored):
    """
    This is the action function to extract list of movie_id
    from people's "movies" attribute based on person_id,
    and then extract list of person_id
    from people dict's "movies" attribute based on movie_id.
    """
    mov_pers_list = []
    next_movies = people[current_node.state]["movies"]
    print(next_movies)
    for movie_id in next_movies:
        next_people = movies[movie_id]["stars"]
        print(next_people)
        for person_id in next_people:
            if explored.contains_state(person_id):
                print(person_id)
                continue
            else:
                mov_pers_list.append((movie_id, person_id))
    print(mov_pers_list)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
