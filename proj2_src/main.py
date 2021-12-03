
from models.family import Person, Family
from models.tree import Tree

from gd.gedcom import generate_gedcom

from gedcom.element.element import Element
from gedcom import tags

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

glenn_tree = Tree(glenn_person)
generate_gedcom(glenn_tree)
