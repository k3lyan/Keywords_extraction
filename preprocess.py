import os
import sys
from datetime import datetime
import textacy
import spacy
import langid
import re
from langid.langid import LanguageIdentifier, model
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests

models = {'fr': spacy.load('fr_core_news_sm'), 'en': spacy.load('en_core_web_sm'), 'es' : spacy.load('es_core_news_sm')}

def line_cleaner(paragraph):
    return re.sub(r"[\n\r]", r"", paragraph)

def webscrap(url):
    page_response = requests.get(url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    nb_paragraphs = len(page_content.find_all("p"))
    paragraphs = [str(line_cleaner(page_content.find_all("p")[i].text)).strip('  ') for i in range(nb_paragraphs)]
    return paragraphs 

def language_detect(text, identifier):
    '''
    Function to detect the language use in a text.
    Input: text and the identifier (model used by langid)
    Output: tuple composed of the main language used and the probability that it is correct.
    '''
    identifier.set_languages(['fr', 'en', 'es'])
    return identifier.classify(text)

def get_language(paragraphs):
    '''
    Fonction to get the sentences of a file text.
    Input: file text with one sentence per line.
    Output: list of the sentences
    '''
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    count_languages = {'fr': 0, 'en': 0, 'es': 0}    
    total_count = 0
    for p in paragraphs:
        infos_language = language_detect(p, identifier)
        if infos_language[1] >= 0.7:
            count_languages[infos_language[0]] += float(infos_language[1])
            total_count += 1
        else:
            del p
    probability_max = 0
    initials = ''
    for k in count_languages.keys():
        if count_languages[k] / total_count > probability_max:
            probability_max = count_languages[k] / total_count
            initials = k  
    print('Text in {} with {}% of confidence\n'. format(initials, probability_max*100)) 
    return initials
           
def get_sentences(initials, text, stemmer):
    '''
    Function to get the sentences with their words(or stems), without the stop-words.
    Inputs: 
        initials: initials of the language mainly used in the text 
        text content: string of the preprocessed text
        stemmer: True if the stemmer should be used
    Output: array of the sentences, each sentence being an array of the words in the original sentence
    '''
    language_map = {'fr': 'french', 'en': 'english', 'es': 'spanish'}
    language = language_map[initials]
    nlp = models[initials]
    if stemmer:
        stemmer = SnowballStemmer(language)
        stop_words = list(stopwords.words(language))
        sentences = [[stemmer.stem(w.text) for w in sent if (str(w.text) not in stop_words and (w.pos_ == 'ADJ' or w.pos_ == 'NOUN'))] for sent in nlp(text).sents]
    else:
        stop_words = list(stopwords.words(language))
        sentences = [[w.text for w in sent if (str(w.text) not in stop_words and (w.pos_ == 'ADJ' or w.pos_ == 'NOUN'))] for sent in nlp(text).sents]
    return sentences
 
def txt_to_sentences(paragraphs, initials):    
    '''Tokenize a text file, calculate the stem and the postag and returns a list of the sentences with this 3 informations for each token.'''
    text = ' '.join(paragraphs).lower()
    try:
        text = textacy.preprocess.normalize_whitespace(text)
        text = textacy.preprocess.fix_bad_unicode(text, normalization=u'NFKC')
        text = textacy.preprocess.unpack_contractions(text)
        sents = get_sentences(initials, text, False)
    except ValueError as e:
        print('ERROR: {}'.format(filename))
        print('{}\n'.format(e))
        sents = []
    return sents 

def preprocess():
    '''
    Function that identifies the language used in the text, and tokenize the text keeping only adjectives and nouns.
    '''
    t0 = datetime.now() 
    paragraphs = webscrap(sys.argv[1])
    initials = get_language(paragraphs)
    sents = txt_to_sentences(paragraphs, initials)
    print('Preprocessing step: {}'.format(datetime.now() - t0))
    return sents

if __name__ == '__main__':
    preprocess()

