from __future__ import annotations
from typing import Set, cast
import uuid

class Node:
	# To keep track of unique nodes
	_id: uuid.UUID

	parents: Set[Node]
	children: Set[Node]

	name: str

	def __init__(self, name: str):
		print(f"CREATED NODE FOR {name}")
		self._id = uuid.uuid4()
		
		self.parents = set()
		self.children = set()

		self.name = name

	def __hash__(self) -> int:
		return hash(self._id)

	def __str__(self) -> str:
		return f"Node({self.name}, {self._id})"
	
	def __eq__(self, node: object) -> bool:
		if type(node) is not Node:
			return False
		
		# Cast for mypy
		n: Node = cast(Node, node)
		return self._id == n._id
	
	def add_parent(self, node: Node):
		"""Adds node as parent, and self as child of parent. Assumes person can have multiple children (polygamy relationship?)"""
		self.parents.add(node)
		# Cannot call add_parent as will recurse forever
		node.children.add(self)
	
	def remove_parent(self, node: Node):
		"""Removes node as parent, and self as child of parent"""
		self.parents.remove(node)
		node.children.remove(self)
	
	def add_child(self, node: Node):
		"""Adds node as child, and self as parent of child"""
		self.children.add(node)
		node.parents.add(self)

	def remove_child(self, node: Node):
		"""Removes node as parent, and self as parent of child"""
		self.children.remove(node)
		node.parents.remove(self)
	
	def siblings(self) -> Set:
		"""Returns all siblings that have at least one parent in common"""
		siblings_set: Set[Node] = set()
		for parent in self.parents:
			siblings_set = siblings_set.union(parent.children)
		siblings_set.remove(self)
		return siblings_set

	def full_siblings(self) -> Set:
		"""Returns all siblings that have all parents in common"""
		if len(self.parents) == 0:
			return set()
		parents_cp = self.parents.copy()

		siblings: Set = parents_cp.pop().children
		for parent in parents_cp:
			siblings = siblings.intersection(parent.children)
		siblings.remove(self)

		return siblings
class Tree:
	root: Node
	
	def __init__(self, root: Node):
		self.root = root
	
	def __iter__(self):
		visited = set()

		def _iterate(node: Node):
			"""yields node, then adds to visited set"""
			yield node
			visited.add(node)
			for p in node.parents:
				if p not in visited:
					yield from _iterate(p)
			
			for c in node.children:
				if c not in visited:
					yield from _iterate(c)

		return _iterate(self.root)