import csv, re, nltk

class Search:

    def __init__(self, filename: str):
        self.filename = filename
        self.index = self.generate_index()

    
    def generate_index(self) ->tuple:
        """ 
        Generate the inverted index. 
        Dictionary and Postings List are implemented in separated datastructures.

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
    
 

    def query(self, term1: str, term2: str = ''):
        dictionary = self.index[0]
        out_list = []

        #CASE 1: only one term
        if term2 == '':
            post_id = dictionary[term1][1]
            postings_list = self.getPostingList(post_id)

            #retrive text
            with open(filename, 'r') as file:
                reader = csv.reader(file, delimiter = '\t')
            
                #iterate through each row of the table
                for row in reader:
                    #(doc_id, url, pub_date, title, news_text) = row
                    doc_id = row[0]
                    news_text = row[-1]
                    if doc_id in postings_list:
                        out_list.append((doc_id, news_text))
        
        #CASE 2: two terms
        else:    
            intersection_list = []

            term1_post_id = dictionary[term1][1]
            term2_post_id = dictionary[term2][1]
            
            term1_postings_list = self.getPostingList(term1_post_id)
            term2_postings_list = self.getPostingList(term2_post_id)
            
            #intersection algorithm
            for term1_doc_id in term1_postings_list:
                for term2_doc_id  in term2_postings_list:
                    if term1_doc_id  == term2_doc_id:
                        intersection_list.append(term1_doc_id)
            
            #retrive text
            with open(filename, 'r') as file:
                reader = csv.reader(file, delimiter = '\t')
            
                #iterate through each row of the table
                for row in reader:
                    #(doc_id, url, pub_date, title, news_text) = row
                    doc_id = row[0]
                    news_text = row[-1]
                    if doc_id in intersection_list:
                        out_list.append((doc_id, news_text))
        
        return out_list


if __name__ == "__main__":
    filename = 'assignment3/code/postillon.csv'
    search = Search(filename=filename)
    
    
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