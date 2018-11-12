import spacy
import requests
import random

mapping = {
    'ADJ': 'adjective',
    'ADP': 'adposition',
    'ADV':	'adverb',
    'AUX':	'auxiliary',
    'CONJ':	'conjunction',
    'CCONJ': 'coordinating conjunction',
    'DET':	'determiner',
    'INTJ':	'interjection',
    'NUM':	'numeral',
    'NOUN':	'noun',
    'PART':	'particle',
    'PRON':	'pronoun',
    'PROPN': 'proper noun',
    'PUNCT': 'punctuation',
    'SCONJ': 'subordinating conjunction',
    'SYM':	'symbol',
    'VERB':	'verb',
    'SPACE':	'space',
}

input = ("Dear Genie, please make Phil less annoying").split()[3:]
print(input)
words = " ".join(input)
print(words)
key = "*********************************"

nlp = spacy.load('en_core_web_sm')
doc = nlp(words)


def get_antonyms(word, part_of_speech):
    url = f"http://words.bighugelabs.com/api/2/{key}/{word}/json"
    thesaurus = requests.get(url).json()
    try:
        antonyms = thesaurus[part_of_speech]["ant"]
        return antonyms
    except:
        synonyms = thesaurus[part_of_speech]["syn"]
        return synonyms

#get token dependencies
root = [token for token in doc if token.head == token][0]
# print("Root children", [child for child in root.children])
new_sentence = [root.orth_]
for text in doc:
    #subject would be
    if text.dep_ == "nsubj":
        if text.orth_ == "me":
            new_sentence.append("you")
        else:
           new_sentence.append(text.orth_)
new_sentence.append(
    next(child.orth_ for child in root.children)
)

word = new_sentence[-1]
print(word)
print(next(child.pos_ for child in root.children))
try:
    antonyms = get_antonyms(word, (mapping[next(child.pos_ for child in root.children)]))
except:
    antonyms = get_antonyms(word, 'adjective')

antonyms.sort(key=len)
print(antonyms)
num = random.randint(0, len(antonyms) - 1)
new_sentence[-1] = antonyms[num]

print(f"I will {' '.join(new_sentence)}!!!")
