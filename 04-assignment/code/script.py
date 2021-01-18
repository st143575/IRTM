import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from operator import itemgetter

class SVM_Classifier:
    path = "04-assignment/code/"

    def __init__(self):
        self.train_data = self.load_data("games-train.csv")
        self.term_weights_dictionary = self.calc_term_weights_dictionary()
    
    
    
    def load_data(self, filename: str) ->pd.DataFrame:
        
        # import data
        dataframe = pd.read_csv(self.path + filename, sep="\t", header=None)

        # stops that will remain in the corpus
        relevant_stops = set(['nicht', 'nichts', 'kein','kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines'])
        
        # stops to remove
        stops = set(stopwords.words('german')) - relevant_stops 
        


        # process data to create corpus
        label_col, text_col = (dataframe[1].tolist(), dataframe[3].tolist())
        binary_label_col, normalized_text_col = ([], [])
        
        for index in range(len(label_col)-1):
            
            label, text = (label_col[index], text_col[index])
            
            # covert the labels into binary values 
            # 'gut' = 1, 'schlecht' = -1
            if label == 'gut': 
                binary_label_col.append(1)
            else: 
                binary_label_col.append(-1)


            # text normalization
            normalized_text = word_tokenize(str(text).lower())

            # remove stops
            for token in normalized_text:
                if token in stops: normalized_text.remove(token)

            normalized_text_col.append(word_tokenize(str(text).lower()))
            

        # create the corpus's data-structure
        corpus = {'label': binary_label_col , 'text': normalized_text_col}
        
        return pd.DataFrame(corpus)
    

    def calc_term_weights_dictionary(self) ->dict:
        term_weights_dict = {}

        for row in self.train_data.iterrows():
            label, text = row[-1]

            term_freq_dict = Counter(text)

            for term in term_freq_dict:

                if term not in term_weights_dict:
                    term_weights_dict.update({ term: label * term_freq_dict[term] })
                else:
                    # sum the term fequencies
                    # if the class is 'schlecht' the term's frequency will be negative
                    term_weights_dict[term] += label * term_freq_dict[term]
        
        return term_weights_dict
    

    




if __name__ == "__main__":
    classifier = SVM_Classifier()
    train_data = classifier.train_data
    dictionary = classifier.term_weights_dictionary
    
    
    sorted_term_weight_list = sorted(dictionary.items(), key=itemgetter(1))
    
    print(" -"*50, "\n Top 100 result for class 'gut': \n", "-"*50)
    for term, weight in sorted_term_weight_list[::-1][:100]:
        print(" ", weight, "\t", term)
    
    print("\n"*3)

    print(" -"*50, "\n Top 100 result for class 'schlecht': \n", "-"*50)
    for term, weight in sorted_term_weight_list[:100]:
        print(" ", weight, "\t", term)
  

    
   
