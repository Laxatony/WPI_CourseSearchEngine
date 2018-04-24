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
        self._myDB = WpiDynamoDBController()


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
        for course in courseDatabase:
            tokens = self._tokenizer.run(course.description)
            contents.append([course.cid,tokens])
        for content in contents:
            temp=[]
            for i in range(len(content[-1])-1):
                temp.append((content[-1][i],content[-1][i+1]))
            continuous1.append([content[0],temp])
        for i in contents:
            for word in i[-1]:
                word_library.add(word)

        #get self.tfidf
        self._tfidf=self.tf_idf(contents,word_library)
        temp=set()
        for i in continuous1:
            for j in i[-1]:
                temp.add(j)
        for i in temp:
            for j in continuous1:
                if i in j[-1]:
                    continuous[i].append(j[0])
        #get self._continuous
        self._continuous=continuous
        # get self._titledict
        titledict=defaultdict(list)
        for course in courseDatabase:
            tokens=self._tokenizer.run(course.title)
            for word in tokens:
                titledict[word].append(course.cid)
        for i in titledict:
            titledict[i]=list(set(titledict[i]))
        self._titledict=titledict

        return self._tfidf, self._continuous, self._titledict

    def _gettfidf(self,word):
        # given a word return a dict {doc1: tfidfscoer,doc2 :tfidfscore}
        return self._myDB.get_tfidf_by_word(word)

    def _gettitle(self,word):
        #given a word, return a list [doc1,doc2,doc3]
        # cids = self._myDB.get_idList_by_title_word(word)
        # print('by title')
        # print(cids)
        return self._myDB.get_idList_by_title_word(word)

    def _getcontinuous(self,word_comb):
        #given a word combination ('machine','learning')
        #return a list [doc1,doc2,doc3]
        # cids = self._myDB.get_idList_by_biwords(word_comb)
        # print('by biwords')
        # print(cids)
        return self._myDB.get_idList_by_biwords(word_comb)

    def _getcoursesbycids(self,cids):
        return self._myDB.get_courses_by_cids(cids)

    # Given a text and its related docIDs, return a ranked docID list
    # Input:
    #   a query text string
    #   a related doc list: [docID1, docID2, ...]
    # Return:
    #   ranked docID list:
    def getRankedList(self, text):
        query=self._tokenizer.run(text)
        if len(query)==1:
            #first_priority: if query is in the course title
            first_priority=[]
            first_priority.extend(self._gettitle(query[0]))
            # Sort by length for first priority
            tempSort = {}
            courses = self._getcoursesbycids(first_priority)
            for course in courses:
                title = course.title
                cid = course.cid
                tempSort[cid] = title
            first_priority = sorted(tempSort, key=lambda k: len(tempSort[k]), reverse=False)

            # third return top 5 tfidf score doc
            third_priority=[]
            arr=self._gettfidf(query[0])
            third_result=sorted(arr.items(), key=lambda item:item[1], reverse=True)[0:5]
            third=[i[0] for i in third_result]
            first_priority.extend(third)
            result=list(set(first_priority))
            result.sort(key=first_priority.index)
            return result
        else:
            # intersection between words in query's corresonding docs
            first_priority=[]
            for word in query:
                first_priority.append(self._gettitle(word))
            temp=set(first_priority[0])
            for i in first_priority[1:]:
                temp=temp.intersection(set(i))
            first_priority=list(temp)
            first_priority.sort()
            # print('first_priority')
            # print(first_priority)

            # Sort by length for first priority
            tempSort = {}
            courses = self._getcoursesbycids(first_priority)
            for course in courses:
                title = course.title
                cid = course.cid
                tempSort[cid] = title
            first_priority = sorted(tempSort, key=lambda k: len(tempSort[k]), reverse=False)
            # print(first_priority)
            

            # second_priority: if the consecutive query is in the course description
            second_priority=[]
            # temp_query=[('a', 'b'), ('b', 'c'), ('c', 'd')] while query=['a','b','c']
            temp_query=[(query[i],query[i+1]) for i in range(len(query)-1)]
            for i in temp_query:
                second_priority.append(self._getcontinuous(i))
            temp=set(second_priority[0])
            for i in second_priority[1:]:
                temp=temp.union(set(i))
            second_priority1=list(temp)
            # print('second_priority')
            # print(second_priority1)

            # super pripority , get intersection
            if len(query)>2:
                super=set(second_priority[0])
                for i in second_priority[1:]:
                    super=super.intersection(set(i))
                super = list(super)
                super.sort()
                if super:
                    for i in super[::-1]:
                        second_priority1.insert(0,i)

            # print('super')
            # print(first_priority)

            # temp: intersections
            temp=set(self._gettfidf(query[0]).keys())
            for word in query[1:]:
                temp=temp.intersection(set(self._gettfidf(word).keys()))
            temp=list(temp)
            # third_priority: return the highest 10 tf-idf
            third_priority=self._gettfidf(query[0])
            for word in query[1:]:
                temp_dict=self._gettfidf(word)
                for i in temp_dict:
                    if i in third_priority:
                        third_priority[i]+=temp_dict[i]
                    else:
                        third_priority[i]=temp_dict[i]
            # sort third_priority and return top10
            third_result=sorted(third_priority.items(), key=lambda item:item[1], reverse=True)[0:10]
            third=[i[0] for i in third_result]

            tempdict={}
            for i in temp:
                tempdict[i]=third_priority[i]
            temp1=sorted(tempdict.items(), key=lambda item:item[1], reverse=True)
            prethird=[i[0] for i in third_result]
            for i in prethird:
                third.remove(i)
            prethird.extend(third)


            # print('third_priority')
            # print(third)

            first_priority.extend(second_priority1)
            first_priority.extend(prethird)
            result=list(set(first_priority))
            result.sort(key=first_priority.index)
            return result


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
    course3.description = "DS502 is statistical learning.\n We will talk about methods for classification and clustering."
    course3.updateCID()
    courses.append(course3)

    return courses
# courseDatabase = getExampleDatabase()

# # Run TFIDF
# coursesTFIDF = TFIDF()
# query='machine learning'
# print("\nRanking of list given query")
# rankedList = coursesTFIDF.getRankedList(query)
