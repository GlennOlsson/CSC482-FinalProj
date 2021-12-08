from enum import Enum

male_file = "male_names.txt"
female_file = "female_names.txt"

male_names = set()
female_names = set()

with open(male_file) as f:
	names = f.read()

	male_names = set(names.split("\n"))

with open(female_file) as f:
	names = f.read()

	female_names = set(names.split("\n"))

class Sex(Enum):
	male = 0
	female = 1
	undefined = 2

	def other(self):
		if self == Sex.undefined:
			return Sex.undefined

		return Sex(self.value ^ 1)

def approximate_sex(name: str):
	name_l = name.lower()
	if name_l in male_names:
		return Sex.male
	if name_l in female_names:
		return Sex.female
	else:
		return Sex.undefined