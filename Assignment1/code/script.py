import csv, re, nltk

def index(filename: str ='code/postillon.csv'):
    index = {}
    dictionary = {}
    postings_lists = []

    tokenizer = nltk.RegexpTokenizer(r"\w+")

    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        postings = []
        
        #iterate through each row of the table
        for row in reader:
            (doc_id, url, pub_date, title, news_text) = row

            #tokenize and normalize news text
            #this procedure will remove symbols like !?() etc.
            #the set data structure will remove all duplicates
            news_text_norm = set(tokenizer.tokenize(news_text.lower()))

            #generate postings
            #iterate through each term
            for term in news_text_norm:
                postings.append((term, doc_id))
            
        #sort postings  
        postings = sorted(postings[1:], key = lambda tup: tup[0])
        

        post_id = 0
        post_size = 0
        #iterate through postings
        for posting in postings:
            term, doc_id = posting
            
            if term not in dictionary:
                #upate the dictionary with the new term
                #initialize the postings size
                #save the postings id, 
                #witch is the position of the postings list
                #into the postings lists
                dictionary.update({term: [post_size+1, post_id]})
                
                #initialize a new postings list
                postings_lists.append([doc_id])

                #update postings id
                post_id +=1
            else:
                #update size of posting
                dictionary[term][0] += 1
                
                #update postings list
                postings_lists[-1].append(doc_id)

    return dictionary, postings_lists


def query(term_1: str, term_2: str = ''):
    if term_2 == '':
        #only term_1
        pass
    else:
        #term_1 AND term_2
        pass 
    pass


if __name__ == "__main__":
    index()