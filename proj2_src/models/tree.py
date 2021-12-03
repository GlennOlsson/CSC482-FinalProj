from __future__ import annotations
from typing import Set, cast, Dict, Optional
import uuid

from models.family import Family, Person
class Tree:
	root: Person
	
	def __init__(self, root: Person):
		self.root = root
	
	def __iter__(self):
		"""Iterate trough all persons in tree"""
		visited_people: Set[People] = set()

		def _iterate(person: Person):
			"""yields person, adds to visited and iterates all parents and children not already visited"""
			visited_people.add(person)
			yield person

			p1: Optional[Person] = person.parent1
			p2: Optional[Person] = person.parent2

			if p1 is not None and p1 not in visited_people:
				yield from _iterate(p1)

			if p2 is not None and p2 not in visited_people:
				yield from _iterate(p2)
			
			for c in person.children:
				if c not in visited_people:
					yield from _iterate(c)
		
		return _iterate(self.root)