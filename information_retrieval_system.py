import os
from collections import Counter

from nltk import word_tokenize
from nltk.stem import PorterStemmer
import regex
import math
import time
import datetime

start_time = time.time()


""" --------------------Reading Document Files-------------------- """


def reading_document_files():
    doc_ID = []
    doc_text = []
    document_file_names = os.listdir('input_files/')
    #document_file_names = sorted(document_file_names, key=lambda s: int(s[6:]))

    for each_file_name in document_file_names:
        each_file_name = 'input_files/' + each_file_name
        file_pointer = open(each_file_name, "r")
        lines = file_pointer.readlines()
        file_pointer.close()
        for line in lines:
            if line.find('<DOCNO>') != -1 and line.find('</DOCNO>') != -1:
                doc_no = line[line.find('<DOCNO>') + len('<DOCNO>'): line.find('</DOCNO>')]
                doc_ID.append(doc_no)

        each_doc_text = []
        text_status = False
        for line in lines:
            if line.find('<TEXT>') != -1:
                text_status = True
                each_doc_text = []
                continue
            elif line.find('</TEXT>') != -1:
                text_status = False
            if text_status:
                each_doc_text.append(line)
            elif not text_status and line.find('</TEXT>') != -1:
                doc_text.append(each_doc_text)

    return doc_ID, doc_text


""" --------------------Reading Document Files-------------------- """


""" ----------------------Reading Query Files--------------------- """


def reading_query_files():
    query_ID = []
    query_title = []
    query_description_title = []
    query_narrative_title = []
    query_file_names = os.listdir('query_files/')

    for each_file_name in query_file_names:
        each_file_name = 'query_files/' + each_file_name
        file_pointer = open(each_file_name, "r")
        lines = file_pointer.readlines()
        file_pointer.close()
        each_query_title = []
        each_query_description_title = []
        each_query_narrative_title = []
        description_status = False
        narrative_status = False
        for line in lines:
            if line.find('<num> Number: ') != -1:
                query_no = line[line.find('<num> Number: ') + len('<num> Number: '):-1]
                query_ID.append(query_no)

            if line.find('<title> ') != -1:
                each_query_title = line[line.find('<title> ') + len('<title> '):-1]
                query_title.append(each_query_title)
                each_query_description_title.append(each_query_title)
                each_query_narrative_title.append(each_query_title)

            if line.find('<desc> Description:') != -1:
                description_status = True
                continue
            if description_status and line == '\n':
                description_status = False
                query_description_title.append(each_query_description_title)
                each_query_description_title = []
            if description_status:
                each_query_description_title.append(line)

            if line.find('<narr> Narrative:') != -1:
                narrative_status = True
                continue
            if narrative_status and line.find('</top>') != -1:
                narrative_status = False
                query_narrative_title.append(each_query_narrative_title)
                each_query_narrative_title = []
            if narrative_status and line != '\n':
                each_query_narrative_title.append(line)

    return query_ID, query_title, query_description_title, query_narrative_title


""" ----------------------Reading Query Files--------------------- """


""" --------------------Reading Judgement Files------------------- """


def reading_judgement_files(query_dictionary, document_dictionary):
    judgement_file_names = os.listdir('judgement_files/')
    for each_file_name in judgement_file_names:
        each_file_name = 'judgement_files/' + each_file_name
        file_pointer = open(each_file_name, "r")
        lines = file_pointer.readlines()
        file_pointer.close()

    relevance_vector = {}
    for each_query_id in query_dictionary:
        relevance_vector[query_dictionary[each_query_id]] = []

    for line in lines:
        values = [word for word in line.split()]
        if values[0] in query_dictionary and values[2] in document_dictionary and int(values[3]):
            relevance_vector[query_dictionary[values[0]]].append(document_dictionary[values[2]])
    return relevance_vector


""" --------------------Reading Judgement Files------------------- """


""" --------------------Reading Stop Word Files-------------------- """


def reading_stopword_file():
    file = open("stopwordlist.txt", "r")
    lines = file.readlines()
    file.close()
    stopwords = []
    for line in lines:
        stopwords.append(line.strip())

    return stopwords


""" --------------------Reading Stop Word Files-------------------- """


""" --------------------Creating Document Dictionary-------------------- """


def making_document_dictionary(doc_ID):
    document_dictionary = {}
    inverse_document_dictionary = {}
    document_number = 1
    for each_doc_id in doc_ID:
        document_dictionary[each_doc_id] = document_number
        inverse_document_dictionary[document_number] = each_doc_id
        document_number += 1

    return document_dictionary, inverse_document_dictionary


