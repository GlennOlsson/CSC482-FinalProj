from typing import Set, Optional

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
	words = nltk.word_tokenize(sentence)
	pos = nltk.pos_tag(words)

	s = set()

	print("Names with syn: ", sentence, compare_synsets)

	for i in range(len(words)):
		synsets = nltk.corpus.wordnet.synsets(words[i])
		if "Victoria" in sentence:
			print("VIKKAN", words[i], synsets)
		for synset in synsets:
			if synset in compare_synsets:
				print("IS IN COMPARE SYNSETS")
				has_near_nn = True
				sample_i_l = i+1
				sample_i_h = i+5
				for j in range(sample_i_l, sample_i_h):
					if j < len(pos) and pos[j][1] == "NN":
						pass
						print("HAS NEAR NN??")
						has_near_nn = False
						break
				if has_near_nn and (pos[i-1][1] == "PRP$" or pos[i-2][1] == "NNP"):
					print("CLOSE TO PRP and NNP")
					sample = words[sample_i_l - 1: sample_i_h]
					sample = " ".join(sample).strip()
					print(f"ANALYSING -{sample}-")
					analzyed = nlp(sample)
					print("Analyzed!! ", analzyed, analzyed.ents)
					for a in analzyed.ents:
						print("ENT: ", a.text, a.label_)
						if a.label_ == "PERSON":
							print("ACCEPTING", a.text)
							s.add(a.text)
							# return a.text
	return s

def analyze_relations(filtered):
	parent_names: Set[str] = set()
	children_names: Set[str] = set()
	sibling_names: Set[str] = set()
	for sentence in filtered:
		parent_names.update(names_with_synset(sentence, parent_synsets))
		children_names.update(names_with_synset(sentence, child_synsets))
		sibling_names.update(names_with_synset(sentence, sibling_synsets))

	new_parents = [Person(name) for name in parent_names]
	parents = set(new_parents)

	new_childrens = [Person(name) for name in children_names]
	children = set(new_childrens)

	new_siblings = [Person(name) for name in sibling_names]
	siblings = set(new_siblings)

	print(parents)
	print(children)
	print(siblings)

	return parents, children, siblings

def convert_to_tree(parents, children, siblings):
	pass

def process_relation_sentences(sentences):
	print("___________________________________FILTERED______________________________________")
	filtered = set()
	for sentence in sentences:
		analyzed = nlp(sentence)
		for a in analyzed.ents:
			if a.label_ == "PERSON":
				filtered.add(sentence)
	for sentence in filtered:
		print(sentence)
		print("________________________________")
	
	return analyze_relations(filtered)

def process_text(name, text):
	sentences = nltk.sent_tokenize(text)

	familial_sentences = set()
	for sentence in sentences:
		tokens = nltk.word_tokenize(sentence)
		for token in tokens:
			synsets = nltk.corpus.wordnet.synsets(token)
			for synset in synsets:
				hypernyms = synset.hypernyms()
				#if synset == son_synset or son_synset in hypernyms or synset == daughter_synset or daughter_synset in hypernyms or synset == child_synset or child_synset in hypernyms or synset == father_synset or father_synset in hypernyms or synset == mother_synset or mother_synset in hypernyms or synset == parent_synset or parent_synset in hypernyms:
				if synset in all_synsets:
				#if synset in child_synset or child_synset in hypernyms or synset == parent_synset or parent_synset in hypernyms:
				#if synset == son_synset or son_synset in hypernyms or synset == daughter_synset or daughter_synset in hypernyms or hypernyms or synset == father_synset or father_synset in hypernyms or synset == mother_synset or mother_synset in hypernyms:
					familial_sentences.add(sentence)
	for sentence in familial_sentences:
		print(sentence)
		print("________________________________")

	person = Person(name)

	parents, children, siblings = process_relation_sentences(familial_sentences)	

	for p in parents:
		person.add_parent(p)
		for sib in siblings:
			p.add_child(sib)
	
	for c in children:
		person.add_child(c)
	
	return Tree(person)

def process_name(name) -> Optional[Tree]:
	try:
		wiki = wikipedia.page(name, auto_suggest=False)
		text = wiki.content
		return process_text(name, text)
	except Exception as e:
		print(e)
		return None