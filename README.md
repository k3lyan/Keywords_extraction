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

## How to use ?
By default, the number of keywords, the URL and the log level must be given. You can configure an environment file at the root containing these values, such as:  
`URL=https://my_url.com/`  
`NB_KW=10`  
`LOG_LEVEL=DEBUG`  
Then build the docker image at the root directory (that we call "kw-extractor" here): `docker image build -t kw-extractor .`  
Run your container by injecting the environment file (for example called ".kw_en""): `docker run --env-file=.kw_env kw-extractor`   

Pay attention ! So far the solution is implemented only for web pages in English, French or Spanish.

