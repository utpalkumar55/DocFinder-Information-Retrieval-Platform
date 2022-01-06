# Simple-Information-Retrieval-System
This project demonstrates a simple Information Retrieval System using basic functionalities. This project contains three major components which are Text Parser, Indexer and Retrieval System.

Text Parser processes the initial provided documents and creates document dictionary and term dictionary. The following tasks are done by Text Parser.
* Reading in document numbers and documents texts separately
* Reading stopwords from the provided stopword file
* Creating Document Dictionary
* Tokenizing document texts of each document
* Removing stopwords from all the tokens
* Stemming all the tokens using Porter Stemmer algorithm
* Creating Term Dictionary

Indexer creates Forward Index and Inverted Index for the entire document collection. The following tasks are done by the Indexer.
* Frequency of every token is calculated for each document after the stemming process
* All tokens are sorted alphabetically for each individual document
* Forward Index is created from the sorted token frequency
* Inverted Index is created using Term Dictionary and Forward Index

Retrieval System parses the query file and processes every query considering three categories which are the main query (title), the description along with the main query (description + title), and the narrative along with the main query (narrative + title). This system also assigns weights to both document and query terms in the vector space model by calculating (TF * IDF). Moreover, it calculates cosine similarity to find the relevance between the queries and the documents. Furthermore, it calculates precision and recall by comparing the retrieved result with the provided judgement file. The precision and recall display the performance comparison among the aforementioned three categories. The following tasks are done by the Retrieval System.
* Reading query title, query description and title, and query narrative and title for each query separately
* Creating Query Dictionary from all query numbers
* Tokenize query title, query description and title, and query narrative and title for each query separately
* Removing stopwords from all the tokens of query title, query description and title, and query narrative and title
* Stemming all the tokens of query title, query description and title, and query narrative and title
* Creating Term Frequency of query title, query description and title, and query narrative and title
* Creating vector space for query title, query description and title, and query narrative and title
* Calculate (TF * IDF) of each term for query title, query description and title, and query narrative and title
* Calculating Similarity Score for query title, query description and title, and query narrative and title against each document
* Reading in the judgement file and creating Relevance Vector
* Generating Relevance Vector for query title, query description and title, and query narrative and title where documents are sorted based on similarity score
* Counting the number of documents in the hit set and the number of relevant documents in the hit set
* Calculating Precision and Recall for each query title, query description and title, and query narrative and title

Resources: The following resources are used in this project.
* TREC dataset
* Stop words list
* Word Tokenizer and Porter Stemmer from NLTK package
* Relevance judgement file (main.qrels)
* Query set (topics.txt)

Output: The following files are produced as a result of this project.
* parser_output.txt: This file contains the Term Dictionary and Document Dictionary.
* forward_index.txt: This file contains term frequency of each term alphabetically sorted for each document
* inverted_index.txt: This file contains document frequencies of each document for each term numerically sorted
* query_title_output.txt: This file contains relevant document ranked from highest similarity score to lowest along with query number for each query title only
* query_description_title_output.txt: This file contains relevant document ranked from highest similarity score to lowest along with query number for each query description along with title
* query_narrative_title_output.txt: This file contains relevant document ranked from highest similarity score to lowest along with query number for each query narrative along with title

Term Weighting and Normalization Scheme: This project uses (TF * IDF) weighting scheme for both the query and document in this project. Also, I divided each term weight by Euclidian length as a normalization scheme.

System Performance Comparison: The precision and recall for each query while considering the title only are given below.

![fig1](https://user-images.githubusercontent.com/3108754/148436667-47796edc-f7d6-43a2-94b9-106e24f11bfb.JPG)

The precision and recall for each query while considering the description along with the title are given below.

![fig2](https://user-images.githubusercontent.com/3108754/148436721-eeb8ab25-3bf0-4882-88a2-9d900e830879.JPG)

The precision and recall for each query while considering the narrative along with the title are given below.

![fig3](https://user-images.githubusercontent.com/3108754/148436780-899087f0-54eb-41d9-b460-eb6185ae9d61.JPG)

According to the results shown above it is evident that, the recall value while considering the query description and title is better than considering query title only for each query. Subsequently, the recall value while considering the query narrative and title is better than considering query description and title for each query.

From the precision results it is observed that, the precision value while considering query description and title decreases compared to while considering query title only for each query. Moreover, the precision value while considering query narrative and title decreases compared to while considering query description and title for each query. The reason behind that is, the Retrieval System finds more relevant documents when more details are provided.