""" --------------------Creating Document Dictionary-------------------- """

""" ----------------------Creating Query Dictionary--------------------- """


def making_query_dictionary(query_ID):
    query_dictionary = {}
    inverse_query_dictionary = {}
    query_number = 1
    for each_query_id in query_ID:
        query_dictionary[each_query_id] = query_number
        inverse_query_dictionary[query_number] = each_query_id
        query_number += 1

    return query_dictionary, inverse_query_dictionary


""" ----------------------Creating Query Dictionary--------------------- """


""" -------------------Generating Tokens From All The Texts------------------- """


def getting_token_from_doc_text(doc_text):
    all_tokens = {}
    doc_no = 1
    for each_doc_text in doc_text:
        token_list = []
        for each_line in each_doc_text:
            tokens = word_tokenize(each_line)
            for each_token in tokens:
                if each_token.isalpha():
                    token_list.append(each_token.lower())
                else:
                    temp_token = regex.split("[\W_0-9]", each_token)
                    for each_temp_token in temp_token:
                        if len(each_temp_token) and each_temp_token.isalpha():
                            token_list.append(each_temp_token.lower())

        all_tokens[doc_no] = token_list
        doc_no += 1

    return all_tokens


""" --------------------Generating Tokens From All The Texts-------------------- """

""" -------------------Generating Tokens From All The Queries------------------- """


def getting_token_from_query_title(query_title):
    all_tokens = {}
    query_no = 1
    for each_query_title in query_title:
        token_list = []
        tokens = word_tokenize(each_query_title)
        for each_token in tokens:
            if each_token.isalpha():
                token_list.append(each_token.lower())
            else:
                temp_token = regex.split("[\W_0-9]", each_token)
                for each_temp_token in temp_token:
                    if len(each_temp_token) and each_temp_token.isalpha():
                        token_list.append(each_temp_token.lower())

        all_tokens[query_no] = token_list
        query_no += 1

    return all_tokens


def getting_token_from_query_text(query_text):
    all_tokens = {}
    query_no = 1
    for each_query_text in query_text:
        token_list = []
        for each_line in each_query_text:
            tokens = word_tokenize(each_line)
            for each_token in tokens:
                if each_token.isalpha():
                    token_list.append(each_token.lower())
                else:
                    temp_token = regex.split("[\W_0-9]", each_token)
                    for each_temp_token in temp_token:
                        if len(each_temp_token) and each_temp_token.isalpha():
                            token_list.append(each_temp_token.lower())

        all_tokens[query_no] = token_list
        query_no += 1

    return all_tokens


""" -------------------Generating Tokens From All The Queries------------------- """


""" --------------------Removing Stop Words From All The Tokens-------------------- """


def removing_stop_words_from_all_tokens(all_tokens, stopwords):
    doc_no = 1
    all_tokens_without_stopwords = {}
    for i in all_tokens:
        token_list_without_stopwords = []
        for each_token in all_tokens[i]:
            if each_token not in stopwords:
                token_list_without_stopwords.append(each_token)
        all_tokens_without_stopwords[doc_no] = token_list_without_stopwords
        doc_no += 1

    return all_tokens_without_stopwords


""" --------------------Removing Stop Words From All The Tokens-------------------- """


""" --------------------Stemming The Tokens Using Porter Stemmer-------------------- """


def stemming_all_tokens(all_tokens_without_stopwords):
    stemmer = PorterStemmer()
    all_stemmed_token_list = {}
    doc_no = 1
    for i in all_tokens_without_stopwords:
        stemmed_token_list = []
        for each_token in all_tokens_without_stopwords[i]:
            stemmed_token_list.append(stemmer.stem(each_token))
        all_stemmed_token_list[doc_no] = stemmed_token_list
        doc_no += 1

    return all_stemmed_token_list


""" --------------------Stemming The Tokens Using Porter Stemmer-------------------- """


""" -----------------------------Generate Forward Index----------------------------- """


def generate_forward_index(all_stemmed_token_list):
    forward_index = {}
    doc_no = 1
    for i in all_stemmed_token_list:
        forward_index_of_each_document = []
        frequency_of_each_token = Counter(all_stemmed_token_list[i])
        sorted_token_of_each_document = sorted(frequency_of_each_token)
        for each_token in sorted_token_of_each_document:
            item_check = [item for item in forward_index_of_each_document if each_token in item]
            if not item_check:
                frequency = frequency_of_each_token[each_token]
                forward_index_of_each_document.append((each_token, frequency))
        forward_index[doc_no] = forward_index_of_each_document
        doc_no += 1
    return forward_index


