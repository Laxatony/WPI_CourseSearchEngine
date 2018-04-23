# WPI Course Finder
This project is aim to help students in WPI search courses more efficient using techniques similar to modern search engines.

## I. Team Member
* Yaichun Hsieh (Data Science) &nbsp;&nbsp; yhsieh2@wpi.edu
* Yang Tao (Data Science)     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ytao2@wpi.edu
* Haowen Zhu (Data Science)   &nbsp;&nbsp;&nbsp;&nbsp; hzhu3@wpi.edu


## II. Motivation
We want to build a WPI course search engine for students to search for their desired courses by simply typing in the key-word about the course. For example, if some students want to study the topic about ‘machine learning’, the search engine should return courses related to ‘machine learning’, like ‘Introduction of Machine Learning’, ’Artificial Intelligence’, which contain knowledge about ‘machine learning’.

Basically, most universities have their own course registration system, some of them are pretty advanced and could support such function. However, in the WPI course registration system, students could only search course by the semester, major, then scan the whole list of courses for that specific major to find their desired courses. It is inefficient and some students might miss their target courses since they could not read all course description across different majors. So we want to optimize the search function of the course registration system by returning

## III. Dataset Source
Crawling the data of information about different courses from the WPI course registration system.

## IV. Approach and Challenges

In general, we will retrieve the course data from WPI registration system and build TF-iDF matrix for each course for the course search engine. Also, we will provide a user interface for users to make query. The engine will use cosine similarity as computation function to find relavant courses and return the results to users. To achieve our goal, several tasks and related challenges are list below:<br>

1. **Crawling the data:**<br>
We will crawl the data of all courses, containing title, course ID, instructor, course description and semester from the WPI course registration system. As we all know, crawling data from website manually is cumbersome. For the usability of the application, the crawler should be able to automatically retrieve needed data. Therefore, we need to develop an automatic web crawler.<br>

2. **Storing the data:**<br>
Each course data will be stored in a NoSQL database. The reason for using a NoSQL database is because we will also store the unique **TF-IDF Matrix** for each course. In other words, we have to learn how to access a NoSQLdatabase<br>

3. **Data Preprocessing:**<br>
We will apply stemming and use **TF-IDF** representation to extract features of each course and build an inverted index. Also, we build the vector space model for each course with normalized TF-IDF value for further use. The bottleneck of data preprocessing is the lemmatization feature. By definition, lemmatization in linguistics is the process of grouping together the inflected forms of a word so they can be analysed as a single item, identified by the word's lemma, or dictionary form. Apart from applying stemming for words, if time permits, lemmatization will be implemented, identifying words like ‘IR’ and ‘Information Retrieval’ as the same term.<br>

4. **Query**<br>
Given a certain query, our system will return a bunch of courses and sort them in a descending order according to their correlation, course ID and instructor popularity. The correlation between query and result courses are computed using **vector space cosine similarity**. Since our target user is all the students in WPI, they should be able to access the search engine easily. Therefore, a web-based application is needed.<br>

5. **Updating parameters of our ranknig model with user’s behaviors.**<br>
In addition to using TF-IDF with cosine similarity as the main ranking approach, we assume that the most relevant course information has the highest amount of review. Therefore, we want to introduce user’s review information into our ranking model as well. For example, given a query term ‘Machine Learning’, if the second result rovided by our ranking system actually has the highest amount of review or the highest authority, the system should take this situation into account, and maybe result in placing the second result at first position. Come up with appropriate formula could be chanllenging.<br>

## V. Evaluation<br>
In the testing process, we will test the demo ourselves to evaluate the accuracy of the results. Besides, we will invite WPI students to use the demo and provide feedback to strength the authority of the results. For long term evaluation, we are going to monitor the ranking performance using the NDCG(Normalized Discounted Cumulative Gain) method. To be more specific, we will normalized the amount of reviews for each query as the ground truth ranking score once a week. Then we compute and average the NDCG value of all exciting
queries to see if the performance is improving over time.<br>

## VI. Schedule
3/18 proposal<br>
3/28 frond-end, back-end, database integration<br>
4/15 system complete<br>
4/24 presentation
