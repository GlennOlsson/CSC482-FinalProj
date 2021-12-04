
from proj2_src.models.family import Person, Family
from proj2_src.models.tree import Tree

from proj2_src.gd.gedcom import generate_gedcom

from proj2_src.nlp import nlp

# glenn_person = Person("Glenn Olsson")

# glenn_dad_person = Person("Jonny Olsson")
# glenn_mom_person = Person("Christina Carlsson")

# glenn_sis1_person = Person("Josefine Törnqvist")
# glenn_sis2_person = Person("Camilla Olsson")

# glenn_person.add_parent(glenn_dad_person)
# glenn_person.add_parent(glenn_mom_person)

# glenn_dad_person.add_child(glenn_sis1_person)
# glenn_dad_person.add_child(glenn_sis2_person)

# glenn_mom_person.add_child(glenn_sis1_person)
# glenn_mom_person.add_child(glenn_sis2_person)

# glenn_granddad_person = Person("Harry Olsson")
# glenn_grandmom_person = Person("Yvonne Dahlsten")
# glenn_dad_person.add_parent(glenn_granddad_person)
# glenn_dad_person.add_parent(glenn_grandmom_person)

# glenn_tree = Tree(glenn_person)
# gedcome_str = generate_gedcom(glenn_tree)

# with open("output.ged", "w") as f:
# 	f.write(gedcome_str)

def main():
	# name = input("Please Enter a Name: ")
	name = "Barack Obama"
	tree = nlp.process_name(name)
	
	gedcome_str = generate_gedcom(tree)
	with open("output.ged", "w") as f:
		f.write(gedcome_str)
main()