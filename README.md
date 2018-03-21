# WPI_Find Me A Course
This project is aim to help students in WPI search courses more efficient using techniques similar to modern search engines.

## I. Team Member
* Yaichun Hsieh (Data Science) &nbsp;&nbsp; yhsieh2@wpi.edu
* Yang Tao (Data Science)     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ytao2@wpi.edu
* Haowen Zhu (Data Science)   &nbsp;&nbsp;&nbsp;&nbsp; hzhu3@wpi.edu


## II. Motivation
We want to build a search engine for students to search for their desired courses by simply typing the key-word about the course. For example, if some students want to study the topic about ‘machine learning’, the search engine should return courses related to ‘machine
learning’, like ‘Introduction of Machine Learning’, ’Artificial Intelligence’, which contain knowledge about ‘machine learning’.

Basically, most universities have their own course registration system, some of them are pretty advanced and could support such function. However, in the WPI course registration system, students could only search course by the semester, major, then scan the whole list of courses for that specific major to find their desired courses. It is inefficient and some students might miss their target courses since they could not read all course description across different majors. So we want to optimize the search function of the course registration system by returning

## III. Dataset Source
Crawling the data of information about different courses from the WPI course registration system.

## IV. Approach and Challenges
We will crawl the data of all courses, containing title, course ID, instructor, course description and semester from the WPI course registration system. Next, we will filter and archive each course in its corresponding field. Use **TF-IDF** to extract features of each course and build an inverted index. Then build the vector space model for each course with normalized TF-IDF value. After inputting a certain query, our system will return a bunch of courses and sort them in a descending order according to their correlation, course ID, instructor popularity. The correlation between query and result courses are computed using **vector space cosine similarity**.

There are several challenges in this project that we have to deal with:<br>
1. **A well designed automatic crawler for data collection.**<br>
Crawling data from WPI course website manually is cumbersome. For the usability of the application, the crawler should automatically + + retrieve needed data for further use.

2. **Word Lemmatization.**<br>
By definition, lemmatization in linguistics is the process of grouping together the inflected forms of a word so they can be analysed as a single item, identified by the word's lemma, or dictionary form. Apart from applying stemming for words, if time
permits, normalization will be implemented, identifying words like ‘IR’ and ‘Information Retrieval’ as the same term.

3. **Updating parameters of our ranknig model with user’s behaviors.**<br>
In addition to using TF-IDF with cosine similarity as the main ranking approach, we assume that the most relevant course information has the highest amount of review. Therefore, we want to introduce user’s review information into our ranking model as well. For example, given a query term ‘Machine Learning’, if the second result rovided by our ranking system actually has the highest amount of review or the highest authority, the system should take this situation into account, and maybe result in placing the second result at first position. Come up with appropriate formula could be chanllenging.

## V. Evaluation
In the testing process, we will test the demo ourselves to evaluate the accuracy of the results. Besides, we will invite WPI students to use the demo and provide feedback to strength the authority of the results. For long term evaluation, we are going to monitor the ranking performance using the NDCG(Normalized Discounted Cumulative Gain) method. To be more specific, we will normalized the amount of reviews for each query as the ground truth ranking score once a week. Then we compute and average the NDCG value of all exciting
queries to see if the performance is improving over time.

## VI. Schedule
3/18 proposal<br>
4/24 deadline
