import csv, re, nltk, math 
from collections import Counter
from operator import itemgetter

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
                # skip table header
                if( row[0] == 'id' ): continue

                #(doc_id, url, pub_date, title, news_text) = row
                doc_id = int(row[0])
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
    
    
    def getPostingList(self, postings_list_ID: int) -> list:
        """Will return a list with the postings given the postings list ID.

        Args:
            postings_listID (int): The ID of the postings list.

        Returns:
            list: return the list with the postings.
        """
        return self.postings_lists[postings_list_ID]
    

    def tf_matching_scores(self, query: str) ->dict:
        query = query.lower()
        query = query.split()
        
        docs_weights = {}
        tf_matching_scores = {}
        
        # retrive the news title and text to calculate tf-weights
        with open( self.filename, 'r' ) as file:
            reader = csv.reader(file, delimiter = '\t')
            
            #iterate through each row of the table
            for row in reader:
                # skip table header
                if( row[0] == 'id' ): continue
                
                #(doc_id, url, pub_date, title, news_text) = row
                doc_ID = int(row[0])
                news_title = row[-2]
                news_text = row[-1]

                docs_weights.update({doc_ID: []})

                tokenizer = nltk.RegexpTokenizer(r"\w+")
                normalized_news_title = tokenizer.tokenize(news_title.lower())
                normalized_news_text = tokenizer.tokenize(news_text.lower())

                news_terms = normalized_news_title + normalized_news_text
                
                for term in query:
                    
                    if( term in news_terms ):
                        log_tf = math.log(dict(Counter(news_terms))[term])
                        docs_weights[doc_ID].append(1 + log_tf)
                    else: 
                        docs_weights[doc_ID].append(0)
                
                # delete all documents that are not relevant to the query
                if( docs_weights[doc_ID] == [0,0] ):
                    docs_weights.pop(doc_ID)

                #calculate tf-matching-scores
                for doc_ID in docs_weights:
                    tf_matching_scores.update( {doc_ID: sum(docs_weights[doc_ID])} )
        
        return tf_matching_scores

    def rank(self, scores: dict):
        sorted_dict = sorted(scores.items(), key=itemgetter(1), reverse=True)
        ranked_list = []
        rank = 0
        old_score = 0
        
        for items in sorted_dict:
            doc_ID = items[0]
            score = items[-1]

            # don't rank if the score is zero
            if( score == 0 ): continue
            
            if( old_score == score):
                ranked_list.append((rank, doc_ID, score))
            else:
                rank += 1
                ranked_list.append((rank, doc_ID, score))
                old_score = score
        
        # print ranking table
        #print only top 10
        print("Rank \t", "Doc \t", "Score")
        print("-"*30)
        counter = 0
        for row in ranked_list:
            if ( counter > 9 ): break
            rank, doc_ID, score = row
            print(rank, "\t", doc_ID, "\t", round(score, 5))
            counter += 1
        


if __name__ == "__main__":
    filename = 'assignment3/code/postillon.csv'
    search = Search(filename=filename)
    
    print("\n"*3)
    print("1. Query: olympische sportbund")
    scores = search.tf_matching_scores("olympische sportbund")
    search.rank(scores)

    print("\n"*3)
    print("2. Query: rot wein")
    scores = search.tf_matching_scores("rot wein")
    search.rank(scores)

    print("\n"*3)
    print("3. Query: kinder sind faul")
    scores = search.tf_matching_scores("kinder sind faul")
    search.rank(scores)
    
    