""" -----------------------------Generate Forward Index----------------------------- """


""" --------------------Removing Duplicate Tokens-------------------- """


def removing_duplicate_tokens(all_stemmed_token_list):
    stemmed_token_flag = {}
    for i in all_stemmed_token_list:
        for each_token in all_stemmed_token_list[i]:
            stemmed_token_flag[each_token] = False

    all_unique_stemmed_token_list = {}
    doc_no = 1
    for a in all_stemmed_token_list:
        unique_stemmed_token_list = []
        for each_token in all_stemmed_token_list[a]:
            if not stemmed_token_flag[each_token]:
                unique_stemmed_token_list.append(each_token)
                stemmed_token_flag[each_token] = True
        all_unique_stemmed_token_list[doc_no] = unique_stemmed_token_list
        doc_no += 1

    return all_unique_stemmed_token_list


""" --------------------Removing Duplicate Tokens-------------------- """


""" --------------------Creating Term Dictionary-------------------- """


def making_term_dictionary(all_unique_stemmed_token_list):
    temp_all_unique_stemmed_token_list = []
    for a in all_unique_stemmed_token_list:
        for each_token in all_unique_stemmed_token_list[a]:
            temp_all_unique_stemmed_token_list.append(each_token)

    temp_all_unique_stemmed_token_list.sort()

    term_dictionary = {}
    term_sequence = 1
    for each_token in temp_all_unique_stemmed_token_list:
        term_dictionary[each_token] = term_sequence
        term_sequence += 1

    return term_dictionary


""" --------------------Creating Term Dictionary-------------------- """


""" ---------------Creating Term Frequency of Queries--------------- """


def making_term_frequency_of_query_text(query_tokens):
    term_frequency = {}
    for query_no in query_tokens:
        term_frequency_of_each_query = {}
        for each_term in query_tokens[query_no]:
            if each_term in term_frequency_of_each_query:
                term_frequency_of_each_query[each_term] = term_frequency_of_each_query[each_term] + 1
            else:
                term_frequency_of_each_query[each_term] = 1
        term_frequency[query_no] = term_frequency_of_each_query
    return term_frequency


""" ---------------Creating Term Frequency of Queries--------------- """


""" ---------------------Creating Inverted Index-------------------- """


def generate_inverted_index(term_dictionary, forward_index):
    inverted_index = {}
    for each_term in term_dictionary:
        inverted_index_for_each_term = []
        for doc_no in forward_index:
            forward_index_of_each_document = forward_index[doc_no]
            item_check = [item for item in forward_index_of_each_document if each_term in item]
            if item_check:
                frequency = item_check[0][1]
                inverted_index_for_each_term.append((doc_no, frequency))
        inverted_index[each_term] = inverted_index_for_each_term

    return inverted_index


""" ---------------------Creating Inverted Index-------------------- """


""" --------------------Writing Term Dictionary and Document Dictionary to File-------------------- """


def writing_dictionary_to_file(term_dictionary, document_dictionary):
    file_pointer = open("parser_output.txt", "w")
    for key in term_dictionary:
        writing_line = f'{key:20s} {term_dictionary[key]:10d}\n'
        file_pointer.writelines(writing_line)
    for key in document_dictionary:
        writing_line = f'{key:10s} {document_dictionary[key]:10d}\n'
        file_pointer.writelines(writing_line)
    file_pointer.close()
    return


""" --------------------Writing Term Dictionary and Document Dictionary to File-------------------- """


""" --------------------Writing Forward Index to File-------------------- """


def writing_forward_index_to_file(forward_index):
    file_pointer = open("forward_index.txt", "w")
    for each_doc_no in forward_index:
        writing_line = str(each_doc_no) + '     '
        for each_term_frequency in forward_index[each_doc_no]:
            writing_line = writing_line + each_term_frequency[0] + ' ' + str(each_term_frequency[1]) + '; '
        writing_line = writing_line + '\n'
        file_pointer.writelines(writing_line)
    return


""" --------------------Writing Forward Index to File-------------------- """


""" --------------------Writing Inverted Index to File-------------------- """


