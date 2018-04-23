import sys, json, numpy as np
from courseInfo import CourseInfo
from courseTFIDF import TFIDF
from WpiDynamoDBController import WpiDynamoDBController

def main():

    data = json.loads(sys.argv[1]) # string to json
    # data = {'func': 'search_courses', 'query': 'machine'}

    # with open('tmp_data.txt', 'w') as outfile:
    #     # json.dump(data, outfile)
    # outfile.close()
    
    result = [] 
    if data['func'] == 'search_courses':
        query = data['query']
        
        courseCIDs = []
        mySearch = TFIDF()
        courseCIDs = mySearch.getRankedList(query)
        # print('cids')
        # print(courseCIDs)

        myDB = WpiDynamoDBController()

        if courseCIDs:
            courses = myDB.get_courses_by_cids(courseCIDs)
        # else:
            # courseCIDs = myDB.get_CIDs_by_partialInfo('Spring 2019', 'DATA SCIENCE', '501')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'DATA SCIENCE', '598')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'DATA SCIENCE', '541')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'DATA SCIENCE', '502')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'CHEMISTRY', '1010')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'CHEMISTRY', '1020')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'CHEMISTRY', '1030')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'CHEMISTRY', '1040')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'COMPUTER SCIENCE', '568')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'COMPUTER SCIENCE', '573')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'COMPUTER SCIENCE', '541')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'COMPUTER SCIENCE', '539')
            # courseCIDs += myDB.get_CIDs_by_partialInfo('Spring 2019', 'COMPUTER SCIENCE', '586')
            # courses = myDB.get_courses_by_cids(courseCIDs)

        for course in courses:
            result.append(course.generateJSONObj())

    else:
        result = []

    jsonFormat = json.dumps(result) # json to string
    print(jsonFormat)

#start process
if __name__ == '__main__':
    main()

    # myDB = WpiDynamoDBController()
   
    # # TEST UPDATE DESCRIPTION
    # cids = myDB.get_CIDs_by_partialInfo('Spring 2019', 'AEROSPACE ENGINEERING', '5104')
    # myDB.update_courses_description(cids, 'qqwqwqw')

    # # TEST GET ALL COURSES
    # courses = myDB.get_courses_all()
    # for course in courses:
    #     if course.term == 'Summer 2018' and course.subject == 'DATA SCIENCE':
    #         print(course.cid)
    #         print(course.description)

    #     if course.term == 'Summer 2018' and course.subject == 'SYSTEMS ENGINEERING':
    #         print(course.cid)
    #         print(course.description)

    # # TEST GET COURSES by cids
    # cids = []
    # cids.append('Summer 2018 SYSTEMS ENGINEERING 501 31462')
    # cids.append('Summer 2018 DATA SCIENCE 501 31387')
    # courses = myDB.get_courses_by_cids(cids)
    # for course in courses:
    #     print(course.cid)
    #     print(course.description)

    # # TEST INSERT AND RETRIEVE TFIDF
    # description_tfidfs = {}
    # description_tfidfs['apple'] = {'dcoID1': 0.11, 'dcoID2': 0.12, 'dcoID3': 0.13, 'dcoID4': 0.14}
    # description_tfidfs['banana'] = {'dcoID2': 0.21, 'dcoID3': 0.22}
    # description_tfidfs['candy'] = {'dcoID4': 0.31, 'dcoID5': 0.32}
    # description_tfidfs['django'] = {'dcoID5': 0.41, 'dcoID1': 0.42, 'dcoID3': 0.43}
    # # myDB.insert_Table_DescriptionTFIDF(description_tfidfs)

    # results = myDB.get_tfidf_by_word('apple')
    # for doc, score in results.items():
    #     print(doc, score)

    # TEST INSERT AND RETRIEVE TITLE
    # title = {}
    # title['Machine'] = ['dcoID1', 'dcoID2', 'dcoID3', 'dcoID4']
    # title['Learning'] = ['dcoID2', 'dcoID3']
    # title['Deep'] = ['dcoID4', 'dcoID5']
    # title['Method'] = ['dcoID5', 'dcoID1', 'dcoID3']
    # myDB.insert_Table_TitleInvertedIndex(title)

    # results = myDB.get_idList_by_title_word('Deep')
    # for doc in results:
    #     print(doc)

    # # TEST INSERT AND RETRIEVE BI-WORD
    # biWord = {}
    # biWord['Machine Learning'] = ['dcoID1', 'dcoID2', 'dcoID3', 'dcoID4']
    # biWord['Learning Method'] = ['dcoID2', 'dcoID3']
    # biWord['Deep Learning'] = ['dcoID4', 'dcoID5']
    # biWord['Statistical Method'] = ['dcoID5', 'dcoID1', 'dcoID3']
    # myDB.insert_Table_BiwordInvertedIndex(biWord)

    # results = myDB.get_idList_by_biwords('Deep', 'Learning')
    # for doc in results:
    #     print(doc)  