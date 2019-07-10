import positional_inverted_index_construction as piic
import re
from collections import Counter
from itertools import chain
from collections import defaultdict
import math
from collections import OrderedDict

def evaluate_proxomity_operator(proximity_window, first_word, second_word):
    # The next word is one position away
    proximity_window += 1
    matched_docs = []

    first_words_postings_lists = list(new_dict[first_word]["right side"].keys())
    second_words_postings_lists = list(new_dict[second_word]["right side"].keys())

    postings_list_union = intersect(first_words_postings_lists, second_words_postings_lists)

    for i in postings_list_union:                               # i = docID
        for j in new_dict[first_word]["right side"][i]:         # j = first word position in docID
            for k in new_dict[second_word]["right side"][i]:    # k = second word position in docID
                if j > k:   continue                            # first word position cant be after second word
                elif j + proximity_window < k: continue         # second word position is too far
                else: matched_docs.append(i)

    return matched_docs

def score_proximity_documents(documents):
    # create dict with {docID:tf}
    counter = dict(Counter(documents))

    for did,tf in counter.items():
        counter[did] = (1 + math.log2(tf)) * math.log2(10 / len(counter.keys()))

    # scored_documents dict will contain {docID: list[tf-idf score for each term]}
    for k, v in chain(counter.items()):
        scored_documents[k].append(v)

    return scored_documents

def score_free_text_documents(query):
    for word in query:
        counter = dict(Counter(new_dict[word]["right side"]))
        # create dict with {docID:tf}
        for did,positions in counter.items():
            counter[did] = len(positions)

        for did, tf in counter.items():
            counter[did] = (1 + math.log2(tf)) * math.log2(10 / len(counter.keys()))

        # scored_documents dict will contain {docID: list[tf-idf score for each term]}
        for k, v in chain(counter.items()):
            scored_documents[k].append(v)

    return scored_documents

def score_all_documents():
    # sum all tf-idf scores
    for k,v in scored_documents.items():
        scored_documents[k] = sum(v)

    # order dict based on tf-idf scores
    ordered_scored_documents = OrderedDict(sorted(scored_documents.items(), key = lambda t: t[1]))
    return ordered_scored_documents


# pythonic way
def intersect(p1, p2):
    return sorted(list(set(p1).intersection(p2)))

# read the document.txt file line by line
# store every line of the document that matches the doc_id in the answers list to the all_matched_docs string
# use doc_start to check for <DOC #>, then have # = doc_ID
def get_text(file, docID):
    all_matched_docs = ""
    doc_start = re.compile(r"<DOC (\d+)>")

    with open(file, "r") as file:
        for line in file:
            match_doc_start = doc_start.search(line)
            if match_doc_start:
                doc_ID = int(match_doc_start.group(1))
            if doc_ID == docID:
                all_matched_docs += line
    return all_matched_docs

# write to queryResults.txt file, if first time writing to file then overwrite it's contents
# otherwise append contents
def store_text(file, all_documents, overwrite_file):
    if overwrite_file:
        with open(file, "w") as file:
            file.write("Search Term: \"" + user_input + "\"\n")
            file.write(f"Postings Lists: {docs}\n")
            for doc in docs:
                file.write(f"docID {doc} has ranking {format(ordered_documents[doc], '.2f')}\n")
            file.writelines(all_docs)
            file.write("\n")
    else:
        with open(file, "a") as file:
            file.write("Search Term: \"" + user_input + "\"\n")
            file.write(f"Postings Lists: {docs}\n")
            for doc in docs:
                file.write(f"docID {doc} has ranking {format(ordered_documents[doc], '.2f')}\n")
            file.writelines(all_docs)
            file.write("\n")
    return

# read file and create dict of dict of dic
def create_dict_from_file(file):
    new_dict = {}
    right_side_of_index = re.compile(r"(\d+)")
    with open(file, "r") as file:
        file.readline()
        for line in file:
            left_side, right_side = line.split("->")

            term, document_frequency = left_side.split(":")
            term = term[1:]
            document_frequency = int(document_frequency[::-1][2:])

            right_side = [int(i) for i in right_side_of_index.findall(right_side)]

            doc_dict = {}
            while right_side:
                positions = []
                doc_id = right_side[0]
                right_side = right_side[1:]
                term_frequency = right_side[0]
                right_side = right_side[1:]

                for i in range(term_frequency):
                    positions.append(right_side[i])

                right_side = right_side[term_frequency:]


                positions_dict = {doc_id:positions}
                doc_dict.update(positions_dict)


            temp_dict = {term: {"df": document_frequency, "right side": doc_dict}}
            new_dict.update(temp_dict)

    return new_dict



new_dict = create_dict_from_file(piic.OUTPUT_FILE_NAME)
scored_documents = defaultdict(list)
all_docs = ""

input_pattern = re.compile(r"(\d+\(\w+ \w+\))", re.IGNORECASE)
keep_searching_pattern = re.compile(r"y|n", re.IGNORECASE)
search = True
create_file = True

while search:
    user_input = input("Enter your search query:\n")
    updated_user_input = user_input

    for i in range(len(input_pattern.findall(user_input))):
        proximity_operator = input_pattern.findall(user_input)[i]

        proximity_digit = re.match("^\d+", proximity_operator)
        proximity_digit = int(proximity_digit.group(0))

        proximity_words = re.findall("\w+ \w+", proximity_operator)
        word_1, word_2 = proximity_words[0].split(" ")
        word_1 = piic.text_processing(word_1)[0]
        word_2 = piic.text_processing(word_2)[0]

        proximity_operator_documents = evaluate_proxomity_operator(proximity_digit, word_1, word_2)
        score_proximity_documents(proximity_operator_documents)

        updated_user_input = updated_user_input.replace(proximity_operator, "")

    updated_user_input = piic.text_processing(updated_user_input)
    score_free_text_documents(updated_user_input)
    ordered_documents = score_all_documents()
    scored_documents.clear()

    docs = list(ordered_documents.keys())[::-1]
    for doc in docs:
        all_docs += get_text(piic.INPUT_FILENAME, doc)

    store_text("queryResults.txt", all_docs, create_file)
    all_docs = ""
    create_file = False







































    # p1, a, p2 = user_input.split(" ")
    # p1 = piic.text_processing(p1)
    # p1 = "".join(p1)
    # p2 = piic.text_processing(p2)
    # p2 = "".join(p2)
    # if a.lower() == "and":
    #     answers = intersect(p1, p2)
    # all_docs = get_text(piic.INPUT_FILENAME)
    # store_text("queryResults.txt", all_docs, create_file)
    # create_file = False
    #
    # keep_searching = input("Want to keep searching? (y/n)\n")
    # while not keep_searching_pattern.match(keep_searching.lower()):
    #     print("Unsupported query format")
    #     keep_searching = input("Want to keep searching? (y/n)")
    # if keep_searching.lower() == "n":
    #     search = False
