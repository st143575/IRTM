import csv, re, nltk

def index(filename: str ='IRTM/assignment1/code/postillon.csv'):
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


def query(data: tuple, term_1: str, term_2: str = ''):
    dictionary, postings_lists = data
    intersect = []
    post_size = 0
    post_id = 0

    #CASE 1: the query contaiuns only one term
    if term_2 == '':
        #iterate through terms in dictionary
        for term in dictionary:
            if term_1 == term:
                post_size, post_id = dictionary[term]
                break
        
        #set the index of the first postings list
        idx = 0 
        #iterate through postings lists 
        for postings_list in postings_lists:
            if post_id == idx:
                return postings_list
                break
            else:
                #update index
                idx += 1
    
    #CASE 2: the query contains two terms
    else:
        #term_1 AND term_2
        term_1_post_id = dictionary[term_1][1]
        term_2_post_id = dictionary[term_2][1]
        
        #set the index of the first postings list
        idx = 0 
        #iterate through postings lists 
        for postings_list_1 in postings_lists:
            if term_1_post_id == idx:
                return postings_list_1
                break
            else:
                #update index
                idx += 1
        
        #set the index of the first postings list
        idx = 0 
        #iterate through postings lists 
        for postings_list_2 in postings_lists:
            if term_2_post_id == idx:
                return postings_list_2
                break
            else:
                #update index
                idx += 1
        
        for doc_id_1 in postings_list_1:
            for doc_id_2 in postings_list_2:
                if doc_id_1 == doc_id_2:
                    intersect.append(doc_id_1)
                if doc_id_1 > doc_id_2:
                    break

        
        return intersect



if __name__ == "__main__":
    data = index()
    print(len(query(data, 'weiß', 'maß')))
    print(len(query(data, 'weiß', 'masse')))
    print(len(query(data, 'weiss', 'maße')))
    print(len(query(data, 'weiss', 'masse')))