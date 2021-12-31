#!/usr/bin/env python3

from heredity import joint_probability

people = {
    'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
    'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
    'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

result = joint_probability(people, {"Harry"}, {"James"}, {"James"})
print(result)

passing = {"mother": 0, "father": 0}
for parent in passing:
    print(parent)


