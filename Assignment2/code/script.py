import csv, re, nltk

def index(filename: str):
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
        self.dictionary, self.postings_lists = index
        self.bigrams_index = self.getBigramIndex()
        self.bigrams_dictionary, self.bigrams_postings_lists = self.bigrams_index

    def getPostingList(self, postings_listID):
        return self.postings_lists[postings_listID]
    
    def getTermBigrams(self, term: str):
        # bigrams for wildcards on the left side
        if term[0] == '*':
            tuple_bigrams = tuple(list(nltk.bigrams(term)) + [(term[-1], '$')])[1:]
        # bigrams for wildcards on the right side
        elif term[-1] == '*':
            tuple_bigrams = tuple([('$', term[0])] + list(nltk.bigrams(term)))[:-1]
        else:
            tuple_bigrams = tuple([('$', term[0])] + list(nltk.bigrams(term)) + [(term[-1], '$')])
        
        bigrams = []
        for bigram in tuple_bigrams:
                #join the bigram tuple into one string
                bigrams.append((''.join([char for char in bigram])).strip())

        return tuple(bigrams)
    
    def getBigramIndex(self): 
        #generate a new dictionary witch contains 
        #bigrams of the terms as the key
        bigrams_dictionary = {}
        for term in self.dictionary:
            bigrams_dictionary.update({self.getTermBigrams(term): self.dictionary[term]})

        return bigrams_dictionary, self.postings_lists
    
    def query(self, term1: str, term2: str = ''):
        #dictionary, postings_lists = self.index
        out_list = []

        #CASE 1: only one term
        if term2 == '':
            postID = self.bigrams_dictionary[term1][1]
            postings_list = self.getPostingList(postID)

            #retrive text
            with open(filename, 'r') as file:
                reader = csv.reader(file, delimiter = '\t')
            
                #iterate through each row of the table
                for row in reader:
                    (docID, url, pub_date, title, news_text) = row
                    if docID in postings_list:
                        out_list.append((docID, news_text))
        
        #CASE 2: two terms
        else: 
            intersection_list = []

            term1_postID = self.bigrams_dictionary[term1][1]
            term2_postID = self.bigrams_dictionary[term2][1]
            
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
            
                #iterate through each row of the table
                for row in reader:
                    (docID, url, pub_date, title, news_text) = row
                    if docID in intersection_list:
                        out_list.append((docID, news_text))
        return out_list

    def getWildcardTerms(self, term):
        out_list = []
        bigrams_term_wildcard = self.getTermBigrams(term)
        
        # wildcard on the right side
        if bigrams_term_wildcard[0][0] == '$':
            for bigrams_term_dictionary in self.bigrams_dictionary:
                
                # check if bigrams of the dictionary correspods with the wildcard
                if bigrams_term_dictionary[0:len(bigrams_term_wildcard)] == bigrams_term_wildcard:
                    out_list.append(bigrams_term_dictionary)
        
        #wildcard on the left side
        else:
            print(bigrams_term_wildcard[::-1])
            for bigrams_term_dictionary in self.bigrams_dictionary:
                
                # check if bigrams of the dictionary correspods with the wildcard
                # the bigrams tuple in this case is reversed
                bigrams_term_dictionary = bigrams_term_dictionary[::-1]
                if bigrams_term_dictionary[0:len(bigrams_term_wildcard)] == bigrams_term_wildcard[::-1]:
                    out_list.append(bigrams_term_dictionary[::-1])

        return out_list

    def queryWildcards(self, term1, term2):
        out_list = []
        bigrams_list_term1 = self.getWildcardTerms(term1)
        #print(bigrams_list_term1)
        bigrams_list_term2 = self.getWildcardTerms(term2)
        print(bigrams_list_term1)
        for bigrams_term1 in bigrams_list_term1:
            for bigrams_term2 in bigrams_list_term2:
                out_list.append(self.query(bigrams_term1, bigrams_term2))
        
        return out_list









if __name__ == "__main__":
    filename = 'assignment1/code/postillon.csv'
    index = index(filename=filename)
    search = Search(filename=filename, index=index)
    
    print( search.queryWildcards('wei*', 'maße') )
    print( search.queryWildcards('weiss', '*e') )
    
    



    """
    #queries
    print('weiß AND maß')
    for item in search.query('weiß', 'maß'):
        print(item)
    
    print('weiß AND masse')
    for item in search.query('weiß', 'masse'):
        print(item, '\n')
    
    print('weiss AND maße')
    for item in search.query('weiss', 'maße'):
        print(item, '\n')
    
    print('weiss AND masse')
    for item in search.query('weiss', 'masse'):
        print(item, '\n')
    """

