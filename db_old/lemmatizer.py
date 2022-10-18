from operator import le
from nltk import stem
import pymorphy2


def lemma(text):
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(text)[0].normal_form


from nltk.stem import SnowballStemmer

def stemmer(text):
    stemmer = SnowballStemmer("russian")
    return stemmer.stem(text)


