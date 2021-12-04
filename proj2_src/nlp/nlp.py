from typing import Set, Optional

import wikipedia
import sys
import nltk
from nltk.corpus import wordnet as wn
import spacy
import re

from proj2_src.models.family import Person
from proj2_src.models.tree import Tree
from proj2_src.models.sex import Sex

nlp = spacy.load("en_core_web_sm")
def analyze_relations(filtered):
	print("___________________________________RELATIONS______________________________________")
	parents: Set[Person] = set()
	children: Set[Person] = set()
	siblings: Set[Person] = set()
	for sentence in filtered:
		words = nltk.word_tokenize(sentence)
		pos = nltk.pos_tag(words)
		for i in range(len(pos)):
			if pos[i][0] == "mother":
				flag = True
				for j in range(i+1, i+5):
					if j < len(pos):
						if pos[j][1] == "NN":
							flag = False
				if (pos[i-1][1] == "PRP$" or pos[i-2][1] == "NNP") and flag:
					sample = words[i+1:i+5]
					sample = " ".join(sample)
					analzyed = nlp(sample)
					for a in analzyed.ents:
						if a.label_ == "PERSON":
							print(a.text)
							mother = Person(a.text, sex=Sex.female)
							parents.add(mother)
		for i in range(len(pos)):
			if pos[i][0] == "father":
				flag = True
				for j in range(i+1, i+5):
					if j < len(pos):
						if pos[j][1] == "NN":
							flag = False
				if (pos[i-1][1] == "PRP$" or pos[i-2][1] == "NNP") and flag:
					sample = words[i+1:i+5]
					sample = " ".join(sample)
					analzyed = nlp(sample)
					for a in analzyed.ents:
						if a.label_ == "PERSON":
							print(a.text)
							father = Person(a.text, sex=Sex.male)
							parents.add(father)
		for i in range(len(pos)):
			if pos[i][0] == "daughter":
				print(sentence)
				print(pos)
				print("________________________________")
				flag = True
				for j in range(i+1, i+5):
					if j < len(pos):
						if pos[j][1] == "NN":
							flag = False
				if (pos[i-1][1] == "PRP$" or pos[i-3][1] == "NN") and flag:
					sample = words[i+1:i+5]
					sample = " ".join(sample)
					analzyed = nlp(sample)
					for a in analzyed.ents:
						if a.label_ == "PERSON":
							print(a.text)
							daughter = Person(a.text, sex=Sex.female)
							children.add(daughter)
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

	# TODO - GLENN: CONVERT TO TREE

def process_text(name, text):
	sentences = nltk.sent_tokenize(text)
	father_synset = wn.synset("father.n.01")
	mother_synset = wn.synset("mother.n.01")
	parent_synset = wn.synset("parent.n.01")
	son_synset = wn.synset("son.n.01")
	daughter_synset = wn.synset("daughter.n.01")
	child_synset = wn.synset("child.n.01")
	brother_synset = wn.synset("brother.n.01")
	sister_synset = wn.synset("sister.n.01")
	sibling_synset = wn.synset("sibling.n.01")
	familial_sentences = set()
	for sentence in sentences:
		tokens = nltk.word_tokenize(sentence)
		for token in tokens:
			synsets = nltk.corpus.wordnet.synsets(token)
			for synset in synsets:
				hypernyms = synset.hypernyms()
				#if synset == son_synset or son_synset in hypernyms or synset == daughter_synset or daughter_synset in hypernyms or synset == child_synset or child_synset in hypernyms or synset == father_synset or father_synset in hypernyms or synset == mother_synset or mother_synset in hypernyms or synset == parent_synset or parent_synset in hypernyms:
				if synset == son_synset or synset == daughter_synset or synset == child_synset or synset == father_synset or synset == mother_synset or synset == parent_synset or synset == brother_synset or synset == sister_synset or synset == sibling_synset:
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
	except:
		return None