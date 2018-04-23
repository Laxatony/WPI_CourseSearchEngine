# Tutorial
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html

# [Error Fix]
# create table: WriteCapacityUnits error, OSError: [Errno 22] Invalid argument
#     solution: MODIFY _naive_is_dst(self, dt) function in the local site-packages\dateutil\tz\tz.py file.
# https://stackoverflow.com/questions/38918668/dynamodb-create-table-calls-fails 

from __future__ import print_function # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from courseInfo import CourseInfo


import json, decimal
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class WpiDynamoDBController:

    def __init__(self):
        self.__TabelName_Courses__ = 'Courses'
        self.__TabelName_Description_Word_TFIDF__ = 'DescriptionTFIDF'
        self.__TabelName_Title_Word_InvertedIndex__ = 'TitleInvertedIndex'
        self.__TabelName_BiWord_InvertedIndex__ = 'BiwordInvertedIndex'

        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    def _create_table_Courses_(self):
        tableName = self.__TabelName_Courses__

        if self.is_table_exist(tableName):
            print(tableName + " already exist.")
            return

        table = self.dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'cid', # "term + ' ' + subject + ' ' + course_index + ' ' + reference"
                    'KeyType': 'HASH'  #Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'cid',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            })
        print("Table status:", table.table_status)

    # {   
    #   term: 'word',
    #   data: {'cid1': tf-idf score, 'cid2': ti-idf score, ...}
    # }
    def _create_table_Description_Word_TFIDF_(self):
        tableName = self.__TabelName_Description_Word_TFIDF__
        
        if self.is_table_exist(tableName):
            print(tableName + " already exist.")
            return

        table = self.dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'term',
                    'KeyType': 'HASH'   #Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'term',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            })
        print("Table status:", table.table_status)

    # {
    #   term: 'word',
    #   data: ['cid3', 'cid1, 'cid4', ...]
    # }
    def _create_table_Title_Word_InverteIndex_(self):
        tableName = self.__TabelName_Title_Word_InvertedIndex__

        if self.is_table_exist(tableName):
            print(tableName + " already exist.")
            return

        table = self.dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'term',
                    'KeyType': 'HASH'   #Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'term',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            })
        print("Table status:", table.table_status)

    # {
    #   term: 'word',
    #   data: ['cid3', 'cid1, 'cid4', ...]
    # }
    def _create_table_BiWord_Word_InverteIndex_(self):
        tableName = self.__TabelName_BiWord_InvertedIndex__

        if self.is_table_exist(tableName):
            print(tableName + " already exist.")
            return

        table = self.dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'term',
                    'KeyType': 'HASH'   #Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'term',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            })
        print("Table status:", table.table_status)
    
    def _delete_table_(self, tabelName):
        if self.is_table_exist(tabelName):
            table = self.dynamodb.Table(tabelName)
            table.delete()
        else:
            print(tabelName + " is not exist.")

    def get_table_list(self):
        tables = []
        for table in self.dynamodb.tables.all():
            tables.append(table.table_name)
        return tables

    def is_table_exist(self, tabelName):
        tables = self.get_table_list()
        return (tabelName in tables)

    ##################################################################
    ##################################################################

    # ================================================================
    # ==================== Database: Courses =========================
    # ================================================================
    def insert_course_item(self, course):
        # DynamoDB will replace data when data already exist
        # Currently, we block this automation manually
        item = course.generateJSONObj()
        tableName = self.__TabelName_Courses__

        if not self.is_table_exist(tableName):
            return
        if self.is_course_item_exist(course.cid):
            return

        table = self.dynamodb.Table(tableName)
        try:
            response = table.put_item(
                Item = item
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False
        else:
            print("PutItem succeeded:")
            return True
            # print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def get_CIDs_by_partialInfo(self, term, subject, course_index):
        result = []
        tableName = "Courses"
        if not self.is_table_exist(tableName):
            print("Table:" + tableName +  " doesn't exist")
            return

        pe = "#cid"
        ea = {"#cid": "cid"}
        fe = Attr('term').eq(term) & Attr('subject').begins_with(subject) & Attr('course_index').begins_with(course_index)

        table = self.dynamodb.Table(tableName)
        try:
            response = table.scan(
                ProjectionExpression = pe,
                ExpressionAttributeNames = ea,
                FilterExpression = fe)

            for item in response['Items']:
                result.append(item['cid'])

            while 'LastEvaluatedKey' in response:
                response = table.scan(
                    ProjectionExpression = pe,
                    ExpressionAttributeNames = ea,
                    FilterExpression = fe,
                    ExclusiveStartKey = response['LastEvaluatedKey']
                )

                for item in response['Items']:
                    result.append(item['cid'])       
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            # print("ScanItem succeeded:")
            # print(json.dumps(response, indent=4, cls=DecimalEncoder))
            return result

    def update_courses_description(self, cids, description):
        tableName = "Courses"
        if not self.is_table_exist(tableName):
            print("Table:" + tableName +  " doesn't exist")
            return

        table = self.dynamodb.Table(tableName)
        for cid in cids:
            try:
                response = table.update_item(
                    Key={
                        'cid': cid,
                    },
                    UpdateExpression="set description = :description",
                    ExpressionAttributeValues={
                        ':description': description,
                    },
                    ReturnValues="UPDATED_NEW")
            
            except ClientError as e:
                if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                    print(e.response['Error']['Message'])
                else:
                    raise
            else:
                response = 'success'
                print(cid, "UpdateItem succeeded:")
                # print(json.dumps(response, indent=4, cls=DecimalEncoder))
            
    def get_courses_all(self):
        courses = []

        tableName = self.__TabelName_Courses__
        table = self.dynamodb.Table(tableName)
        
        response = table.scan()
        for item in response['Items']:
            # print(json.dumps(item, cls=DecimalEncoder))
            course = CourseInfo()
            course.generateFromJSONObj(item)
            courses.append(course)

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            for item in response['Items']:
                course = CourseInfo()
                course.generateFromJSONObj(item)
                courses.append(course)

        return courses
    
    def get_courses_by_cids(self, cids):
        courses = []

        tableName = self.__TabelName_Courses__
        table = self.dynamodb.Table(tableName)
        
        for cid in cids:
            response = table.query(KeyConditionExpression=Key('cid').eq(cid))
            for item in response['Items']:
                course = CourseInfo()
                course.generateFromJSONObj(item)
                courses.append(course)

            while 'LastEvaluatedKey' in response:
                response = table.query(KeyConditionExpression=Key('cid').eq(cid), ExclusiveStartKey=response['LastEvaluatedKey'])
                for item in response['Items']:
                    course = CourseInfo()
                    course.generateFromJSONObj(item)
                    courses.append(course)

        return courses

    def is_course_item_exist(self, cid):
        tableName = self.__TabelName_Courses__
        table = self.dynamodb.Table(tableName)

        try:
            response = table.get_item(
                Key={
                    'cid': cid,
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            return False
        else:
            if "Item" in response :
                print("Item Exist: " + cid)
                # item = response['Item']
                # print(json.dumps(item, indent=4, cls=DecimalEncoder))
                return True
            else:
                return False
    
    # ================================================================
    # ================ Database: DescriptionTFIDF ====================
    # ================================================================
    # dicts = 
    # {
    #   'word1' : {'doc1': tf-idf score, 'doc2': tf-idf, ...},
    #   'word2' : {'doc1': tf-idf score, 'doc2': tf-idf, ...},
    #   ...
    # }
    def insert_Table_DescriptionTFIDF(self, dicts):
        # DynamoDB will replace data when data already exist
        # Currently, we block this automation manually

        tableName = self.__TabelName_Description_Word_TFIDF__

        if not self.is_table_exist(tableName):
            return

        table = self.dynamodb.Table(tableName)

        with table.batch_writer() as batch:
            print('items: ', len(dicts))
            count = 0
            for term, tfidfs in dicts.items():
                try:
                    item = {}
                    item['term'] = term
                    # float to decimal # DynamoDB accept only decimal
                    for doc, score in tfidfs.items():
                        tfidfs[doc] = decimal.Decimal(str(score))
                    item['tfidfs'] = tfidfs
                    

                    response = batch.put_item(
                        Item = item
                    )
                except ClientError as e:
                    print(e.response['Error']['Message'])
                    print('error')
                    print(term, '------', tfidfs)
                    for doc, score in tfidfs.items():
                        tfidfs[doc] = decimal.Decimal(str(score))
                    print(term, '------', tfidfs)
                    return False
                else:
                    if count == 500:
                        print("PutItem succeeded: " + str(count))
                        count = 0
                    else:
                        count += 1
        print("insert Table(DescriptionTFIDF) Done...")


    # @Func:     Given a word, return corresponding TF-iDF scores in all courses
    # @Database: DB(DescriptionTFIDF)
    # @input:    word              (ex:) 'machine'
    # @output:   dict{'cid':score} (ex:) {'docID1': 0.12, 'docID3':0.44, 'docID2':0.31, ...}
    def get_tfidf_by_word(self, term):
        result = {}

        tableName = self.__TabelName_Description_Word_TFIDF__
        table = self.dynamodb.Table(tableName)
        
        response = table.query(KeyConditionExpression=Key('term').eq(term))
        for item in response['Items']:
            # print(json.dumps(item, cls=DecimalEncoder))

            result = item['tfidfs']
            # decimal to float # Transform back to its original data type
            for doc, score in result.items():
                    result[doc] = float(score)

        while 'LastEvaluatedKey' in response:
            response = table.query(KeyConditionExpression=Key('word').eq(word), ExclusiveStartKey=response['LastEvaluatedKey'])
            for item in response['Items']:
                # print(json.dumps(item, cls=DecimalEncoder))
                result = item['tfidfs']

        return result


    # ================================================================
    # ================ Database: TitleInvertedIndex ==================
    # ================================================================
    # items = 
    # {
    #   'word1' : ['doc1', 'doc2', 'doc3', ...],
    #   'word2' : ['doc1', 'doc3', 'doc4', ...],
    #   ...
    # }
    def insert_Table_TitleInvertedIndex(self, dicts):
        tableName = self.__TabelName_Title_Word_InvertedIndex__

        if not self.is_table_exist(tableName):
            return

        table = self.dynamodb.Table(tableName)
        
        with table.batch_writer() as batch:

            print('items: ', len(dicts))
            count = 0
            for term, docs in dicts.items():
                try:
                    item = {}
                    item['term'] = term
                    item['docs'] = docs

                    response = batch.put_item(
                        Item = item
                    )
                except ClientError as e:
                    print(e.response['Error']['Message'])
                    print(term, '------', docs)
                else:
                    if count == 500:
                        print("PutItem succeeded: " + str(count))
                        count = 0
                    else:
                        count += 1
        print("insert Table(TitleInvertedIndex) Done...")
    
    # @Func:    Given a word, retrieve corresponding document ids that containing the word in Title Database
    # @Database: DB(TitleInvertedIndex)
    # @input:   word            (ex:) 'machine'
    # @output:  array['cid']    (ex:) ['docID1', 'docID2', 'docID3']
    def get_idList_by_title_word(self, term):
        result = []

        tableName = self.__TabelName_Title_Word_InvertedIndex__
        table = self.dynamodb.Table(tableName)
        
        response = table.query(KeyConditionExpression=Key('term').eq(term))
        for item in response['Items']:
            # print(json.dumps(item, cls=DecimalEncoder))
            result = item['docs']

        while 'LastEvaluatedKey' in response:
            response = table.query(KeyConditionExpression=Key('word').eq(term), ExclusiveStartKey=response['LastEvaluatedKey'])
            for item in response['Items']:
                result = item['docs']

        return result

    
    # ================================================================
    # ================ Database: BiwordInvertedIndex =================
    # ================================================================
    # items = 
    # {
    #   'word1' : ['doc1', 'doc2', 'doc3', ...],
    #   'word2' : ['doc1', 'doc3', 'doc4', ...],
    #   ...
    # }
    def insert_Table_BiwordInvertedIndex(self, dicts):
        tableName = self.__TabelName_BiWord_InvertedIndex__

        if not self.is_table_exist(tableName):
            return

        table = self.dynamodb.Table(tableName)

        with table.batch_writer() as batch:
            print('items: ', len(dicts))
            count = 0
            for biWord, docs in dicts.items():
                try:
                    term = ''
                    for index, word in enumerate(biWord):
                        if index == 0:
                            term += word
                        else:
                            term += ' ' + word
                    # biword = ('A','B') ---> term = 'A B'
                    item = {}
                    item['term'] = term
                    item['docs'] = docs

                    response = table.put_item(
                        Item = item
                    )
                except ClientError as e:
                    print(e.response['Error']['Message'])
                    print(biWord, '------', docs)
                    return False
                else:
                    if count == 500:
                        print("PutItem succeeded: " + str(count))
                        count = 0
                    else:
                        count += 1
        print("insert Table(BiwordInvertedIndex) Done...")
    
    # @Func:    Given 2 words, retrieve corresponding document ids that containing the word in Bi-word Database
    # @Database: DB(BiwordInvertedIndex)
    # @input:   wordA, wordB    (ex:) 'machine', 'learning'
    # @output:  array['cid']    (ex:) ['docID1', 'docID2', 'docID3']
    def get_idList_by_biwords(self, biWord):

        term = ''
        for index, word in enumerate(biWord):
            if index == 0:
                term += word
            else:
                term += ' ' + word
        # biword = ('A','B') ---> term = 'A B'
        result = []

        tableName = self.__TabelName_BiWord_InvertedIndex__
        table = self.dynamodb.Table(tableName)
        
        response = table.query(KeyConditionExpression=Key('term').eq(term))
        for item in response['Items']:
            # print(json.dumps(item, cls=DecimalEncoder))
            result = item['docs']

        while 'LastEvaluatedKey' in response:
            response = table.query(KeyConditionExpression=Key('term').eq(term), ExclusiveStartKey=response['LastEvaluatedKey'])
            for item in response['Items']:
                result = item['docs']

        return result


# myDB = WpiDynamoDBController()
# courseDatabase = myDB.get_courses_all()
# count = 1
# for course in courseDatabase:
#     print(str(count), course.cid)
#     print(course.description + '\n')
#     count += 1

# myDB._delete_table_('Courses')
# myDB._create_table_Courses_()

# myDB._delete_table_('DescriptionTFIDF')
# myDB._create_table_Description_Word_TFIDF_()

# myDB._delete_table_('TitleInvertedIndex')
# myDB._create_table_Title_Word_InverteIndex_()

# myDB._delete_table_('BiwordInvertedIndex')
# myDB._create_table_BiWord_Word_InverteIndex_()