import unittest
from typing import List
from proj2_src.models.tree import Tree
from proj2_src.models.family import Family, Person

class TestTree(unittest.TestCase):

	glenn_tree: Tree
	glenn: Person
	all_glenn_tree_nodes: List[Person]

	def setUp(self):

		glenn_person = Person("Glenn Olsson")

		glenn_dad_person = Person("Jonny Olsson")
		glenn_mom_person = Person("Christina Carlsson")

		glenn_sis1_person = Person("Josefine Törnqvist")
		glenn_sis2_person = Person("Camilla Olsson")

		glenn_person.add_parent(glenn_dad_person)
		glenn_person.add_parent(glenn_mom_person)

		glenn_dad_person.add_child(glenn_sis1_person)
		glenn_dad_person.add_child(glenn_sis2_person)

		glenn_mom_person.add_child(glenn_sis1_person)
		glenn_mom_person.add_child(glenn_sis2_person)

		self.glenn_tree = Tree(glenn_person)
		self.glenn = glenn_person
		self.all_glenn_tree_persons = [glenn_person, glenn_dad_person, glenn_mom_person, glenn_sis1_person, glenn_sis2_person]
		assert(len(self.all_glenn_tree_persons) == 5)

	def testPeopleIteratesThroughAllPersons(self):

		visited = set() # Easiest comparision is with set vs set, instead of list vs list as order would matter
		visited_count = 0 # To make sure that not to many items are added
		for p in self.glenn_tree:
			visited.add(p)
			visited_count += 1

		self.assertEqual(len(visited), visited_count)
		
		expected_visited = set(self.all_glenn_tree_persons)

		self.assertEqual(len(visited), len(expected_visited))
		self.assertSetEqual(visited, expected_visited)
	
	def testMeaningfulFamiliesIs1(self):
		fams = set()
		for p in self.glenn_tree:
			families = p.families()
			meaningful_fams = [f for f in families if f.is_meaningful()]
			fams.update(meaningful_fams)

		self.assertEqual(len(fams), 1)

	def testGlennsDadHasNonMeaningfulFamilies(self):
		# Will have non-meaningful family as parents are not defined
		fams = self.all_glenn_tree_persons[1].families()
		meaningful_fams = [f for f in fams if f.is_meaningful()]
		self.assertGreater(len(fams), len(meaningful_fams))