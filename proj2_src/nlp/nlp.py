from typing import Set, Optional, List

import wikipedia
import sys
import nltk
from nltk.corpus import wordnet as wn
import spacy
import re
from enum import Enum

from proj2_src.models.family import Person
from proj2_src.models.tree import Tree
from proj2_src.models.sex import Sex

import os

DEBUG = os.environ['DEBUG'] == "True"

nlp = spacy.load("en_core_web_sm")

father_synset = wn.synset("father.n.01")
mother_synset = wn.synset("mother.n.01")
parent_synset = wn.synset("parent.n.01")
son_synset = wn.synset("son.n.01")
daughter_synset = wn.synset("daughter.n.01")
child_synset = wn.synset("child.n.01")
brother_synset = wn.synset("brother.n.01")
sister_synset = wn.synset("sister.n.01")
sibling_synset = wn.synset("sibling.n.01")

parent_synsets = [
	father_synset,
	mother_synset,
	parent_synset
]

child_synsets = [
	son_synset,
	daughter_synset,
	child_synset
]

sibling_synsets = [
	brother_synset,
	sister_synset,
	sibling_synset
]


all_synsets = [father_synset,
	mother_synset,
	parent_synset,
	son_synset,
	daughter_synset,
	child_synset,
	brother_synset,
	sister_synset,
	sibling_synset
]

def names_with_synset(sentence, compare_synsets) -> Set[str]:
	"""Takes a sentece and synsets to compare with. Returns a set of person names associated with the 
	relation relevant for the compare_synsets"""
	words = nltk.word_tokenize(sentence)
	pos = nltk.pos_tag(words)

	s = set()

	if DEBUG:
		print("Names with syn: ", sentence, compare_synsets)

	for i in range(len(words)):
		synsets = nltk.corpus.wordnet.synsets(words[i])
		for synset in synsets:
			if synset in compare_synsets:
				has_near_nn = True
				sample_i_l = i+1
				sample_i_h = i+5
				for j in range(sample_i_l, sample_i_h):
					if j < len(pos) and pos[j][1] == "NN":
						has_near_nn = False
						break
				if has_near_nn and (pos[i-1][1] == "PRP$" or pos[i-2][1] == "NNP"):
					sample = words[sample_i_l - 1: sample_i_h]
					sample = " ".join(sample).strip()
					if DEBUG:
						print(f"ANALYSING -{sample}-")
					analzyed = nlp(sample)
					if DEBUG:
						print("Analyzed!! ", analzyed, analzyed.ents)
					for a in analzyed.ents:
						if DEBUG:
							print("ENT: ", a.text, a.label_)
						if a.label_ == "PERSON":
							if DEBUG:
								print("ACCEPTING", a.text)
							s.add(a.text)
							# return a.text
	return s

def analyze_relations(filtered):
	"""Takes sentences and returns (parents, children, siblings) tuple with sets based on sentences"""
	parent_names: Set[str] = set()
	children_names: Set[str] = set()
	sibling_names: Set[str] = set()
	for sentence in filtered:
		parent_names.update(names_with_synset(sentence, parent_synsets))
		children_names.update(names_with_synset(sentence, child_synsets))
		sibling_names.update(names_with_synset(sentence, sibling_synsets))

	# new_parents = [Person(name) for name in parent_names]
	# parents = set(new_parents)

	# new_childrens = [Person(name) for name in children_names]
	# children = set(new_childrens)

	# new_siblings = [Person(name) for name in sibling_names]
	# siblings = set(new_siblings)

	# if DEBUG:
	# 	print(parents)
	# if DEBUG:
	# 	print(children)
	# if DEBUG:
	# 	print(siblings)

	return parent_names, children_names, sibling_names


def check_mother(name, mother, text):
	#print(text)
	for i in range(len(text)):
		if text[i] in mother:
			sample = text[:i]
			my_reg = r"[^ ]+'s mother .* mother, " + mother
			#print(my_reg)
			match_1 = re.match(my_reg, text) #.[^,.]+[,.]
			match_2 = re.match(r"[^ ]+'s", text)
			if match_1 is not None:
				#print("______________________CHECK___________________________")
				#print(match_1.group(0))
				#print(match_2.group(0))
				for part in name:
					if part in match_2.group(0):
						return False
	return True
			#for part in name:
			#    if name in match_1
			#match_2.strip("'s")

