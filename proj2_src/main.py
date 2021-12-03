from gedcom.element.element import Element
from gedcom import tags
# import wikipedia
# from bs4 import BeautifulSoup

# page = wikipedia.page("Barack Obama")
# html = page.html()

# soup = BeautifulSoup(html, "html.parser")


# def generate_gedcom(tree):
# 	gedcom.
# 	node_elements: Dict[Node, ] = dict()

e = Element(level=1, pointer="glenn", tag=tags.GEDCOM_TAG_CHILD, value="hej", crlf='\n', multi_line=True)

parent = Element(level=2, pointer="glenn_dad", tag=tags.GEDCOM_TAG_FAMILY, value="Jonny", crlf='\n', multi_line=True)
parent.add_child_element(e)
print(parent.to_gedcom_string(recursive=True))