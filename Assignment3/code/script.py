import csv, re, nltk
from collections import Counter

class Search:

    def __init__(self, filename: str):
        self.filename = filename
        self.index = self.generate_index()
        self.dictionary, self.postings_lists = self.index

    
    def generate_index(self) ->tuple:
        """ 
        Generate the inverted index. 
        Dictionary and Postings List are implemented in separated datastructures.

        The Dictionary take a term as a key and returns the size and ID of the postings list.

        Returns:
            tuple: Dictionary and Postings List
        """
        dictionary = {}
        postings_lists = []

        tokenizer = nltk.RegexpTokenizer(r"\w+")

        with open(self.filename, 'r') as file:
            reader = csv.reader(file, delimiter = '\t')
            postings = []
            
            #iterate through each row of the table
            for row in reader:
                #(doc_id, url, pub_date, title, news_text) = row
                doc_id = row[0]
                news_text = row[-1]

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
    
    
    def getPostingList(self, postings_list_id: int) -> list:
        """Will return a list with the postings given the postings list ID.

        Args:
            postings_listID (int): The ID of the postings list.

        Returns:
            list: return the list with the postings.
        """
        return self.index[-1][postings_list_id]
    
 

    def tf_matching_scores(self, sentence: str):
        dictionary, postings_lists = self.index
        query_postings_lists_IDs = []
        query_doc_IDs = set()
        
        # finds all relevant postings lists
        for term in sentence.split():
            postings_list_id = dictionary[term][-1]
            query_postings_lists_IDs.extend(self.getPostingList(postings_list_id))

        # finds all relevant documents
        for list_ID in query_postings_lists_IDs:
            list_ID = int(list_ID) #solve some issues
            postings_list = postings_lists[list_ID]
            query_doc_IDs.update(postings_list)
        
        # convert all IDs from strings in intagers
        query_doc_IDs = [int(doc_ID) for doc_ID in query_doc_IDs]
        
        sorted_query_doc_IDs = sorted(query_doc_IDs, reverse=True)

        # init the frequecy weights of the query's terms for each document
        documents_weights = {}
        for doc_ID in sorted_query_doc_IDs:
            documents_weights.update({doc_ID: []})

        # retrive the news title and text to calculate tf-weights
        with open(self.filename, 'r') as file:
            reader = csv.reader(file, delimiter = '\t')
            
            #iterate through each row of the table
            for row in reader:
                # skip table header
                if( row[0] == 'id' ): continue

                # if all documents were found 
                # we don't need to iterate anymore
                if not sorted_query_doc_IDs: break
                
                #(doc_id, url, pub_date, title, news_text) = row
                doc_ID = int(row[0])
                news_title = row[-2]
                news_text = row[-1]
                
                for term in sentence.split():
                    if("sportbund" in news_text): print(term, "FOUND!")
                
                """
                query_doc_ID = sorted_query_doc_IDs[-1]
                #print(query_doc_ID)

                # calculate tf-weights in the relevant documents
                if( doc_ID == query_doc_ID ):
                
                    tokenizer = nltk.RegexpTokenizer(r"\w+")
                    normalized_news_title = tokenizer.tokenize(news_title.lower())
                    normalized_news_text = tokenizer.tokenize(news_text.lower())

                    news_terms = normalized_news_title + normalized_news_text
                    
                    tf_news = dict(Counter(news_terms))
                    
                    for term in sentence.split():
                        #print(tf_news.keys())
                        for key in tf_news:
                            print(key)

                        
                        if term in tf_news:
                            
                            documents_weights[doc_ID].append(tf_news[term])
                        else: 
                            documents_weights[doc_ID].append(0)
                    
                    

                    sorted_query_doc_IDs = sorted_query_doc_IDs[:-1]
                    """  


        
        #return documents_weights
        pass




if __name__ == "__main__":
    filename = 'assignment3/code/postillon.csv'
    search = Search(filename=filename)

    print(search.tf_matching_scores("olympische sportbund"))
    
    