from models.tree import Tree
from models.family import Person, Family

from typing import Optional, Set, List

from gedcom.element.element import Element
from gedcom import tags

# 0 @glenn@ INDI
# 1 NAME Glenn Olsson
# 1 FAMC @F1@
# 1 FAMS @F2@
def person_gedcom(p: Person, fams: List[Family]) -> Element:
	ind_elem = Element(level=0, pointer=p.pointer(), tag=tags.GEDCOM_TAG_INDIVIDUAL, value="")
	
	name_elem = Element(level=1, pointer="", tag=tags.GEDCOM_TAG_NAME, value=p.name)
	ind_elem.add_child_element(name_elem)

	for fam in fams:
		# One family where p is the child, rest are parent families
		tag: str
		if p in fam.children:
			tag = tags.GEDCOM_TAG_FAMILY_CHILD
		else:
			tag = tags.GEDCOM_TAG_FAMILY_SPOUSE

		elem = Element(level=1, pointer="", tag=tag, value=fam.pointer())
		ind_elem.add_child_element(elem)

	return ind_elem

# 0 @F1@ FAM
# 1 HUSB @jonny@
# 1 WIFE @tina@
# 1 CHIL @glenn@

def family_gedcom(fam: Family) -> Element:
	"""Family must be meaningful, see Family declaration"""
	fam_elem = Element(level=0, pointer=fam.pointer(), tag=tags.GEDCOM_TAG_FAMILY, value="")

	if fam.husband is not None:
		husb_elem = Element(level=1, pointer="", tag=tags.GEDCOM_TAG_HUSBAND, value=fam.husband.pointer())
		fam_elem.add_child_element(husb_elem)

	if fam.wife is not None:
		wife_elem = Element(level=1, pointer="", tag=tags.GEDCOM_TAG_WIFE, value=fam.wife.pointer())
		fam_elem.add_child_element(wife_elem)

	for c in fam.children:
		child_elem = Element(level=1, pointer="", tag=tags.GEDCOM_TAG_CHILD, value=c.pointer())
		fam_elem.add_child_element(child_elem)

	return fam_elem

def gedcom_str(e: Element) -> str:
	res = e.to_gedcom_string()
	for c in e.get_child_elements():
		res += gedcom_str(c)

	return res

def generate_gedcom(tree: Tree) -> str:
	"""Generate the GEDCOM string represented by the tree"""
	families: Set[Family] = set()

	gedcom_root = Element(level=0, pointer="", tag="HEAD", value="")

	for p in tree:
		meaningful_families = [f for f in p.families() if f.is_meaningful()]
		families.update(meaningful_families)

		p_elems = person_gedcom(p, meaningful_families)
		gedcom_root.add_child_element(p_elems)
	
	# After to make sure each family is only generated once
	for fam in families:
		fam_elems = family_gedcom(fam)
		gedcom_root.add_child_element(fam_elems)
	
	gedcom_end = Element(level=0, pointer="", tag="TRLR", value="")
	gedcom_root.add_child_element(gedcom_end)

	return gedcom_str(gedcom_root)