from __future__ import annotations
from typing import Set, cast, Dict, Optional
import uuid

from proj2_src.family import Family, Person
class Tree:
	root: Family
	
	def __init__(self, root: Family):
		self.root = root
	
	def people(self):
		"""iterator for all people in tree, uncertain order"""
		visited = set()
		def _iterate(person: Person):
			yield person
			visited.add(person)
			child_fam = person.child_family
			if child_fam is not None:
				for c in child_fam.children:
					if c not in visited:
						yield from _iterate(c)
				sp1 = child_fam.spouse1
				sp2 = child_fam.spouse2


				
				if sp1 is not None and sp1 not in visited:
					yield from _iterate(sp1)
				
				if sp2 is not None and sp2 not in visited:
					yield from _iterate(sp2)
			
			parent_fams = person.parent_families
			for p_fam in parent_fams:
				for c in p_fam.children:
					if c not in visited:
						yield from _iterate(c)
				sp1 = p_fam.spouse1
				sp2 = p_fam.spouse2
				
				if sp1 is not None and sp1 not in visited:
					yield from _iterate(sp1)
				
				if sp2 is not None and sp2 not in visited:
					yield from _iterate(sp2)
		
		root_tree = self.root

		# Find some person to start with, all other will be visited eventually
		if root_tree.spouse1 is not None:
			return _iterate(root_tree.spouse1)
		elif root_tree.spouse2 is not None:
			return _iterate(root_tree.spouse2)
		else:
			for c in root_tree.children: # Will only go to first child, then break loop by returning
				return _iterate(c)
	
	def __iter__(self):
		"""Iterate trough all families in tree"""
		visited = set() # Keep track of all families yielded

		# Recursive generator for all families
		def _iterate(person: Person):
			"""yields family, then adds to visited set"""
			# visited.add(person)
			child_fam = person.child_family
			if child_fam is not None and child_fam not in visited:

				yield child_fam
				visited.add(child_fam)

				sp1 = child_fam.spouse1
				sp2 = child_fam.spouse2

				if sp1 is not None and sp1 not in visited:
					yield from _iterate(sp1)
				if sp2 is not None and sp2 not in visited:
					yield from _iterate(sp2)
				for c in child_fam.children:
					if c not in visited:
						yield from _iterate(c)

			for parent_fam in person.parent_families:
				yield parent_fam
				visited.add(parent_fam)

				sp1 = parent_fam.spouse1
				sp2 = parent_fam.spouse2

				if sp1 is not None and sp1 not in visited:
					yield from _iterate(sp1)
				if sp2 is not None and sp2 not in visited:
					yield from _iterate(sp2)
				for c in parent_fam.children:
					if c not in visited:
						yield from _iterate(c)

		root_tree = self.root

		# Find some person to start with, all other will be visited eventually
		if root_tree.spouse1 is not None:
			return _iterate(root_tree.spouse1)
		elif root_tree.spouse2 is not None:
			return _iterate(root_tree.spouse2)
		else:
			for c in root_tree.children: # Will only go to first child, then break loop by returning
				return _iterate(c)