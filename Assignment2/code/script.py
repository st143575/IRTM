import csv, re, nltk

class Search:

    def __init__(self, filename: str):
        self.filename = filename
        self.index = self.getIndex()
        self.dictionary, self.postings_lists = self.getIndex()
        self.bigrams_index = self.getBigramIndex()
        self.bigrams_dictionary, self.bigrams_postings_lists = self.bigrams_index

    def getIndex(self):
        dictionary = {}
        postings_lists = []

        tokenizer = nltk.RegexpTokenizer(r"\w+")

        with open(self.filename, 'r') as file:
            reader = csv.reader(file, delimiter = '\t')
            postings = []
            
            #iterate through each row of the table
            for row in reader:
                #(doc_id, url, pub_date, title, news_text) = row
                docID = row[0]
                news_text = row[-1]

                #tokenize and normalize news text
                #this procedure will remove symbols like !?() etc.
                #the set data structure will remove all duplicates
                news_text_norm = set(tokenizer.tokenize(news_text.lower()))

                #generate postings
                #iterate through each term
                for term in news_text_norm:
                    postings.append((term, docID))
                
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


    def getPostingList(self, postings_listID: int) -> list:
        """Will return a list with the postings given the postings list ID.

        Args:
            postings_listID (int): The ID of the postings list.

        Returns:
            list: return the list with the postings.
        """
        return self.postings_lists[postings_listID]
    
    def query(self, term1: str, term2: str = '') -> list:
        """Search if one or two terms are contained in the same document.
        Then returns the document ID and the news text.

        Args:
            term1 (str): A term
            term2 (str, optional): A term or nothings. Defaults to ''.

        Returns:
            list: A list of results
        """

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
                    docID = row[0]
                    news_text = row[-1]

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
                    #(docID, url, pub_date, title, news_text) = row
                    docID = row[0]
                    news_text = row[-1]
                    
                    if docID in intersection_list:
                        out_list.append((docID, news_text))
                        #out_list.append((news_text))
        
        return out_list
   
    def getTermBigrams(self, term: str):
        """Returns the bigrams of a given term. 

        Args:
            term (str): A term.

        Returns:
            tuple: The bigrams of a term.
        """
        
        # solve some issues
        if not term:
            tuple_bigrams = ()
        
        # bigrams for wildcards on the left side
        elif term[0] == '*':
            tuple_bigrams = tuple(list(nltk.bigrams(term)) + [(term[-1], '$')])[1:]
        
        # bigrams for wildcards on the right side
        elif term[-1] == '*':
            tuple_bigrams = tuple([('$', term[0])] + list(nltk.bigrams(term)))[:-1]
        
        # bigrams
        else:
            tuple_bigrams = tuple([('$', term[0])] + list(nltk.bigrams(term)) + [(term[-1], '$')])
        
        bigrams = []
        for bigram in tuple_bigrams:
                #join the bigram tuple into one string
                bigrams.append((''.join([char for char in bigram])).strip())

        return tuple(bigrams)
    
    def getBigramIndex(self):
        """Generate a Bigram Index from an other Index"""

        #generate a new dictionary witch contains 
        #bigrams of the terms as the key
        bigrams_dictionary = {}
        for term in self.dictionary:
            bigrams_dictionary.update({self.getTermBigrams(term): self.dictionary[term]})

        return bigrams_dictionary, self.postings_lists

    def getWildcardTerms(self, term: str) -> list:
        """Retuns a list of terms for a given term with a wildcard.
        The terms will be returned in the form of bigrams.

        Args:
            term (str): A term or a part of it.

        Returns:
            [list]: A list of term's bigrams
        """
        out_list = []
        bigrams_term_wildcard = self.getTermBigrams(term)
        
        if '*' not in term:
            out_list.append(bigrams_term_wildcard)

        # wildcard on the right side
        elif term[0] == '$' and term[-1] != '$':
            for bigrams_term_dictionary in self.bigrams_dictionary:
                
                if bigrams_term_dictionary[0:len(bigrams_term_wildcard)] == bigrams_term_wildcard:
                    out_list.append(bigrams_term_dictionary)
        
        #wildcard on the left side
        elif term[0] != '$' and term[-1] == '$':
        
            for bigrams_term_dictionary in self.bigrams_dictionary:
                if bigrams_term_dictionary[::-1][0:len(bigrams_term_wildcard)] == bigrams_term_wildcard[::-1]:
                    out_list.append(bigrams_term_dictionary)
        
        # wildcard in the of the term or no wildcard
        else:
            term_splits = term.split('*')
            term_split_1 = self.getTermBigrams(term_splits[0])[:-1]
            term_split_2 = self.getTermBigrams(term_splits[1])[1:]

            for bigrams_term_dictionary in self.bigrams_dictionary: 
                if bigrams_term_dictionary[:len(term_split_1)] == term_split_1:
                    if bigrams_term_dictionary[::-1][:len(term_split_2)] == term_split_2[::-1]:
                        out_list.append(bigrams_term_dictionary)

        return out_list

    def queryWildcards(self, term1: str, term2: str) -> list:
        """Returns the resoult of a query with wildcards implementation.
        A query for every term in the list of terms found for a given wildcard.

        Args:
            term1 (str): A term.
            term2 (str): A term.

        Returns:
            list: A list with the results of all the queries.
        """
        out_list = []
        bigrams_list_term1 = self.getWildcardTerms(term1)
        bigrams_list_term2 = self.getWildcardTerms(term2)
        
        for bigrams_term1 in bigrams_list_term1:
            for bigrams_term2 in bigrams_list_term2:
                out_list.append(self.query(bigrams_term1, bigrams_term2))
        
        return out_list




if __name__ == "__main__":
    filename = 'assignment1/code/postillon.csv'
    search = Search(filename=filename)
    
    #print(search.query(search.getTermBigrams('weiß'), search.getTermBigrams('maße')))
    #print(search.query(search.getTermBigrams('weiss'), search.getTermBigrams('maße')))
    #print(search.query(search.getTermBigrams('weiß'), search.getTermBigrams('masse')))
    #print(search.query(search.getTermBigrams('weiss'), search.getTermBigrams('masse')))

    #wildcards
    #print(search.queryWildcards('weiß', 'maße'))
    #print(search.queryWildcards('weiss', '*aße'))
    print(search.queryWildcards('wei*', '*asse'))
    #print(search.queryWildcards('wei*s', 'm*sse'))

