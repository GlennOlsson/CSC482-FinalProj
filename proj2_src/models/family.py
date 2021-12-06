from __future__ import annotations
from typing import Optional, Set, List, cast

from uuid import UUID, uuid4
from proj2_src.models.sex import approximate_sex, Sex

def childs(p1: Optional[Person], p2: Optional[Person]) -> Set[Person]:
	"""Returns children has between two people"""
	# Handle cases where not all parents are known
	if p1 is None: # If p1 is none, we cannot have set p2 either
		return set()
	if p2 is None: # p1 must be non-None here
		return p1.children
	
	# Else, knows both parents

	p1_c = p1.children
	p2_c = p2.children

	return p1_c.intersection(p2_c)

def sanitize(s: str) -> str:
	"""Sanitize string to be GEDCOM pointer acceptable"""
	return s.replace(".", "").replace(",", "").replace(" ", "").replace("-", "")

class Person:
	name: str
	sex: Sex
	_id: UUID

	parent1: Optional[Person]
	parent2: Optional[Person]

	children: Set[Person]

	def __init__(self, name: str, sex: Optional[Sex] = None):
		self.name = name
		self._id = uuid4()
		if sex is None:
			self.sex = approximate_sex(name.split()[0]) # approximate for first name before space
		else:
			self.sex = sex

		self.parent1 = None
		self.parent2 = None

		self.children = set()
	
	def add_child(self, person: Person):
		# If already in. To handle recursive calls
		if person in self.children:
			return
		self.children.add(person)
		person.add_parent(self)
	
	def add_parent(self, p: Person):
		# If person already is set to one of the parents, skip doing anything
		if p == self.parent1 or p == self.parent2:
			return
		if self.parent1 is None:
			self.parent1 = p
		else: # Assumes that parent2 is None. If adding more than 2 parents, parent2 will always be replaced
			self.parent2 = p

		p.add_child(self)

	def families(self) -> Set[Family]:
		families: Set[Family] = set()

		siblings = childs(self.parent1, self.parent2) # Siblings including person self
		child_family = Family(self.parent1, self.parent2, siblings)
		families.add(child_family)

		# Create all families where self is a parent
		for c in self.children:
			c_p1: Optional[Person] = c.parent1
			c_p2: Optional[Person] = c.parent2

			siblings = childs(c_p1, c_p2) # Siblings including c

			c_fam = Family(c_p1, c_p2, siblings)
			families.add(c_fam)
		
		return families
	
	def identifier(self) -> str:
		return f'{sanitize(self.name)}{self._id.int}'

	def pointer(self) -> str:
		"""Return a suiting GEDCOM pointer"""
		return f'@{self.identifier()[:40]}@'
	
	def __hash__(self) -> int:
		return hash(self._id)

	def __str__(self):
		return f"Person({self.name})"

class Family:
	"""Assumes that family (that can have children) are between a male and a female which is only relevant for
	GEDCOM output"""

	husband: Optional[Person]
	wife: Optional[Person]

	children: Set[Person]

	def __init__(self, s1: Optional[Person], s2: Optional[Person], children: Set[Person]):
		self.assign_parents(s1, s2)

		self.children = children
	
	def assign_parents(self, sp1: Optional[Person], sp2: Optional[Person]):
		"""Assign a husband and wife on best guess"""
		sp1_sex: Sex = sp1.sex if sp1 is not None else Sex.undefined
		sp2_sex: Sex = sp2.sex if sp2 is not None else Sex.undefined

		# For case where both people have same sex, one of them will be assigned other sex
		if sp1_sex == Sex.undefined and sp2_sex == Sex.undefined:
			# Just assign something, couldn't guess who was who
			self.husband = sp1
			self.wife = sp2
		elif sp1_sex != Sex.undefined:
			if sp1_sex == Sex.male:
				self.husband = sp1
				self.wife = sp2
			else:
				self.wife = sp1
				self.husband = sp2
		else: # sp2_sex != Sex.undefined
			if sp2_sex == Sex.male:
				self.wife = sp1
				self.husband = sp2
			else:
				self.husband = sp1
				self.wife = sp2
		
	def is_meaningful(self) -> bool:
		"""Returns if there are at least two people in this family, i.e. is meaningful"""
		i = 0
		if self.husband is not None:
			i += 1
		if self.wife is not None:
			i += 1

		i += len(self.children)

		return i >= 2
	
	def pointer(self) -> str:
		"""Return a suiting GEDCOM pointer"""
		husb = self.husband.name if self.husband is not None else "NoHusb"
		wife = self.wife.name if self.wife is not None else "NoWife"

		name = f"{sanitize(husb)}AND{sanitize(wife)}"

		return f'@{name[:40]}@'
	
	def __eq__(self, o):
		if type(o) is not Family:
			return false
		
		# Cast for mypy
		o = cast(Family, o)
		
		return self.husband == o.husband and self.wife == o.wife

	def __hash__(self) -> int:
		"""A husband and wife will only have 1 family"""
		return hash(self.husband) ^ hash(self.wife)
	
	def __str__(self) -> str:
		return f"Family(husband={self.husband}, wife={self.wife}, children={self.children})"
