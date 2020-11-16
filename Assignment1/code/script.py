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

class Search:

    def __init__(self, filename: str, index: tuple):
        self.filename = filename
        self.index = index

    def getPostingList(self, postID):
        postings_lists = self.index[1]
        
        #set the index of the first postings list
        idx = 0 
        #iterate through postings lists 
        for postings_list in postings_lists:
            if postID == idx:
                return postings_list
                break
            else:
                #update index
                idx += 1
    
    def query(self, term: str):
        dictionary, postings_lists = self.index
        postID = dictionary[term][1]
        postings_list = self.getPostingList(postID)

        #retrive text
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter = '\t')
            postings = []
        
            #iterate through each row of the table
            for row in reader:
                (docID, url, pub_date, title, news_text) = row
                if docID in postings_list:
                    return(docID, news_text)
        
        pass

    def query(self, term1: str, term2: str = ''):
        dictionary, postings_lists = self.index
        out_list = []

        #CASE 1: only one term
        if term2 == '':
            postID = dictionary[term1][1]
            postings_list = self.getPostingList(postID)

            #retrive text
            with open(filename, 'r') as file:
                reader = csv.reader(file, delimiter = '\t')
                postings = []
            
                #iterate through each row of the table
                for row in reader:
                    (docID, url, pub_date, title, news_text) = row
                    if docID in postings_list:
                        out_list.append((docID, news_text))
        #CASE 2: two terms
        else:
            
            intersection_list = []

            term1_postID = dictionary[term1][1]
            term2_postID = dictionary[term2][1]
            
            term1_postings_list = self.getPostingList(term1_postID)
            term2_postings_list = self.getPostingList(term2_postID)
            
            #intersection algorithm
            for term1_docID in term1_postings_list:
                for term2_docID  in term2_postings_list:
                    if term1_docID  == term2_docID :
                        intersection_list.append(term1_docID )
            
            #retrive text
            with open(filename, 'r') as file:
                reader = csv.reader(file, delimiter = '\t')
                postings = []
            
                #iterate through each row of the table
                for row in reader:
                    (docID, url, pub_date, title, news_text) = row
                    if docID in intersection_list:
                        out_list.append((docID, news_text))
        return out_list




if __name__ == "__main__":
    filename = 'IRTM/assignment1/code/postillon.csv'
    index = index()
    search = Search(filename=filename, index=index)
    
    #queries
    print(search.query('weiß', 'maß'))
    print(search.query('weiß', 'masse'))
    print(search.query('weiss', 'maße'))
    print(search.query('weiss', 'masse'))