import wikipedia
from bs4 import BeautifulSoup

page = wikipedia.page("Barack Obama")
html = page.html()

soup = BeautifulSoup(html, "html.parser")

pass