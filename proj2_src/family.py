from __future__ import annotations
from typing import Optional, Set, List

from uuid import UUID, uuid4
from proj2_src.sex import approximate_sex, Sex

class Person:
	name: str
	sex: Sex
	_id: UUID

	child_family: Optional[Family]
	parent_families: Set[Family] # Can be parent in multiple families, but only in one family once

	def __init__(self, name: str):
		self.name = name
		self._id = uuid4()
		self.sex = approximate_sex(name)

		self.child_family = None
		self.parent_families = set()
	
	def __str__(self):
		return f"Person({self.name})"

class Family:

	spouse1: Optional[Person]
	spouse2: Optional[Person]

	children: Set[Person]

	_id: UUID

	def __init__(self):
		self.spouse1 = None
		self.spouse2 = None

		self.children = set()

		self._id = uuid4()
	
	def add_child(self, person: Person):
		"""Adds person as child and sets persons child_family as self"""
		self.children.add(person)
		person.child_family = self
	
	def add_spouse(self, person: Person):
		person.parent_families.add(self)
		if self.spouse1 is None:
			self.spouse1 = person
		else: # Assumes that spouse2 is None. If adding more than 2 spouses, spouse2 will always be replaced
			self.spouse2 = person
		
	def __str__(self):
		return f"Family(sp1={self.spouse1}, sp2={self.spouse2}, children={self.children})"

	def gedcom(self):
		return GEDCOMFamily(self)
