###############################################################################
# Notes: 
#  - any text in a line after a "#" is a comment intended for humans to read,
#       but that the computer will ignore
#  - additionally, sets of lines can be commented out by using 3 apostrophes 
#      (''') to start and end the commented out section
#
# The parts you will have to edit are Step 1: loading files and Step 6: Look 
# up and display results 
###############################################################################

# I based this example loosely off of the answers in these posts:
# https://stackoverflow.com/questions/35562789/how-do-i-calculate-a-word-word-co-occurrence-matrix-with-sklearn
# https://stackoverflow.com/questions/27488446/how-do-i-get-word-frequency-in-a-corpus-using-scikit-learn-countvectorizer

#  First import code libraries that we will use
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from operator import itemgetter

# these two lines only need to be run once, then you can delete them or comment
# them out (they download some nlp [natural language processing] files)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

###############################################################################
# Step 1: import the text we want to process
# You can change this to load whatever files you want, saved as .txt files in the
# same directory as the python script
###############################################################################

print("loading files...") #output text to show progress

text_to_process = "" # create a variable that will hold all of the text to process

# in the code below just replace the 'pride_and_prejudice.txt' with the file 
# you want to load

# load pride_and_prejudice.txt (txt file must be in same directory as python script)
with open('pride_and_prejudice.txt', 'r', encoding="utf8") as content_file:
    text_to_process += content_file.read()

# OPTIONAL: load more files to process them as well. Just remove the '''s
'''
# load emma.txt (txt file must be in same directory as python script)
with open('emma.txt', 'r', encoding="utf8") as content_file:
    text_to_process +=  content_file.read()
'''

###############################################################################
# Step 2: split words into sections  (we use sentences here)
###############################################################################

#split text into sentences
text_as_sentences = nltk.tokenize.sent_tokenize(text_to_process)

# Note: the sentence tokenizer sometimes makes odd decisions about where to 
# split sentences. I see sometimes mulitple sentences are combined around
# quotes. For example, type in the console "text_as_sentences[212]" to see 
# sentence number 212, and you can see that it has several sentences combined.

# output progress and dispolay the first 3 sentences
print("files loaded and split into sentences:")
print(text_as_sentences[0:3])
print() #add a blankline to make output easier to read

###############################################################################
# Step 3: OPTIONAL: clean up data (remove certain types of words, stem words)
###############################################################################

# Note: remove the apostrophes at the begining and end of this section to allow
# the code to run

'''

print("processing files...")

# remove words of certain types of speech
# https://pythonprogramming.net/part-of-speech-tagging-nltk-tutorial/

# list types to remove: personal pronouns (and possessive), preposition/subordinating conjunction,
# determiner, coordinating conjunction
types_to_remove = ["PRP", "PRP$", "IN", "DT", "CC"]

for i in range(len(text_as_sentences)): # for the index of each sentence
    sentence = text_as_sentences[i] # get sentence number i
    sentence_words = nltk.word_tokenize(sentence) #split the sentence into words
    tagged_words = nltk.pos_tag(sentence_words)  #get the tags for each word
    filtered_sentence = "" # create a new sentence for just the filtered word 
    for tagged_word in tagged_words: # for each tagged words
        if(tagged_word[1] not in types_to_remove): #if it isn't in our list of types to remove
            filtered_sentence += " " + tagged_word[0] #add it to our filtered sentence
    text_as_sentences[i] = filtered_sentence # replace the sentence with our new filtered sentence


# Stem all the words (e.g., "speaking" -> "speak")
# you wont be able to select the word "speaking" anymore
# if you want to choose a word, run, for example, ps.stem("speaking") to see what you should select
ps = nltk.stem.PorterStemmer() #initialize the PorterStemmer
for i in range(len(text_as_sentences)):  # for the index of each sentence
    sentence = text_as_sentences[i] # get sentence number i
    sentence_words = nltk.word_tokenize(sentence) #split the sentence into words
    stemmed_sentence = "" # create a new sentence for the stemmed words
    for word in sentence_words: # for each word
        stemmed_sentence += " " + ps.stem(word) #add the stemmed version of the word
    text_as_sentences[i] = stemmed_sentence # replace the sentence with our new filtered sentence
    
# output progress and dispolay the first 3 sentences
print("files processed:'")
print(text_as_sentences[0:3])
print() #add a blankline to make output easier to read

'''

###############################################################################
# Step 4: find the co-occurance matrix for all words in the text              #
###############################################################################

# set up the code for count ing words (you can change the setup to count phrases too). 
count_model = CountVectorizer()

# calculate which words appear in which sentences
#    occurances_by_sentence is a matrix where:
#       * each columns represents a word
#       * each row represent a sentences
#       * the values are the number of times the word occurs in the sentence
occurances_by_sentence = count_model.fit_transform(text_as_sentences)

# get the information of which word goes with which column number. We need to 
# be able to look up in either diection
#  vocabIndexes lets you take a word and look up its column index
vocab_to_index = count_model.vocabulary_
#  indexToVocab lets you take a column index and look up the word
index_to_vocab = dict([[v,k] for k,v in vocab_to_index.items()])


