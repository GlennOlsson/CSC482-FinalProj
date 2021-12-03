import unittest
from proj2_src.sex import approximate_sex, Sex

class SexTest(unittest.TestCase):

	def testGlennIsMale(self):
		name = "Glenn"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.male)
	
	def testLouiseIsFemale(self):
		name = "Louise"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.female)
	
	def testNonsenseIsUndefined(self):
		name = "asdfsdjfns"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.undefined)

		name = "nonsense"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.undefined)

		name = "Brfxxccxxmnpcccclllmmnprxvclmnckssqlbb11116"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.undefined)
	
	def testDifferentCases(self):
		name = "Glenn"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.male)

		name = "gLenn"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.male)

		name = "GLENN"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.male)

		name = "glenn"
		sex = approximate_sex(name)
		
		self.assertEqual(sex, Sex.male)
	
	def testOtherSex(self):
		sex = Sex.male

		self.assertEqual(sex.other(), Sex.female)

		sex = Sex.female

		self.assertEqual(sex.other(), Sex.male)

		sex = Sex.undefined

		self.assertEqual(sex.other(), Sex.undefined)