def writing_inverted_index_to_file(inverted_index):
    file_pointer = open("inverted_index.txt", "w")
    for each_term in inverted_index:
        writing_line = f'{each_term:20s}'
        for each_document_frequency in inverted_index[each_term]:
            writing_line = writing_line + str(each_document_frequency[0]) + ': ' + str(each_document_frequency[1]) + ', '
        writing_line = writing_line + '\n'
        file_pointer.writelines(writing_line)
    return


""" --------------------Writing Inverted Index to File-------------------- """


""" --------------------Writing Relevance Vector to File-------------------- """


def writing_relevance_vector_to_file(relevance_vector, inverse_document_dictionary, inverse_query_dictionary, file_name):
    file_pointer = open(file_name, "w")
    for each_query_no in relevance_vector:
        document_rank = 1
        for each_relevance_score in relevance_vector[each_query_no]:
            writing_line = f'{inverse_query_dictionary[each_query_no]:4s} {"    "} {inverse_document_dictionary[each_relevance_score[0]]:17s} {document_rank:3d} {"   "} {each_relevance_score[1]:.6f}\n'
            file_pointer.writelines(writing_line)
            document_rank += 1
    file_pointer.close()

    return


""" --------------------Writing Relevance Vector to File-------------------- """


""" -----------------------Generating Document tf-idf----------------------- """


def generate_document_tf_idf(doc_ID, term_dictionary, forward_index):
    document_vector = {}
    for i in range(1, len(doc_ID) + 1):
        document_vector[i] = 0

    document_vector_length = document_vector.copy()
    document_tf_idf = {}
    df = {}
    for each_term in term_dictionary:
        document_tf_idf[each_term] = document_vector.copy()
        df[each_term] = 0

    for each_doc_id in forward_index:
        term_frequency = forward_index[each_doc_id]
        for each_term_frequency in term_frequency:
            document_tf_idf[each_term_frequency[0]][each_doc_id] = document_tf_idf[each_term_frequency[0]][each_doc_id] + each_term_frequency[1]
            df[each_term_frequency[0]] = df[each_term_frequency[0]] + 1

    for each_doc_id in forward_index:
        term_frequency = forward_index[each_doc_id]
        for each_term_frequency in term_frequency:
            document_tf_idf[each_term_frequency[0]][each_doc_id] = document_tf_idf[each_term_frequency[0]][each_doc_id] * math.log10(len(doc_ID) / df[each_term_frequency[0]])
            document_vector_length[each_doc_id] = document_vector_length[each_doc_id] + document_tf_idf[each_term_frequency[0]][
                each_doc_id] ** 2
        document_vector_length[each_doc_id] = math.sqrt(document_vector_length[each_doc_id])

    for each_term in document_tf_idf:
        for each_doc_id in document_tf_idf[each_term]:
            document_tf_idf[each_term][each_doc_id] = document_tf_idf[each_term][each_doc_id] / document_vector_length[each_doc_id]

    return document_tf_idf, df


""" -----------------------Generating Document tf-idf----------------------- """


""" ---------------------Creating Vector Space for Query-------------------- """


def creating_vector_space_for_queries(ID, term_dictionary):
    vector = {}
    for i in range(1, len(ID) + 1):
        vector[i] = 0
    vector_length = vector.copy()
    tf_idf = {}
    for each_term in term_dictionary:
        tf_idf[each_term] = vector.copy()

    return tf_idf, vector_length


""" ---------------------Creating Vector Space for Query-------------------- """


""" ---------------------Generating tf-idf for Query-------------------- """


def generate_query_tf_idf(query_tf_idf, df, doc_ID, query_vector_length, term_frequency_of_query):
    for query_no in term_frequency_of_query:
        for each_query_term in term_frequency_of_query[query_no]:
            if each_query_term in query_tf_idf:
                query_tf_idf[each_query_term][query_no] = term_frequency_of_query[query_no][each_query_term]

    for each_query_term in query_tf_idf:
        for each_query_no in query_tf_idf[each_query_term]:
            query_tf_idf[each_query_term][each_query_no] = query_tf_idf[each_query_term][each_query_no] * math.log10(len(doc_ID) / df[each_query_term])
            query_vector_length[each_query_no] = query_vector_length[each_query_no] + query_tf_idf[each_query_term][each_query_no] ** 2

    for each_query_no in query_vector_length:
        query_vector_length[each_query_no] = math.sqrt(query_vector_length[each_query_no])

    for each_query_term in query_tf_idf:
        for each_query_no in query_tf_idf[each_query_term]:
            query_tf_idf[each_query_term][each_query_no] = query_tf_idf[each_query_term][each_query_no] / query_vector_length[each_query_no]

    return query_tf_idf


