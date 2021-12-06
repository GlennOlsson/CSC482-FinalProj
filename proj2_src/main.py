
from proj2_src.models.family import Person, Family
from proj2_src.models.tree import Tree

from proj2_src.gd.gedcom import generate_gedcom

from typing import Set, Tuple, Optional

from proj2_src.nlp import nlp

# BarackObama66fe006eab49478fbaf58588900e3783 [shape=box, label = "Barack Obama", color = black];
def person_dot(p: Person) -> str:
	return f"{p.identifier()} [shape=box, label = \"{p.name}\", color = black];\n"

def edge_dot(p1: Person, p2: Person) -> str:
	return f"{p1.identifier()} -> {p2.identifier()} [dir=none];\n"

def add_if_not_in(p1: Person, p2: Person, s: Set[Tuple[Person, Person]]):
	if (p1, p2) not in s and (p2, p1) not in s:
		s.add((p1, p2))

def generate_dot(tree: Tree):
	people: Set[Person] = set()

	dot_str = """
digraph
{
splines = ortho;
"""

	edges: Set[Tuple[Person, Person]] = set()

	for p in tree:
		dot_str += person_dot(p)

		parent1 = p.parent1
		parent2 = p.parent2
		children = p.children

		if parent1 is not None:
			add_if_not_in(parent1, p, edges)

		if parent2 is not None:
			add_if_not_in(parent2, p, edges)

		for c in children:
			add_if_not_in(p, c, edges)
	
	dot_str += "\n"
		
	for p1, p2 in edges:
		dot_str += edge_dot(p1, p2)
	
	dot_str += "}"

	return dot_str

def main():
	try:
		name = input("Please Enter a Name: ")
		# name = "Barrack Obama"

		if len(name) < 1:
			print("Must input a name")
			main()
			return

		tree: Optional[Tree] = nlp.process_name(name)

		if tree is None:
			print(f"Could not create tree for {name}")
			return
		
		gedcome_str = generate_gedcom(tree)
		with open("output.ged", "w") as f:
			f.write(gedcome_str)

		print("GEDCOM printed to output.ged")
		
		dot_str = generate_dot(tree)
		with open("output.dot", "w") as f:
			f.write(dot_str)
		
		print("dot format printed to output.dot")

		# Requires Graphviz to run
		try:
			# (graph,) = pydot.graph_from_dot_file('output.dot')
			# graph.write_png('output.png')

			# Using the library generated some extra circle for some reason... 

			import subprocess
			subprocess.run(["dot", "-Tpng", "output.dot", "-o", "output.png"])
			print("Graphical representation printed to output.png")
		except:
			print("Could not save as png")

		print("DONE")
	except:
		print("Sorry, I am afraid I can't do that")

main()