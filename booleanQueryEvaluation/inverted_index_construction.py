# NLTK is a leading platform for building Python programs to work with human language data
# re is pythons regular expression operations
import nltk
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.porter import *
import re
from itertools import chain
from collections import defaultdict


INPUT_FILENAME = "documents.txt"
OUTPUT_FILE_NAME = "invertedIndex.txt"

# take table dictionary and merge it with the master_table dictionary
# use chain() to retain the keys of the old table
# using update() would overwrite keys
def invert_index(table):
    for k, v in chain(table.items()):
        master_table[k].append(v)
    return dict(master_table)

# text processing includes tokenizing, stemming, removing stopwords and repetition
def text_processing(sentence):
    sentence = tokenize(sentence)
    sentence = porter_stemmer(sentence)
    # sentence = snowball_stemmer(sentence)
    sentence = remove_stopwords(sentence)
    sentence = sort_and_remove_repetition(sentence)
    return sentence

# tokenize sentence using nltk tokenizer
# the regex expression /W+ is the equivalent of [^a-zA-Z0-9_]+
# re.sub replaces every not [a-zA-Z0-9_]+ with nothing
# filter out all empty strings
def tokenize(sentence):
    tokenized = nltk.word_tokenize(sentence)
    tokenized = [re.sub(r"\W+", "", t).lower() for t in tokenized]
    # tokenized = [re.sub(r"[^a-zA-Z0-9]+", "", t).lower() for t in tokenized]
    tokenized = list(filter(lambda t: t.isalnum(), tokenized))
    return tokenized

# use nltk porter stemmer
# traverse each token and stem each word
def porter_stemmer(sentence):
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in sentence]
    return stemmed_tokens

# use nltk snowball stemmer
# traverse each token and stem each word
def snowball_stemmer(sentence):
    stemmer = EnglishStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in sentence]
    return stemmed_tokens

# stopwords include the, is, at, of, on, and, a
# store keywords in a tuple to save memory
# if stopwords appear in stemmed_tokens, filter them out
def remove_stopwords(sentence):
    stopwords = ("the", "is", "at", "of", "on", "and", "a")
    stopwords_removed = list(filter(lambda st: st not in stopwords, sentence))
    return stopwords_removed

# sort the stopwords_removed list and delete repeated terms
def sort_and_remove_repetition(sentence):
    return sorted(set(sentence))


# search for the beginning of the document and correlate the docID to the document number
# read file line by line and store all lines in one giant string
# once the ending of the document in found, process the entire document text and form the dictionary
# repeat for next document
def read_from_file(file):
    doc = ""
    doc_start = re.compile(r"<DOC (\d+)>")
    doc_end = re.compile("</DOC>")
    with open(file, "r") as file:
        for line in file:
            match_doc_start = doc_start.search(line)
            match_doc_end = doc_end.search(line)
            if match_doc_start:
                docID = int(match_doc_start.group(1))
                continue
            elif match_doc_end:
                doc = text_processing(doc)
                table = {token:docID for token in doc}
                invert_index(table)
                doc = ""
                continue
            doc += line
    return

def write_to_file(file):
    with open(file, "w") as file:
        file.write("Term, Frequency, Postings Lists\n")
        for term in sorted(master_table.keys()):
            file.write(f"{term}, {len(master_table[term])}, {master_table[term]}\n")
    return

# only run if this is the file I execute
# do not run any code if this program was imported from another file
if __name__ == "__main__":
    master_table = defaultdict(list)
    read_from_file(INPUT_FILENAME)
    write_to_file(OUTPUT_FILE_NAME)