""" ---------------------Generating tf-idf for Query-------------------- """


""" ----------------Generating Similarity Score for Query--------------- """


def generate_similarity_score(query_dictionary, document_dictionary, term_dictionary, document_tf_idf, query_tf_idf):
    query_similarity_score = {}
    for each_query_id in query_dictionary:
        similarity_score_of_each_query = {}
        for each_doc_id in document_dictionary:
            similarity_score_of_each_query[document_dictionary[each_doc_id]] = 0
            for each_term in term_dictionary:
                similarity_score_of_each_query[document_dictionary[each_doc_id]] = similarity_score_of_each_query[document_dictionary[each_doc_id]] + document_tf_idf[each_term][document_dictionary[each_doc_id]] * query_tf_idf[each_term][query_dictionary[each_query_id]]
        query_similarity_score[query_dictionary[each_query_id]] = similarity_score_of_each_query
    return query_similarity_score


""" ----------------Generating Similarity Score for Query--------------- """


""" ----------------Generating Relevance Vector for Query--------------- """


def generate_query_relevance_vector(query_similarity_score, relevance_vector):
    query_relevance_vector = {}
    R_h = {}
    R_r = {}
    for each_query_no in query_similarity_score:
        each_query_relevance_vector = []
        each_query_R_h = 0
        each_query_R_r = 0
        for each_doc_no in query_similarity_score[each_query_no]:
            if query_similarity_score[each_query_no][each_doc_no]:
                each_query_R_h += 1
                if each_doc_no in relevance_vector[each_query_no]:
                    each_query_R_r += 1
                    each_query_relevance_vector.append((each_doc_no, query_similarity_score[each_query_no][each_doc_no]))
        each_query_relevance_vector.sort(key=lambda x: x[1], reverse=True)
        query_relevance_vector[each_query_no] = each_query_relevance_vector
        R_h[each_query_no] = each_query_R_h
        R_r[each_query_no] = each_query_R_r

    return query_relevance_vector, R_h, R_r


""" ----------------Generating Relevance Vector for Query--------------- """


""" ----------------------------Main Function--------------------------- """


