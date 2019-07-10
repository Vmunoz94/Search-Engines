import inverted_index_construction as iic
import re

# if both terms postings lists intersect, then add the posting list to a answer list
# while incrementing index, if index_out_of_bounds error occures. This means there is
# nothing left to compare. So return from function.
def intersect(p1, p2):
    answer = []
    p1_index = 0
    p2_index = 0

    try:
        while p1 and p2:
            if new_dict[p1][p1_index] == new_dict[p2][p2_index]:
                add(answer, new_dict[p1][p1_index])
                p1_index += 1
                p2_index += 1
            elif new_dict[p1][p1_index] < new_dict[p2][p2_index]:
                p1_index += 1
            else:
                p2_index += 1
    finally:
        return answer

# add posting list to the answer list
def add(answer, docID):
    answer.append(docID)
    return answer

# pythonic way
# def intersect(p1, p2):
#     return list(set(new_dict[p1]).intersection(new_dict[p2]))

# read the document.txt file line by line
# store every line of the document that matches the doc_id in the answers list to the all_matched_docs string
# use doc_start to check for <DOC #>, then have # = doc_ID
def get_text(file):
    all_matched_docs = ""
    doc_start = re.compile(r"<DOC (\d+)>")
    with open(file, "r") as file:
        for line in file:
            match_doc_start = doc_start.search(line)
            if match_doc_start:
                doc_ID = int(match_doc_start.group(1))
            if doc_ID in answers:
                all_matched_docs += line
    return all_matched_docs

# write to queryResults.txt file, if first time writing to file then overwrite it's contents
# otherwise append contents
def store_text(file, docs, overwrite_file):
    if overwrite_file:
        with open(file, "w") as file:
            file.write("Search Term: \"" + user_input + "\"\n")
            file.write("Postings Lists: " + str(sorted(answers)) + "\n")
            file.writelines(docs)
            file.write("\n")
    else:
        with open(file, "a") as file:
            file.write("Search Term: \"" + user_input + "\"\n")
            file.write("Postings Lists: " + str(sorted(answers)) + "\n")
            file.writelines(docs)
            file.write("\n")
    return

# read file and create dictionary
def create_dict_from_file(file):
    new_dict = {}
    with open(file, "r") as file:
        file.readline()
        for line in file:
            term, frequency, postings_lists = line.split(",", 2)
            postings_lists = iic.tokenize(postings_lists.strip("\n"))
            new_dict[term] = [int(i) for i in postings_lists]
    return new_dict



new_dict = create_dict_from_file(iic.OUTPUT_FILE_NAME)
input_pattern = re.compile(r"^\w+ (and) \w+$", re.IGNORECASE)
keep_searching_pattern = re.compile(r"y|n", re.IGNORECASE)
search = True
create_file = True

while search:
    user_input = input("Enter your search query (ex. cat and dog):\n")
    while not input_pattern.match(user_input):
        print("Unsupported query format")
        user_input = input("Enter your search query (ex. cat and dog):\n")

    p1, a, p2 = user_input.split(" ")
    p1 = iic.text_processing(p1)
    p1 = "".join(p1)
    p2 = iic.text_processing(p2)
    p2 = "".join(p2)
    if a.lower() == "and":
        answers = intersect(p1, p2)
    all_docs = get_text(iic.INPUT_FILENAME)
    store_text("queryResults.txt", all_docs, create_file)
    create_file = False

    keep_searching = input("Want to keep searching? (y/n)\n")
    while not keep_searching_pattern.match(keep_searching.lower()):
        print("Unsupported query format")
        keep_searching = input("Want to keep searching? (y/n)")
    if keep_searching.lower() == "n":
        search = False