# def check_regex(word, sentence, s):


def analyze_relations_2(name, filtered: List[str]):
	# I think this works better than the other one. Following this, after a match is found need to go back
	# and check the sentence to ensure it is a good match. For instance, still getting grandomther as motehr. 
	# That needs to be filtered out.
	print("___________________________________RELATIONS 2______________________________________")
	parents = set()
	children = set()
	siblings = set()
	for sentence in filtered: 
		sanitized_sentence = sentence.replace("Sr.", "Sr").replace("Jr.", "Jr")
		print("SAN: ", sanitized_sentence)
		matches = re.findall(r" daughters?[^.]+[,.]", sentence)
		for match in matches:
			if "(" in match or ")" in match:
				match = re.sub(r'\([^)]*\)', '', match)
			print("________________DAUGHTER__________________")
			print(match)
			print(sentence)
			# analyzed = nlp(match)
			analyzed = nlp(match)
			print(analyzed.ents)
			max_people_dist = 3
			curr_people_dist = 0
			for a in analyzed.ents:
				curr_people_dist += 1
				if a.label_ == "PERSON" and match.index(a.text) < 20:
				# if a.text in match and not any(map(str.isdigit, a.text)):
					#print(a.text)
					children.add(a.text)
		matches = re.findall(r" sons?[^.]+[,.]", sanitized_sentence)
		for match in matches:
			# analyzed = nlp(match)
			analyzed = nlp(match)
			#print(analyzed.ents)
			max_people_dist = 3
			curr_people_dist = 0
			for a in analyzed.ents:
				curr_people_dist += 1
				
				if a.label_ == "PERSON" and match.index(a.text) < 20:
				# if a.text in match and not any(map(str.isdigit, a.text)):
					#print(a.text)
					children.add(a.text)
		matches = re.findall(r" mother[^.]+[,.]", sanitized_sentence)
		for match in matches:
			# analyzed = nlp(match)
			analyzed = nlp(match)
			#print(analyzed.ents)
			max_people_dist = 3
			curr_people_dist = 0
			for a in analyzed.ents:
				curr_people_dist += 1
				if a.label_ == "PERSON" and match.index(a.text) < 20:
					#print("______________MOTHER____________________________________")
					#print(sentence)
					#print(a.text)
					#tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
					#print(tagged)
					#print(a.text)
					flag = check_mother(name, a.text, sentence)
					if flag:
						print("_____________ADDING RELATION________________")
						print(sentence)
						parents.add(a.text)
		matches = re.findall(r" father[^.]+[,.]", sanitized_sentence)
		for match in matches:
			# analyzed = nlp(match)
			analyzed = nlp(match)
			#print(analyzed.ents)
			max_people_dist = 3
			curr_people_dist = 0
			for a in analyzed.ents:
				curr_people_dist += 1
				if a.label_ == "PERSON" and match.index(a.text) < 20:
				# if a.text in match:
					#print(a.text)
					parents.add(a.text)
		matches = re.findall(r"[- ]sisters?[^.]+[,.]", sanitized_sentence)
		for match in matches:
			# analyzed = nlp(match)
			analyzed = nlp(match)
			print(match)
			#print(analyzed.ents)
			max_people_dist = 3
			curr_people_dist = 0
			for a in analyzed.ents:
				curr_people_dist += 1
				print(a.label_)
				if a.label_ == "PERSON" and match.index(a.text) < 20:
				# if a.text in match:    
					#print(a.text)
					siblings.add(a.text)
					print(siblings)
		matches = re.findall(r"[- ]brothers?[^.]+[,.]", sanitized_sentence)
		for match in matches:
			# analyzed = nlp(match)
			analyzed = nlp(match)
			#print(analyzed.ents)
			max_people_dist = 3
			curr_people_dist = 0
			for a in analyzed.ents:
				curr_people_dist += 1
				if a.label_ == "PERSON" and match.index(a.text) < 20:
				# if a.text in match: #a.label_ == "PERSON":
					#print(a.text)
					siblings.add(a.text)
		matches = re.findall(r" child(?:ren)?[^.]+", sanitized_sentence)
		for match in matches:
		#    print(matches.group(0))
			# analyzed = nlp(match)
			analyzed = nlp(match)
			#print(analyzed.ents)
			if "Jr" in sanitized_sentence:
				print("ENTS; ", analyzed.ents, match)
			max_people_dist = 3
			curr_people_dist = 0
			for a in analyzed.ents:
				curr_people_dist += 1
				if a.label_ == "PERSON" and match.index(a.text) < 20:
				# if a.text in match and not any(map(str.isdigit, a.text)):
					#print(a.text)
					children.add(a.text)
	return parents, children, siblings

