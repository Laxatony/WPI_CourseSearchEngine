class CourseInfo:
    def __init__(self):
        self.term = 'Spring 2019'                   # string *
        self.reference = '21026'                    # string *
        self.subject = 'Data Science'               # string
        self.title = 'Big Data Management'          # string
        self.course_index = '585'                   # string
        self.section = '191'                        # string
        self.campus = '1'                           # string
        self.days = 'M'                             # string
        self.time = '06:00 pm-08:50 pm'             # string
        self.capacity = '30'                        # string
        self.registered = '3'                       # string
        self.remaining = '27'                       # string
        self.instructor = 'Elke A. Rundensteiner(P)'# string
        self.date = '01/09-04/30'                   # string
        self.location = 'SH 309'                    # string
        self.description = 'no description'         # string
        self.cid = self.term + ' ' + self.subject + ' ' + self.course_index + ' ' + self.reference # string *

    def updateCID(self):
        # "term + ' ' + subject + ' ' + course_index + ' ' + reference"
        self.cid = self.term + ' ' + self.subject + ' ' + self.course_index + ' ' + self.reference # string *

    def generateJSONObj(self):
        result = {}
        result['term'] = self.term
        result['reference'] = self.reference
        result['subject'] = self.subject
        result['title'] = self.title
        result['course_index'] = self.course_index
        result['section'] = self.section
        result['campus'] = self.campus
        result['days'] = self.days
        result['time'] = self.time
        result['capacity'] = self.capacity
        result['registered'] = self.registered
        result['remaining'] = self.remaining
        result['instructor'] = self.instructor
        result['date'] = self.date
        result['location'] = self.location
        result['description'] = self.description
        result['cid'] = self.cid

        return result

    def generateFromJSONObj(self, jsonObj):
        self.term = jsonObj['term']
        self.reference = jsonObj['reference']
        self.subject = jsonObj['subject']
        self.title = jsonObj['title']
        self.course_index = jsonObj['course_index']
        self.section = jsonObj['section']
        self.campus = jsonObj['campus']
        self.days = jsonObj['days']
        self.time = jsonObj['time']
        self.capacity = jsonObj['capacity']
        self.registered = jsonObj['registered']
        self.remaining = jsonObj['remaining']
        self.instructor = jsonObj['instructor']
        self.date = jsonObj['date']
        self.location = jsonObj['location']
        self.description = jsonObj['description']
        self.updateCID()

    def toLower_all(self):
        self.term = self.term.lower()
        self.reference = self.reference.lower()
        self.subject = self.subject.lower()
        self.title = self.title.lower()
        self.course_index = self.course_index.lower()
        self.section = self.section.lower()
        self.campus = self.campus.lower()
        self.days = self.days.lower()
        self.time = self.time.lower()
        self.capacity = self.capacity.lower()
        self.registered = self.registered.lower()
        self.remaining = self.remaining.lower()
        self.instructor = self.instructor.lower()
        self.date = self.date.lower()
        self.location = self.location.lower()
        self.description = self.description.lower()
        self.cid = self.cid.lower()



