import unittest
from typing import List
from proj2_src.tree import Tree, Node

class TestTree(unittest.TestCase):

	glenn_tree: Tree
	glenn: Node
	all_glenn_tree_nodes: List[Node]

	def setUp(self):

		glenn_node = Node("Glenn Olsson")

		glenn_dad_node = Node("Jonny Olsson")
		glenn_mom_node = Node("Christina Carlsson")

		glenn_sis1_node = Node("Josefine Törnqvist")
		glenn_sis2_node = Node("Camilla Olsson")

		glenn_node.add_parent(glenn_dad_node)
		glenn_node.add_parent(glenn_mom_node)

		glenn_mom_node.add_child(glenn_sis1_node)
		glenn_mom_node.add_child(glenn_sis2_node)

		glenn_dad_node.add_child(glenn_sis1_node)
		glenn_dad_node.add_child(glenn_sis2_node)

		self.glenn_tree = Tree(glenn_node)
		self.glenn = glenn_node
		self.all_glenn_tree_nodes = [glenn_node, glenn_dad_node, glenn_mom_node, glenn_sis1_node, glenn_sis2_node]
		assert(len(self.all_glenn_tree_nodes) == 5)

	def testGlennHas2Siblings(self):
		glenn_full_siblings = self.glenn.full_siblings()
		# should be same in this case
		glenn_siblings = self.glenn.siblings()

		self.assertSetEqual(glenn_full_siblings, glenn_siblings)
		self.assertEqual(len(glenn_full_siblings), 2)

	def testIteratesThroughAllNodes(self):

		visited = set()
		for n in self.glenn_tree:
			visited.add(n)
		
		expected_visited = set(self.all_glenn_tree_nodes)

		self.assertEqual(len(visited), len(expected_visited))
		self.assertSetEqual(visited, expected_visited)