#OPTIONAL: only count a word once per sentence (even if it is there more than once)
#       e.g. In the sentence: "It was really, really, really good."
#       if you don't run the following line, "really" counts 3 times
#       if you run the following line, it only counts as once

# occurances_by_sentence[occurances_by_sentence > 1] = 1 


# find the number of times each word occurs in the documents
word_occurances = occurances_by_sentence.toarray().sum(axis=0)

# use matrix multiplication to get how often each word co-occurs in the same 
# sentence with each other potential word.
word_cooccurances = (occurances_by_sentence.T * occurances_by_sentence)

# output progress
print("word occurances and coocrrances found")
print()

###############################################################################
# Step 5: define custom functions to help retrieve and display information               
###############################################################################

# This function takes as input a term (e.g., "elizabeth") and displays the 
# number of times that term appeared
def display_occurance_count(term):
    term_index = vocab_to_index[term]
    word_count = word_occurances[term_index]
    # output the occurance count
    print(f'"{term}" appeared {word_count} times')
    print() #add an extra blank line
       
    
# This function finds the occurance count of all words and sorts them. It then
# returns the result to the code which calls this function.
def get_occurances_sorted():
    # make a list of the occurances so we can sort occurances easier
    term_occurrances = list() # start an empty list
    #for each word_occurance, append the word and the occurance to the list
    for i in range(len(word_occurances)): # get each index of word_occurances
        # add a tuple: (term, word occurance count)
        term_occurrances.append(
            (index_to_vocab[i], word_occurances[i])
        )
        
    # sort the list by the occurance, backward so the highest occurance is first
    term_occurrances.sort(key=itemgetter(1), reverse=True)
    
    # return this list to the code which calls it
    return term_occurrances


# This function takes as input a number (e.g., 10) and displays the 
# most common terms with the counts
def dislay_top_occurances(numTerms):
    #
    occurances_sorted = get_occurances_sorted() # get the sorted occurances
    top_occurances = occurances_sorted[:numTerms] # select the first numTerms of them
    # output the top occurances
    print(f'top {numTerms} words')
    print(top_occurances)
    print() #add an extra blank line


# This function takes a term and finds the co-occurance counts of all words
# with that term. It then sorts the results and returns them to the code which
# calls this function.
def get_cooccurances_sorted(term):
    term_index = vocab_to_index[term] #get the index of the provided term
    
    # make a list of the occurances so we can sort occurances easier
    term_cooccurrances = list()
    
    # for each possible other term index, we will add the cooccurance info to the list 
    for other_term_index in range(word_cooccurances.shape[0]):
        other_term = index_to_vocab[other_term_index] #get the other term
        cooccurance = word_cooccurances[term_index, other_term_index] # get the cooccurance info
        
        #OPTIONAL: to get proportional co-occurances replace the above line with:
        #cooccurance =  word_cooccurances[term_index, other_term_index] / word_occurances[other_term_index]
        
        if(cooccurance > 0): #only bother adding therms that actually co-occured
            # add a tuple: (other term, word co-occurance count)
            term_cooccurrances.append(
                    (other_term, cooccurance)
            )
    
    # sort the list by the cooccurance, backward so the highest occurance is first
    term_cooccurrances.sort(key=itemgetter(1), reverse=True)
    
    # return this list to the code which calls it
    return term_cooccurrances
        
# This function takes as input a term and a number (e.g., "elizabeth", 10) and 
# displays the most common cooccurances with the term
def display_top_cooccurances(term, numTerms):
    #use our custom get_cooccurances_sorted function to get cooccurance info
    cooccurances_sorted = get_cooccurances_sorted(term) 
    top_cooccurances = cooccurances_sorted[:numTerms] # get the first numTerms items in the list
    # output the top cooccurances
    print(f'top {numTerms} terms co-occuring with "{term}: ')
    print(top_cooccurances)
    print() #add an extra blank line
           

# This function takes as input two term (e.g., "elizabeth", "pride") and 
# displays how often those terms co-occure
def display_terms_cooccurance(term_1, term_2):
    # get the term 1 and term 2 indexes
    term_1_index = vocab_to_index[term_1]
    term_2_index = vocab_to_index[term_2]
    # get the coocurance value from the word_cooccurances matrix
    cooccurance = word_cooccurances[term_1_index, term_2_index]
    # output the top cooccurances
    print(f'"{term_1}" co-occurs with "{term_2}" {cooccurance} times.')
    print() #add an extra blank line
    

###############################################################################
# Step 6: Look up and display results in the console, probably over there --->
# Use the custom functions defined above to do this.
# TODO: You can modify and copy and paste these lines to ask your own questions
###############################################################################

dislay_top_occurances(40) # display the top 40 words

display_occurance_count("elizabeth") # display how many times "elizabeth" appeared
display_top_cooccurances("elizabeth", 40) # display top 40 words that appeared with "elizabeth"

display_occurance_count("pride") # display how many times "pride" appeared
display_top_cooccurances("pride", 40) # display top 40 words that appeared with "pride"

display_terms_cooccurance("elizabeth", "pride") # display how many times "elizabeth" appeared with "pride"
display_terms_cooccurance("darcy", "pride") # display how many times "darcy" appeared with "pride"


