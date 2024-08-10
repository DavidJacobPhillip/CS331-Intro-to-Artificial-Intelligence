"""
Names: Santosh Ramesh & Anshul Batish
Date: 5-30-22
Class: CS 331 Intro to Artificial Intelligence
Program: Bayes Net Classifier
Description: Performs sentiment analysis on a set of yelp reviews
References:
- https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
- https://www.w3schools.com/python/ref_string_rstrip.asp#:~:text=The%20rstrip()%20method%20removes,default%20trailing%20character%20to%20remove.
- https://www.datacamp.com/tutorial/case-conversion-python
- https://www.w3schools.com/python/python_howto_reverse_string.asp
- https://www.techiedelight.com/remove-first-character-string-python/
- https://sites.pitt.edu/~naraehan/python3/split_join.html
- https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
- https://www.delftstack.com/howto/python/python-append-list-into-another-list/#:~:text=list%20in%20Python.-,Use%20the%20extend()%20Method%20to%20Append%20a%20List%20Into,element%20of%20the%20main%20list.
- https://favtutor.com/blogs/remove-duplicates-from-list-python
- https://www.w3schools.com/python/python_functions.asp
- https://www.programiz.com/python-programming/global-keyword
- https://appdividend.com/2022/05/30/python-list-contains/#:~:text=To%20check%20if%20the%20item,not%2C%20then%20it%20returns%20false.
- https://www.delftstack.com/howto/python/python-insert-into-list/#:~:text=%2C%2078%2C%20100%5D-,Use%20the%20%2B%20Operator%20to%20Append%20an%20Element%20to%20the%20Front,them%20in%20the%20specified%20order.
- https://www.w3schools.com/python/python_file_write.asp
- https://www.techiedelight.com/remove-all-items-from-list-python/
- https://linuxhint.com/overwrite-file-python/#:~:text=To%20overwrite%20a%20file%2C%20to,txt%E2%80%9D.
- 

"""

# IMPORTS
import math


# GLOBALS
training = 'trainingSet.txt'
testing = 'testSet.txt'
sentences = []
test_sentences = []                                                 # Contains all of the sentences that are to be tested
train_sentences = []                                                # Contains all of the sentences that are to be trained
unfiltered_words = []                                               # Contains a word bank of all words
filtered_words = []                                                 # Contains a word bank of all words minus duplicates
positive = []                                                       # Stores cases of the positive sentiment
negative = []                                                       # Stores cases of the negative sentiment
trained_words = []                                                  # Stores the words that are all trained
pos_prob = []                                                       # Stores conditional probabilites of each case given a positive sentiment
neg_prob = []                                                       # Stores conditional probabilites of each case given a negative sentiment
pos_class = 0                                                       # Holds the class probability of being positive for all reviews
neg_class = 0                                                       # Holds the class probability of being negative for all reviews


# FUNCTIONS
# Pre-processes the data
def pre_processing(file_name, processed_file_name):
    global unfiltered_words, filtered_words, positive, negative, trained_words, test_sentences, train_sentences

    # Opens the training file
    with open(file_name) as file:
        # For every line in the testing file, appends a lowercase version of the sentence to the "sentences" list 
        for line in file:
            # Removing buffer spacing between class label and review, and extracting the review
            line = line.rstrip()                                        # Removes the whitespace at the end of the sentence
            line = line[::-1]                                           # Reverses the sentence such that the class label is on the left-most side
            label = int(line[0])                                        # Retrieving class label
            line = line[5:]                                             # Removes the tabs, spaces, and period at the end of each sentence
            line = line[::-1]

            # Performing further preprocessing to lowercase and remove punctuation for each line
            line = line.lower()
            for char in ",!?':*;)(": line = line.replace(char,"")
            for char in ".-/": line = line.replace(char," ")             # Replaces the periods and hyphens with spaces instead

            # Splitting each sentence into a words list and adding it to the unfiltered word list
            words = line.split()
            unfiltered_words.extend(words)

            # Appending to a list of sentences
            pair = [words, label]
            sentences.append(pair)

    # Removing duplicate words from the unfiltered_words list and sorts it
    if file_name == "trainingSet.txt":
        filtered_words = list(set(unfiltered_words)) 
        filtered_words = sorted(filtered_words)

    # Converting the list of words into a feature vector comprised of 1's and 0's based on the existence of each word
    for sentence in sentences:
        words = sentence.pop(0)
        for bank in reversed(filtered_words):
            if bank in words:
                sentence.insert(0, 1)
            else:
                sentence.insert(0, 0)

    # If the training set, use it to calibrate the probabilites
    if file_name == "trainingSet.txt":
        for sentence in sentences:
            # Appending to the positive list if class label is positive
            if sentence[len(sentence) - 1] == 1:
                positive.append(sentence)

            # Appending to the negative list if class label is negative
            else:
                negative.append(sentence)

        trained_words = list(filtered_words)
        train_sentences = list(sentences)
    else:
        test_sentences = list(sentences)

    # Outputing the results
    processed_file = open(processed_file_name, "w")
    for word in filtered_words:                                          # Printing the class header labels
        processed_file.write(word)
        processed_file.write(", ")

    processed_file.write("classlabel \n")

    for sentence in sentences:                                           # Printing the class header labels
        for binary in sentence[:-1]:
            processed_file.write(str(binary))
            processed_file.write(", ")
        processed_file.write(str(sentence[len(sentence) - 1]))
        processed_file.write("\n")

    processed_file.close()

    # Clearing lists
    sentences.clear()
    unfiltered_words.clear()

