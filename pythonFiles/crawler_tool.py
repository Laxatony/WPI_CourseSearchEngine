import sys
import time
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from courseInfo import CourseInfo
from WpiDynamoDBController import WpiDynamoDBController
#driver.page_source

class WPI_BannerWeb_Course_Crawler:

    def __init__(self, login_url, userName, userPwd):
        self._maxTestAmount = 100
        self._totalClasses = 0
        self._driver = webdriver.Chrome()
        self._userName = userName
        self._password = userPwd

        self._driver.get(login_url)
        self._quarters = []

        self._myDynamoDB = WpiDynamoDBController()

    def _login_page_(self):
        # 1. enter username
        # 2. enter password
        # 3. press [Log in]
        time.sleep(0.5)
        self._driver.find_element_by_xpath("//form[1]/table[1]/tbody[1]/tr[1]/td[2]/input[1]").send_keys(self._userName)
        time.sleep(0.5)
        self._driver.find_element_by_xpath("//form[1]/table[1]/tbody[1]/tr[2]/td[2]/input[1]").send_keys(self._password)
        time.sleep(0.5)
        self._driver.find_element_by_xpath("//table[1]/tbody[1]/tr[3]/td[1]/input[1]").click()
        print("leave _login_page, enter _mainMenu_page")

    def _mainMenu_page_(self):
        # 1. press [Student Services & Financial Aid] 
        time.sleep(0.5)   # delays for 1 seconds. You can Also Use Float Value.
        self._driver.find_element_by_xpath("//table[@class='menuplaintable']/tbody[1]/tr[2]/td[2]/a[1]").click()
        print("leave _mainMenu_page, enter _studentServices_page")

    def _studentServices_page_(self):
        # 1. press [Registration] 
        time.sleep(0.5)   # delays for 1 seconds. You can Also Use Float Value.
        self._driver.find_element_by_xpath("//table[@class='menuplaintable']/tbody[1]/tr[2]/td[2]/a[1]").click()
        print("leave _studentServices_page, enter _registration_page")

    def _registration_page_(self):
        # 1. press [Look-up Classes to Add] 
        time.sleep(0.5)   # delays for 1 seconds. You can Also Use Float Value.
        self._driver.find_element_by_xpath("//table[@class='menuplaintable']/tbody[1]/tr[3]/td[2]/a[1]").click()
        print("leave _registration_page, enter _lookupClass_page")

    def _lookupClass_page_(self, numOfQuarters):
        from selenium.webdriver.support.ui import Select

        for termIndex in range(1, (numOfQuarters+1)): # 3quarter = range(1, 4) position[0] is [Term:NULL]
             # Term Selection Page
            select_box_term = Select(self._driver.find_element_by_id("term_input_id"))

            # Set quarter
            select_box_term.select_by_index(termIndex)
            self._driver.find_element_by_xpath("//div[3]/form[1]/input[2]").click()
            # =====================================================================

            select_box_subject = Select(self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[1]/td[2]/select[@name="sel_subj"]'))
            subjectNum = len(select_box_subject.options)
            for subjectIndex in range(subjectNum):

                # Subject Selection Page
                select_box_subject = Select(self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[1]/td[2]/select[@name="sel_subj"]'))
        
                # print(option.text, option.get_attribute('value'))
                if subjectIndex > 0:
                    select_box_subject.deselect_by_index((subjectIndex-1))
                select_box_subject.select_by_index(subjectIndex)
                self._driver.find_element_by_xpath("//div[3]/form[1]/input[17]").click()

                # Navigate Course Page
                self._course_page_()
                self._driver.back() # back from course page to subject page
                #time.sleep(0.5)

            self._driver.back() # back from subject page to term page
            time.sleep(1)

    def _course_page_(self):

        course_RootXPath = "//div[3]/table[2]/tbody[1]/tr"

        # Get Course row amount
        rowCount = len(self._driver.find_elements_by_xpath(course_RootXPath))
        #rowCount: 10 -> course info is in tr[3]~tr[10] (tr[1~2] is title row)

        # Get Course Term and Subject name
        termPath = course_RootXPath + '[1]' + '/th[1]/span[1]'
        termList = self._driver.find_elements_by_xpath(termPath)
        term = ""
        for element in termList:
            term = element.text
        print('term: ', term)

        subjectPath = course_RootXPath + '[2]' + '/th[1]'
        subjectList = self._driver.find_elements_by_xpath(subjectPath)
        subject = ""
        for element in subjectList:
            subject = element.text
        print('subject: ', subject)
        
        # ==================================================

        # Access Course information one by one
        for courseIndex in range(3, (rowCount+1)):
            inner_CourseFormXPath = course_RootXPath + '[' + str(courseIndex) + ']' + '/td[3]/form[1]/input'
            courseFormInputCount = len(self._driver.find_elements_by_xpath(inner_CourseFormXPath))
            # Button is the last one
            course_Btn_XPath = inner_CourseFormXPath + '[' + str(courseFormInputCount) + ']'
            self._driver.find_element_by_xpath(course_Btn_XPath).click()
            self._get_course_info_(term, subject)
            self._driver.back() # back from course info page to all courses page

    def _get_course_info_(self, term, subject):

        courseItem_RootXPath = "//div[3]/form[1]/table[1]/tbody[1]/tr"
        # Get Course row amount
        rowCount = len(self._driver.find_elements_by_xpath(courseItem_RootXPath))
        #rowCount: 4 -> course info is in tr[3]~tr[4] (tr[1~2] is title row)

        for itemIndex in range(3, (rowCount+1)):
            itemXPath = courseItem_RootXPath + '[' + str(itemIndex) + ']'
            crn = self._driver.find_element_by_xpath(itemXPath + '/td[2]').text
            if crn == ' ':
                continue

            courseInfo = CourseInfo()
            courseInfo.term = term
            courseInfo.reference = crn
            courseInfo.subject = subject
            courseInfo.course_index = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[4]').text
            courseInfo.section = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[5]').text
            courseInfo.campus = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[6]').text
            courseInfo.title = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[8]').text
            courseInfo.days = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[9]').text
            courseInfo.time = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[10]').text
            courseInfo.capacity = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[11]').text
            courseInfo.registered = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[12]').text
            courseInfo.remaining = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[13]').text
            courseInfo.instructor = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[20]').text
            courseInfo.date = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[21]').text
            courseInfo.location = self._driver.find_element_by_xpath('//div[3]/form[1]/table[1]/tbody[1]/tr[3]/td[22]').text
            courseInfo.updateCID()

            self._myDynamoDB.insert_course_item(courseInfo)
            self._totalClasses += 1
            self._maxTestAmount -= 1
            
    def automation(self):
        self._login_page_()
        self._mainMenu_page_()
        self._studentServices_page_()
        self._registration_page_()

        # quartersAmount = 3
        # self._lookupClass_page_(quartersAmount)

        #self._driver.back()

    def close(self):
        self._driver.close()


class WPI_Schedule_Planner_Crawler:

    def __init__(self, login_url, userName, userPwd):
        self._driver = webdriver.Chrome()
        self._userName = userName
        self._password = userPwd

        self._driver.get(login_url)
        self._quarters = []

        self._myDynamoDB = WpiDynamoDBController()

    def _login_page_(self):
        # 1. enter username
        # 2. enter password
        # 3. press [Log in]
        time.sleep(0.5)
        self._driver.find_element_by_xpath("//form[1]/table[1]/tbody[1]/tr[1]/td[2]/input[1]").send_keys(self._userName)
        time.sleep(0.5)
        self._driver.find_element_by_xpath("//form[1]/table[1]/tbody[1]/tr[2]/td[2]/input[1]").send_keys(self._password)
        time.sleep(0.5)
        self._driver.find_element_by_xpath("//table[1]/tbody[1]/tr[3]/td[1]/input[1]").click()
        print("leave _login_page, enter _mainMenu_page")

    def _mainMenu_page_(self):
        # 1. press [Student Services & Financial Aid] 
        time.sleep(0.5)   # delays for 1 seconds. You can Also Use Float Value.
        self._driver.find_element_by_xpath("//table[@class='menuplaintable']/tbody[1]/tr[2]/td[2]/a[1]").click()
        print("leave _mainMenu_page, enter _studentServices_page")

    def _studentServices_page_(self):
        # 1. press [Registration] 
        time.sleep(0.5)   # delays for 1 seconds. You can Also Use Float Value.
        self._driver.find_element_by_xpath("//table[@class='menuplaintable']/tbody[1]/tr[2]/td[2]/a[1]").click()
        print("leave _studentServices_page, enter _registration_page")

    def _registration_page_(self):
        # 1. press [Schedule Planner] 
        time.sleep(0.5)   # delays for 1 seconds. You can Also Use Float Value.
        self._driver.find_element_by_xpath("//table[@class='menuplaintable']/tbody[1]/tr[10]/td[2]/a[1]").click()
        time.sleep(1.5)   # it takes longer time for page switch
        print("leave _registration_page, enter _schedule_planner_page_")

    def _schedule_planner_intro_page_(self):
        # First term selection page (just click submit)
        self._driver.find_element_by_xpath("//button[@class='btn btn-primary center-block btn-save']").click()
        time.sleep(5)
        # Second term selection page (just click submit)
        self._driver.find_element_by_xpath("//button[@class='btn btn-primary center-block btn-save']").click()
        time.sleep(5)
        
    def _schedule_planner_page_(self):

        # Enter Term Selection Page, check only number of terms and back
        self._driver.find_element_by_xpath("//div[@class='selected-term-label']/div[2]/a[1]").click()
        term_RootXPath = "//table[@class='table table-hover filter-grid']/tbody[1]/tr"
        rowCount = len(self._driver.find_elements_by_xpath(term_RootXPath))
        time.sleep(1)
        self._driver.back()

        print('rowCount: ', rowCount)
        for row in range(3, (rowCount+1)):
            # Enter Term Selection Page, to choose term by current row number
            self._driver.find_element_by_xpath("//div[@class='selected-term-label']/div[2]/a[1]").click()
            time.sleep(1)

            # Get corresponding term text
            term_XPath = term_RootXPath + '[' + str(row) + ']' + '/td[2]'
            term = self._driver.find_element_by_xpath(term_XPath).text
            print('selected term: ', term)
            time.sleep(1)

            # Press corresponding radio button
            term_selection_XPath = term_RootXPath + '[' + str(row) + ']' + '/td[1]/input[1]'
            self._driver.find_element_by_xpath(term_selection_XPath).click()
            time.sleep(1)

            # Press [SAVE BUTTON]
            self._driver.find_element_by_xpath("//button[@class='btn btn-primary pull-right btn-save']").click()
            time.sleep(1)

            # Go to [ADD COURSE] to loop course description
            self._driver.refresh()
            self._driver.find_element_by_xpath("//button[@class='btn btn-primary btn-course-add pull-right']").click()
            time.sleep(1)
            self._course_page_(term)
            
            # Get back to schedule planner main page
            self._driver.back()
            time.sleep(1)
            
    def _course_page_(self, term):
        from selenium.webdriver.support.ui import Select

        self._driver.refresh()
        time.sleep(2)
        # Open Subject Category and get num of Subject
        self._driver.find_element_by_xpath("//div[@id='s2id_subject-selector']/a[1]").click()
        time.sleep(1)
        list_box_subject = self._driver.find_elements_by_xpath("//ul[@id='select2-results-1']/li")
        subjectNum = len(list_box_subject)
        print('list num:', subjectNum)
        list_box_subject[0].click() # just for close the list

        for subjectIndex in range(15, subjectNum):
            self._driver.find_element_by_xpath("//div[@id='s2id_subject-selector']/a[1]").click()
            list_box_subject = self._driver.find_elements_by_xpath("//ul[@id='select2-results-1']/li")
            list_box_subject[subjectIndex].click()
            time.sleep(0.5)

            # Open course list and get num of course
            self._driver.find_element_by_xpath("//div[@id='s2id_course-selector']").click()
            time.sleep(1)
            list_box_subject = self._driver.find_elements_by_xpath("//ul[@id='select2-results-2']/li")
            courseNum = len(list_box_subject)
            list_box_subject[0].click() # just for close the list

            time.sleep(1)
            print('course num:', courseNum)
            for courseIndex in range(courseNum):
                self._driver.find_element_by_xpath("//div[@id='s2id_course-selector']").click()
                list_box_subject = self._driver.find_elements_by_xpath("//ul[@id='select2-results-2']/li")
                list_box_subject[courseIndex].click()

                time.sleep(1)
                # get subject and course_index from title
                title = self._driver.find_element_by_xpath("//h3[@class='panel-title']").text
                # title = 'DATA SCIENCE 503 - BIGDATAMANAGEMENT'
                firstDigitIndex = re.search("\d", title).start()
                subject = title[:(firstDigitIndex-1)]
                course_index = title[firstDigitIndex: title[firstDigitIndex:].find(' ')+firstDigitIndex]

                try:
                    description = self._driver.find_element_by_xpath("//div[@class='descr-pane']").text
                except NoSuchElementException as e:
                    description = 'no description'
                    print(term, subject, course_index)
                    cids = self._myDynamoDB.get_CIDs_by_partialInfo(term, subject, course_index)
                    for cid in cids:
                        print(cid)
                    self._myDynamoDB.update_courses_description(cids, description)
                else:
                    print(term, subject, course_index)
                    cids = self._myDynamoDB.get_CIDs_by_partialInfo(term, subject, course_index)
                    for cid in cids:
                        print(cid)
                    self._myDynamoDB.update_courses_description(cids, description)

        time.sleep(1)

            
    def automation(self):
        self._login_page_()
        self._mainMenu_page_()
        self._studentServices_page_()
        self._registration_page_()
        self._schedule_planner_intro_page_()
        self._schedule_planner_page_()

        #self._driver.back()

    def close(self):
        self._driver.close()


# userName = 'yhsieh2'
# userPwd = 'Laxative334670-1'

# Create Testing Database
def getExampleDatabase():
    courses = []

    course1 = CourseInfo()
    course1.term = 'Spring 2019'
    course1.subject = 'Data Science'
    course1.course_index = '585'
    course1.reference = '20016'
    course1.description = "Big Data Management is one of the hottest courses in WPI.\nEvery one should take this course instead of Machine Learning."
    course1.updateCID()
    courses.append(course1)

    course2 = CourseInfo()
    course2.term = 'Spring 2019'
    course2.subject = 'Computer Science'
    course2.course_index = '500'
    course2.reference = '21000'
    course2.description = "Deep Learning is more interesting than Machine Learning.\n It's not pure classification.\n Artificial Intelligence is a wild concept tought by Pro. Gini."
    course2.updateCID()
    courses.append(course2)

    course3 = CourseInfo()
    course3.term = 'Spring 2019'
    course3.subject = 'Computer Science'
    course3.course_index = '500'
    course3.reference = '21001'
    course3.description = "Data Science(DS)502 is teaching statistical learning.\n We will talk about methods for classification and clustering."
    course3.updateCID()
    courses.append(course3)

    return courses

def main(argv):

    login_url = "https://bannerweb.wpi.edu/pls/prod/twbkwbis.P_WWWLogin"
    userName = argv[1]
    userPwd = argv[2]

    wpi_crawler = WPI_BannerWeb_Course_Crawler(login_url, userName, userPwd)
    wpi_crawler.automation()
    wpi_crawler.close()
    time.sleep(5)

    # wpi_crawler = WPI_Schedule_Planner_Crawler(login_url, userName, userPwd)
    # wpi_crawler.automation()
    # wpi_crawler.close()

    
    # # Initial Database Connection ##########################
    # myDynamoDB = WpiDynamoDBController()

    # # Insert course ######################################
    # courses = getExampleDatabase()
    # for course in courses:
    #     myDynamoDB.insert_course_item(course)

    # # Get all courses ####################################
    # courses = myDynamoDB.get_courses_all()
    # count = 1
    # for course in courses:
    #     print(str(count) + ' ' +  course.cid + ':\n' + course.description + '\n')
    #     count += 1

    # # Update description #################################
    # term = 'Spring 2019'
    # subject = 'Computer Science'
    # course_index = '500'
    # courseCIDs = myDynamoDB.get_course_CIDs(term, subject, course_index)
    # print(courseCIDs)
    # input("pause")
    # description = "Updated description..."
    # myDynamoDB.update_courses_description(courseCIDs, description)


    
if __name__ == "__main__":
    import sys
    main(sys.argv)
