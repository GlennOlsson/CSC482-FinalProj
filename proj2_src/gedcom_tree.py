from typing import Optional, List

from proj2_src.sex import approximate_sex, Sex
from proj2_src.family import Family, Person

class GEDCOMFamily:
	husband: Optional[Person]
	wife: Optional[Person]

	children: List[Person]

	def __init__(self, family: Family):
		sp1_sex: Sex = family.spouse1.sex if family.spouse1 is not None else Sex.undefined
		sp2_sex: Sex = family.spouse2.sex if family.spouse2 is not None else Sex.undefined

		# For case where both people have same sex, one of them will be assigned other sex
		# Can't really do anything else

		if sp1_sex == Sex.undefined and sp2_sex == Sex.undefined:
			# Just assign something, couldn't guess who was who
			self.husband = family.spouse1
			self.wife = family.spouse1
		elif sp1_sex != Sex.undefined:
			if sp1_sex == Sex.male:
				self.husband = family.spouse1
				self.wife = family.spouse2
			else:
				self.wife = family.spouse1
				self.husband = family.spouse2
		else: # sp2_sex != Sex.undefined
			if sp2_sex == Sex.male:
				self.wife = family.spouse1
				self.husband = family.spouse2
			else:
				self.husband = family.spouse1
				self.wife = family.spouse2