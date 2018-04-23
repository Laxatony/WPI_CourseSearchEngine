# stopwords download
# https://www.nltk.org/data.html
# 1. open python commend line
# 2.> import nltk
# 3.> nltk.download()
# 4. set correct directory for download accroding to the introduction website
# 5. choose "stopwords" in Corpora and download
# 6. choose "punkt" in Models and download


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import re

class Tokenizer:

    # Input: text string
    # Return: a list of tokens
    def run(self, text):

        # 1.remove stop word and turn into lower case
        stop = stopwords.words('english') + list(string.punctuation)
        tokens = [i for i in word_tokenize(text.lower()) if i not in stop]

        # 2.for tokens like "'s", maybe remove "'" -> maybe keep only a-zA-Z0-9
        tokens_ = []
        for i in tokens:
            # add stemming
            ps = PorterStemmer()
            i = ps.stem(i)
            tokens_.append(re.sub('\W', '', i))   #keep only a-zA-Z0-9
        tokens = tokens_

        # 3.remove empty elements
        tokens = list(filter(None, tokens))

        return tokens

# example ============================================
#example = "this's a a the FOo bar, shop, shopping, shops, bar black sheep."
#tokenizer = Tokenizer()
#tokens = tokenizer.run(example)
#print(tokens)