def classification():
    global positive, negative, trained_words, pos_prob, neg_prob, pos_class, neg_class, train_sentences, test_sentences

    # Calculating the probability of the review either being positive or negative (with the natural log taken)
    class_pos = math.log(len(positive) / (len(positive) + len(negative)))
    class_neg = math.log(len(negative) / (len(positive) + len(negative)))

    index = 0
    count = 0

    # Going through each word in the "trained_words" list to develop a conditional probability based on whether the word is positive or negative
    for word in trained_words:
        # Counting up the number of times a word appears in the positive list
        for pos in positive:
            if pos[index] == 1:
                count+=1
        count = (count + 1) / (len(positive) + 2)                       # Conducting latent dirichlet priors to calculate the probability
        pos_prob.append(count)
        count = 0

        # Counting up the number of times a word appears in the negative list
        for neg in negative:
            if neg[index] == 1:
                count+=1
        count = (count + 1) / (len(negative) + 2)                       # Conducting latent dirichlet priors to calculate the probability
        neg_prob.append(count)
        count = 0
        
        index+=1
    
    pos_predict = class_pos
    neg_predict = class_neg
    index = 0

    # Predicting class labels for each review in training set
    for sentence in train_sentences:
        for word in sentence[:-1]:
            # Calculating the probability that the review is positive
            if word == 1:
                pos_predict += math.log(pos_prob[index])
            else:
                pos_predict += math.log(1 - pos_prob[index])

            # Calculating the probability that the review is negative
            if word == 1:
                neg_predict += math.log(neg_prob[index])
            else:
                neg_predict += math.log(1 - neg_prob[index])
            
            index += 1
        
        # Predicting the label based on calculated probabilites
        if neg_predict > pos_predict:
            sentence.append(0)
        else:
            sentence.append(1)
        
        index = 0
        pos_predict = class_pos
        neg_predict = class_neg

    index = 0
    # Predicting class labels for each review in testing set
    for sentence in test_sentences:
        for word in sentence[:-1]:
            # Calculating the probability that the review is positive
            if word == 1:
                pos_predict += math.log(pos_prob[index])
            else:
                pos_predict += math.log(1 - pos_prob[index])

            # Calculating the probability that the review is negative
            if word == 1:
                neg_predict += math.log(neg_prob[index])
            else:
                neg_predict += math.log(1 - neg_prob[index])
            
            index += 1
        
        # Predicting the label based on calculated probabilites
        if neg_predict > pos_predict:
            sentence.append(0)
        else:
            sentence.append(1)
        
        index = 0
        pos_predict = class_pos
        neg_predict = class_neg    
    
    # Calculating accuracy of training set
    count = 0
    for sentence in train_sentences:
        if sentence[len(sentence) - 2] == sentence[len(sentence) - 1]:
            count += 1
    count = count / len(train_sentences)
    print("Training Accuracy: ", count)

    # Calculating accuracy of testing set
    count = 0
    for sentence in test_sentences:
        if sentence[len(sentence) - 2] == sentence[len(sentence) - 1]:
            count += 1
    count = count / len(test_sentences)
    print("Testing Accuracy: ", count)


# MAIN
def main():
    global testing, training, sentences, unfiltered_words, filtered_words, positive, negative, trained_words, pos_prob, neg_prob, pos_class, neg_class, test_sentences, train_sentences

    # Pre-processing both of the datasets
    pre_processing(training, "preprocessed_train.txt")
    pre_processing(testing, "preprocessed_test.txt")

    # Running classification 
    classification()

# CALLING MAIN
if __name__ == "__main__":
    main()

