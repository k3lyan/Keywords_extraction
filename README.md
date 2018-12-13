# Keywords extraction from a website page
This module aims at implementing the k-truss graph of words method in order to extract keywords from a website page. It implements several algorithms presented in the following links: https://arxiv.org/pdf/1205.6693.pdf and https://www.aclweb.org/anthology/D16-1191.

## preprocess
Once we get the text data from the website page, several steps are required to do a proper preprocessing of the textual data:
* Webscrapping de la page Web depuis son url
* Detect the language used in the text
* Remove stop words with a language associated list of stop words
* Remove ponctuation
* Make everything lowercase
* Tokenize the text into sentences and words
* Stemming and/or lemmatization
* Postagging: adj, noun, verb

## optimization
* Density calculation
* Elbow function

## keywords_extraction
* Build inputs for the graph construction (dictionnary of the edges)
* Build the unweighted graph G
* Build the K-truss subgraphs
* Optimize by density and elbow method to get the optimal number of keywords

## Libraries needed
Install requests:
`$pip install requests`
Install beautifulsoup4:
`$pip install beautifulsoup4`
Install spacy:
`$pip install -U spacy`
Download the languages models (in our example 3 of them: french, english and spanish):
`$python -m spacy download fr_core_news_sm`
`$python -m spacy download en_core_web_sm`
`$python -m spacy download es_core_news_sm`
Install textacy:
`$pip install textacy`
Install nltk:
`$pip install -U nltk`
Install networkx:
`$pip install networkx`
Install langid:
`$pip install langid`

## How to use ?
By default, the number of keywords must be given but through the implementation of the optimization method, it is possible to get automatically the best number of keywords (see optimization.py). Through the default choice, you can thus launch the script this way:
`$python3 keywords_extraction.py url_link nb_of_keywords_wanted`
Pay attention ! So far the solution is implemented only for web pages in English, French or Spanish.

