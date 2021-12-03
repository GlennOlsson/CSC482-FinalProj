import unittest
from typing import List
from proj2_src.tree import Tree
from proj2_src.family import Family, Person

class TestTree(unittest.TestCase):

	glenn_tree: Tree
	glenn: Person
	all_glenn_tree_nodes: List[Person]

	def setUp(self):

		glenn_node = Person("Glenn Olsson")

		glenn_dad_node = Person("Jonny Olsson")
		glenn_mom_node = Person("Christina Carlsson")

		glenn_sis1_node = Person("Josefine Törnqvist")
		glenn_sis2_node = Person("Camilla Olsson")

		glenn_family = Family()

		glenn_family.add_child(glenn_node)

		glenn_family.add_child(glenn_sis1_node)
		glenn_family.add_child(glenn_sis2_node)

		glenn_family.add_spouse(glenn_dad_node)
		glenn_family.add_spouse(glenn_mom_node)

		self.glenn_tree = Tree(glenn_family)
		self.glenn = glenn_node
		self.all_glenn_tree_nodes = [glenn_node, glenn_dad_node, glenn_mom_node, glenn_sis1_node, glenn_sis2_node]
		assert(len(self.all_glenn_tree_nodes) == 5)

	# def testGlennHas2Siblings(self):
	# 	glenn_full_siblings = self.glenn.full_siblings()
	# 	# should be same in this case
	# 	glenn_siblings = self.glenn.siblings()

	# 	self.assertSetEqual(glenn_full_siblings, glenn_siblings)
	# 	self.assertEqual(len(glenn_full_siblings), 2)

	def testPeopleIteratesThroughAllNodes(self):

		visited = set()
		for n in self.glenn_tree.people():
			visited.add(n)
		
		expected_visited = set(self.all_glenn_tree_nodes)

		self.assertEqual(len(visited), len(expected_visited))
		self.assertSetEqual(visited, expected_visited)