import unittest
from proj2_src.nlp.nlp import names_with_synset ,analyze_relations ,process_relation_sentences ,process_text ,process_name

class NLPTest(unittest.TestCase):

	# Is root function of file so if this is fine, all others are fine too
	def testProcessNameAlwaysExitsGracefully(self):
		try:
			name = "Barack Obama"
			process_name(name)
			
			name = ""
			process_name(name)

			name = " "
			process_name(name)

			name = "\t"
			process_name(name)

			name = None
			process_name(name)

			name = "BJÖÖÖRN"
			process_name(name)

			name = "ĦÖȷȈ˸ʳӦֵۦ߆޵ީީୗ୆୅ଃ଒"
			process_name(name)

		except:
			self.fail(f"processName() raised ExceptionType unexpectedly! Name={name}")