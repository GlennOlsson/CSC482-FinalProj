import wikipedia
import sys
import nltk
from nltk.corpus import wordnet as wn
import spacy
import re
nlp = spacy.load("en_core_web_sm")
def analyze_relations(filtered):
	print("___________________________________RELATIONS______________________________________")
	parents = set()
	children = set()
	siblings = set()
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
							parents.add(("Mother", a.text))
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
							parents.add(("Father", a.text))
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
							children.add(("Daughter", a.text))
	print(parents)
	print(children)
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
	parents, children, siblings = analyze_relations(filtered)
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
	process_relation_sentences(familial_sentences)
def process_name(name):
	wiki = wikipedia.page(name, auto_suggest=False)
	text = wiki.content
	process_text(name, text)
def main():
	if len(sys.argv) == 1:
		name = input("Please Enter a Name: ")
		process_name(name)
	elif len(sys.argv) == 2:
		return
	else:
		sys.exit("Usage: python3 test.py [file.txt]")
if __name__ == "__main__":
	main()