# Courses Finder

## Author
* Yaochun Hsieh (Data Science) &nbsp;&nbsp;yhsieh2@wpi.edu
* Yang Tao (Data Science)     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ytao2@wpi.edu
* Haowen Zhu (Data Science)   &nbsp;&nbsp;&nbsp;&nbsp; hzhu3@wpi.edu

## Motivation
We want to build a WPI course search engine for students to search for their desired courses by simply typing in the key-word about the course. For example, if some students want to study the topic about ‘machine learning’, the search engine should return courses related to ‘machine learning’, like ‘Introduction of Machine Learning’, ’Artificial Intelligence’, which contain knowledge about ‘machine learning’.

Basically, most universities have their own course registration system, some of them are pretty advanced and could support such function. However, in the WPI course registration system, students could only search course by the semester, major, then scan the whole list of courses for that specific major to find their desired courses. It is inefficient and some students might miss their target courses since they could not read all course description across different majors. Therefore, we want to optimize the search function of the course registration system by returning.

## Dataset
All the WPI courses in Summer 2018, Fall 2018 and Spring 2019. There are totally 2663 courses.
The basic information including term, subject, CRN, title, insturctor, remaining seats and course description is stored for each course.

## Environment and Needed Installation / Packages
1. Javascript and NodeJS Related:
    - WebSocket: *message exchange between client and server*
    - [PythonShell](https://www.npmjs.com/package/python-shell):  *message exchange between server and python file*
2. Python Related:
    - automatic course web crawler
      * [Selenium](http://selenium-python.readthedocs.io/): 
      * a brawser driver execution (ex: cromedriver.exe)
    - access AWS Dynamo database
      * [boto3](https://boto3.readthedocs.io/en/latest/index.html)
      * json
      * decimal
    - search engine
      * [nltk](https://www.nltk.org/)
      * [autocorrect](https://github.com/phatpiglet/autocorrect)
3. DynamoDB
    - [DynamoDB](https://aws.amazon.com/dynamodb/) (Local version is ok with this project)
    
## How The WPI Courses Finder works
[Building the search engine]
We crawled and stored all the courses data in dynamoDB. After that, TF-iDF table for course description, inverted index for title and inverted index for bi-word(2 terms combination) are built for course searching.<br> 

[Searching Courses]
Given a query content provided by user, the client javascript will send the query to server using json and websocket, then the server will pass the query to python root file using PythonShell. In backend, the query will be tokenized, stemming and corrected. Then with designed searching methods and structures(invertedIndex, tfidf, cosine-similarity) we build beforehand, courses relevant to the query will be retrieved from dynamoDB using boto3 and send back to server. Finally, the server will pass the courses data to client using WebSocket ,and the client program can update the courses data on the screen.
<br>
![Image of Prototype](https://github.com/Laxatony/WPI_Project_CourseFinder/blob/master/flows.png)

    
## How To Use
### Using the crawler:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
First you need a valid WPI student ID, since the crawler is accessing WPI courses system. The ID is needed for log-in before the crawler can start its work. Make sure the crawler_tool.py and your browser driver execution for crawler are in the same directory, then just execute the crawler_tool.py. A new browser window should be created, and you should see the website in the browser being navigated automatically.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[Notice] The crawler uses tags such as 'id', 'class' and XPath to get the perticular information. It fails when the tags it is looking for are no longer available or the hierarchical structure of the target webpage is changed.
<br>

### Accessing DynamoDB:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[Notice] The tables are designed based on WPI courses information, so the data processing procedure is also based on this project's need. However, how to access DynamoDB(insert/delete/update/query/scan) using Python is the same for any project. Primary methods for access a dynamoDB is implemented in WpiDynamoDBController.py.

### Hosting your own WPI courses finder
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
The courses finder service is a web based application. It consists of client, server and database. First you have to lunch your server and the database respectively(can be done all in local):<br>
- Lunch server.js : open Command Prompt and direct to the server.js directory, type: ```node server.js```
- Lunch DynamoDB : open Command Prompt and direct to the local dynamoDB directory, type: ```java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Now you can open index.html to use the website with your local database.

## Futher Work
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Currently, the system does not support wildcard searching. Also abbreviation such as 'ML' is not recognized as 'Machine Learning'.
These features can be added to the system, making it more desirable.


.