def main():

    doc_ID, doc_text = reading_document_files()

    stopwords = reading_stopword_file()

    document_dictionary, inverse_document_dictionary = making_document_dictionary(doc_ID)

    all_tokens = getting_token_from_doc_text(doc_text)

    all_tokens_without_stopwords = removing_stop_words_from_all_tokens(all_tokens, stopwords)

    all_stemmed_token_list = stemming_all_tokens(all_tokens_without_stopwords)

    forward_index = generate_forward_index(all_stemmed_token_list)
    writing_forward_index_to_file(forward_index)

    all_unique_stemmed_token_list = removing_duplicate_tokens(all_stemmed_token_list)

    term_dictionary = making_term_dictionary(all_unique_stemmed_token_list)
    writing_dictionary_to_file(term_dictionary, document_dictionary)

    inverted_index = generate_inverted_index(term_dictionary, forward_index)
    writing_inverted_index_to_file(inverted_index)

    document_tf_idf, df = generate_document_tf_idf(doc_ID, term_dictionary, forward_index)

    query_ID, query_title, query_description_title, query_narrative_title = reading_query_files()

    query_dictionary, inverse_query_dictionary = making_query_dictionary(query_ID)

    all_tokens_of_query_title = getting_token_from_query_title(query_title)
    all_tokens_of_query_description_title = getting_token_from_query_text(query_description_title)
    all_tokens_of_query_narrative_title = getting_token_from_query_text(query_narrative_title)

    all_tokens_of_query_title_without_stopwords = removing_stop_words_from_all_tokens(all_tokens_of_query_title, stopwords)
    all_tokens_of_query_description_title_without_stopwords = removing_stop_words_from_all_tokens(all_tokens_of_query_description_title, stopwords)
    all_tokens_of_query_narrative_title_without_stopwords = removing_stop_words_from_all_tokens(all_tokens_of_query_narrative_title, stopwords)

    all_stemmed_tokens_of_query_title = stemming_all_tokens(all_tokens_of_query_title_without_stopwords)
    all_stemmed_tokens_of_query_description_title = stemming_all_tokens(all_tokens_of_query_description_title_without_stopwords)
    all_stemmed_tokens_of_query_narrative_title = stemming_all_tokens(all_tokens_of_query_narrative_title_without_stopwords)

    term_frequency_of_query_title = making_term_frequency_of_query_text(all_stemmed_tokens_of_query_title)
    term_frequency_of_query_description_title = making_term_frequency_of_query_text(all_stemmed_tokens_of_query_description_title)
    term_frequency_of_query_narrative_title = making_term_frequency_of_query_text(all_stemmed_tokens_of_query_narrative_title)

    query_tf_idf, query_vector_length = creating_vector_space_for_queries(query_ID, term_dictionary)

    query_title_tf_idf = query_tf_idf.copy()
    query_title_vector_length = query_vector_length.copy()
    query_title_tf_idf = generate_query_tf_idf(query_title_tf_idf, df, doc_ID, query_title_vector_length, term_frequency_of_query_title)
    query_title_similarity_score = generate_similarity_score(query_dictionary, document_dictionary, term_dictionary, document_tf_idf, query_title_tf_idf)

    query_description_title_tf_idf = query_tf_idf.copy()
    query_description_title_vector_length = query_vector_length.copy()
    query_description_title_tf_idf = generate_query_tf_idf(query_description_title_tf_idf, df, doc_ID, query_description_title_vector_length, term_frequency_of_query_description_title)
    query_description_title_similarity_score = generate_similarity_score(query_dictionary, document_dictionary, term_dictionary, document_tf_idf, query_description_title_tf_idf)

    query_narrative_title_tf_idf = query_tf_idf.copy()
    query_narrative_title_vector_length = query_vector_length.copy()
    query_narrative_title_tf_idf = generate_query_tf_idf(query_narrative_title_tf_idf, df, doc_ID, query_narrative_title_vector_length, term_frequency_of_query_narrative_title)
    query_narrative_title_similarity_score = generate_similarity_score(query_dictionary, document_dictionary, term_dictionary, document_tf_idf, query_narrative_title_tf_idf)

    relevance_vector = reading_judgement_files(query_dictionary, document_dictionary)

    query_title_relevance_vector, query_title_R_h, query_title_R_r = generate_query_relevance_vector(query_title_similarity_score, relevance_vector)
    writing_relevance_vector_to_file(query_title_relevance_vector, inverse_document_dictionary, inverse_query_dictionary, "query_title_output.txt")
    print('Performance while considering only the main query (title):')
    for each_query_no in inverse_query_dictionary:
        precision = query_title_R_r[each_query_no] / query_title_R_h[each_query_no]
        recall = query_title_R_r[each_query_no] / len(relevance_vector[each_query_no])
        print('     Performance for query ', inverse_query_dictionary[each_query_no], ': Precision = ',precision, ', Recall = ', recall)

    query_description_title_relevance_vector, query_description_title_R_h, query_description_title_R_r = generate_query_relevance_vector(query_description_title_similarity_score, relevance_vector)
    writing_relevance_vector_to_file(query_description_title_relevance_vector, inverse_document_dictionary, inverse_query_dictionary, "query_description_title_output.txt")
    print('Performance while considering the description along with the main query (description + title):')
    for each_query_no in inverse_query_dictionary:
        precision = query_description_title_R_r[each_query_no] / query_description_title_R_h[each_query_no]
        recall = query_description_title_R_r[each_query_no] / len(relevance_vector[each_query_no])
        print('     Performance for query ', inverse_query_dictionary[each_query_no], ': Precision = ', precision,', Recall = ', recall)

    query_narrative_title_relevance_vector, query_narrative_title_R_h, query_narrative_title_R_r = generate_query_relevance_vector(query_narrative_title_similarity_score, relevance_vector)
    writing_relevance_vector_to_file(query_narrative_title_relevance_vector, inverse_document_dictionary, inverse_query_dictionary, "query_narrative_title_output.txt")
    print('Performance while considering the narrative along with the main query (narrative + title):')
    for each_query_no in inverse_query_dictionary:
        precision = query_narrative_title_R_r[each_query_no] / query_narrative_title_R_h[each_query_no]
        recall = query_narrative_title_R_r[each_query_no] / len(relevance_vector[each_query_no])
        print('     Performance for query ', inverse_query_dictionary[each_query_no], ': Precision = ', precision,', Recall = ', recall)

    return


""" ----------------------------Main Function--------------------------- """


main()

print(str(datetime.timedelta(seconds = time.time() - start_time)))