def process_relation_sentences(name, sentences):
	"""Filters out sentences that does not contain a name, based on SpaCy. Returns set of sentences"""
	if DEBUG:
		print("___________________________________FILTERED______________________________________")
	filtered = set()
	for sentence in sentences:
		# Remove all "(born 2012) etc"
		sentence = re.sub(r' \(born \d+\)', '', sentence)
		analyzed = nlp(sentence)
		max_people_dist = 3
		curr_people_dist = 0
		for a in analyzed.ents:
			curr_people_dist += 1
			if a.label_ == "PERSON" or a.label_ == "ORG":
				filtered.add(sentence)
				break
	for sentence in filtered:
		if DEBUG:
			print(sentence)
		if DEBUG:
			print("________________________________")
	
	parents_1, children_1, siblings_1 = analyze_relations_2(name, filtered)

	parents_2, children_2, siblings_2 = analyze_relations(filtered)

	parents = parents_1.union(parents_2)
	children = children_1.union(children_2)
	siblings = siblings_1.union(siblings_2)

	return parents, children, siblings

def process_text(name, text):
	"""Takes name and text, sees what sentences are relevant and returns a Tree of
	parents, children and siblings"""
	sentences = nltk.sent_tokenize(text)

	# familial_sentences = set()
	# for sentence in sentences:
	# 	tokens = nltk.word_tokenize(sentence)
	# 	for token in tokens:
	# 		synsets = nltk.corpus.wordnet.synsets(token)
	# 		for synset in synsets:
	# 			hypernyms = synset.hypernyms()
	# 			#if synset == son_synset or son_synset in hypernyms or synset == daughter_synset or daughter_synset in hypernyms or synset == child_synset or child_synset in hypernyms or synset == father_synset or father_synset in hypernyms or synset == mother_synset or mother_synset in hypernyms or synset == parent_synset or parent_synset in hypernyms:
	# 			if synset in all_synsets:
	# 			#if synset in child_synset or child_synset in hypernyms or synset == parent_synset or parent_synset in hypernyms:
	# 			#if synset == son_synset or son_synset in hypernyms or synset == daughter_synset or daughter_synset in hypernyms or hypernyms or synset == father_synset or father_synset in hypernyms or synset == mother_synset or mother_synset in hypernyms:
	# 				familial_sentences.add(sentence)
	# for sentence in familial_sentences:
	# 	if DEBUG:
		# print(sentence)
	# 	if DEBUG:
		# print("________________________________")

	person = Person(name)

	parents, children, siblings = process_relation_sentences(name, sentences)	

	for p_name in parents:
		p = Person(p_name)
		person.add_parent(p)

	# Assume all siblings are full siblings
	for sib_name in siblings:
		sib = Person(sib_name)
		
		p1 = person.parent1
		p2 = person.parent2

		if p1 is not None:
			p1.add_child(sib)
		
		if p2 is not None:
			p2.add_child(sib)

	for c_name in children:
		c = Person(c_name)
		person.add_child(c)
	
	return Tree(person)

def process_name(name) -> Optional[Tree]:
	"""Takes name and returns a tree, if it can be created"""
	try:
		wiki = wikipedia.page(name, auto_suggest=False)
		# Replace some weird comma with regular comma
		text = wiki.content.replace(".", ". ").replace("‚", ",")
		return process_text(name, text)
	except Exception as e:
		print(e)
		return None