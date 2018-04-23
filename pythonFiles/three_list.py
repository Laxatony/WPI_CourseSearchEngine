from wpiTokenizer import Tokenizer
from courseInfo import CourseInfo
import math
from collections import defaultdict
from collections import Counter
from WpiDynamoDBController import WpiDynamoDBController
class TFIDF:

    def __init__(self):
        self._tokenizer = Tokenizer()
        self._tfidf = None
        self._continuous= None
        self._titledict=None


    def tf_idf(self,contents,word_library):
        dict1=defaultdict(int)
        idflist=[]
        idfdict={}
        for i in word_library:
            idfdict[i]={}
            for j in contents:
                if i in j[-1]:
                    dict1[i]+=1
        # dict1, the frequency of each word in the whole collection
        # transfer it to idf
        for i in dict1:
            dict1[i]=math.log10(len(contents)/dict1[i])

        for content in contents:
            temp2=dict(Counter(content[-1]))
            #temp2: tf
            for i in temp2:
                temp2[i]=(temp2[i]/len(temp2))*dict1[i]
            idflist.append([content[0],temp2])
        for word in word_library:
            for doc in idflist:
                if word in doc[-1]:
                    idfdict[word][doc[0]]=doc[-1][word]
        return idfdict


    def run(self, courseDatabase):
        word_library=set()
        contents=[]
        continuous=defaultdict(list)
        continuous1=[]
        #word_library ={all words in all courses' description}
        #contents=[[course1,tokens1],[course2,tokens2]]
        #continuous1=[[course1,[(a,b),(b,c),(c,d)]],[course2,[(a,b),(b,c)]]]
        print("step0")
        for course in courseDatabase:
            tokens = self._tokenizer.run(course.description)
            contents.append([course.cid,tokens])
        print("step1")
        for content in contents:
            temp=[]
            for i in range(len(content[-1])-1):
                temp.append((content[-1][i],content[-1][i+1]))
            continuous1.append([content[0],temp])
        print("step2")
        for i in contents:
            for word in i[-1]:
                word_library.add(word)
        print("step3")
        #get self.tfidf
        self._tfidf=self.tf_idf(contents,word_library)

        print("step4")
        temp=set()
        for i in continuous1:
            for j in i[-1]:
                temp.add(j)
        print("step5")
        print('length: ', len(temp), ' ', len(continuous1))
        for i in temp:
            for j in continuous1:
                if i in j[-1]:
                    continuous[i].append(j[0])
        #get self._continuous
        self._continuous=continuous

        print("step6")
        # get self._titledict
        titledict=defaultdict(list)
        for course in courseDatabase:
            tokens=self._tokenizer.run(course.title)
            for word in tokens:
                titledict[word].append(course.cid)
        print("step7")
        for i in titledict:
            titledict[i]=list(set(titledict[i]))
        self._titledict=titledict

        return self._tfidf, self._continuous, self._titledict

# ======================== example ========================
# Create Testing Database
def getExampleDatabase():
    courses = []

    course1 = CourseInfo()
    course1.term = 'Spring 2019'
    course1.reference = '20016'
    course1.description = "Big Data Management is one of the hottest courses in WPI.\nEvery one should take this course instead of Machine Learning."
    course1.updateCID()
    courses.append(course1)

    course2 = CourseInfo()
    course2.term = 'Fall 2019'
    course2.reference = '10143'
    course2.description = "Deep Learning is more interesting than Machine Learning.\n It's not pure classification.\n Artificial Intelligence is a wild concept tought by Pro. Gini."
    course2.updateCID()
    courses.append(course2)

    course3 = CourseInfo()
    course3.term = 'Spring 2018'
    course3.reference = '10110'
    course3.description = "Data Science(DS)502 is teaching statistical learning.\n We will talk about methods for classification and clustering."
    course3.updateCID()
    courses.append(course3)

    return courses
# courseDatabase = getExampleDatabase()

# myDB = WpiDynamoDBController()
# courseDatabase = myDB.get_courses_all()

# T=TFIDF()
# tfidf, biword, title = T.run(courseDatabase)

# print("done generate data")
# myDB.insert_Table_DescriptionTFIDF(tfidf)
# print("done tfidf insert")
# myDB.insert_Table_BiwordInvertedIndex(biword)
# print("done biword")
# myDB.insert_Table_TitleInvertedIndex(title)
# print("done title")
