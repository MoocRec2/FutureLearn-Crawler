from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

client = MongoClient('mongodb://forum_analyzer:admin123@ds157901.mlab.com:57901/moocrecv2')

database = client.moocrecv2


class Thread:

    @staticmethod
    def save_threads(threads):
        try:
            result = database.threads.insert(threads)
            return result
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
        except:
            print('An Error Occurred')

    @staticmethod
    def upsert_threads(threads):
        try:
            for thread in threads:
                database.threads.update_one({'id': thread['id']}, {"$set": thread}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False

    @staticmethod
    def get_discussion_threads_with_responses(course_id):
        try:
            results = database.threads.find(
                {
                    'course_id': course_id,
                    'thread_type': 'discussion',
                    '$or': [
                        {'children': {'$exists': 'true'}},
                        {'non_endorsed_responses': {'$exists': 'true'}}
                    ]
                }
            ).limit(100)
            return results
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return

    @staticmethod
    def get_sentiment_analyzed_threads():
        try:
            results = database.Threads.find({
                'course_id': 'course-v1:UCSanDiegoX+DSE200x+1T2019a',
                'thread_type': 'discussion',
                '$or': [
                    {'children': {'$exists': 'true'}},
                    {'non_endorsed_responses': {'$exists': 'true'}}
                ],
                '$and': [{'is_sentiment_analyzed': {'$exists': 'true'}}, {'sentiment_score': {'$exists': 'true'}}]
            }, {'is_sentiment_analyzed': 1, 'sentiment_score': 1}).sort({'sentiment_score': -1})
            return results
        except:
            return []


class FutureLearnThreads:

    @staticmethod
    def upsert_threads(threads):
        try:
            for thread in threads:
                database.future_learn_threads.update_one({'id': thread['id']}, {"$set": thread}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False


class Course:

    @staticmethod
    def upsert_courses(courses):
        try:
            for course in courses:
                database.courses.update_one({'key': course['key']}, {"$set": course}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False

    @staticmethod
    def get_course(course_key):
        try:
            courses = database.courses.find({'key': course_key})
            return courses[0]
        except:
            return None

    @staticmethod
    def get_all_courses():
        try:
            courses = database.courses.find()
            return courses
        except:
            return None

    @staticmethod
    def convert_all_courses_to_edx():
        courses = Course.get_all_courses()
        count = 1
        new_courses = []
        for course in courses:
            if 'platform' in course.keys():
                pass
            else:
                course['platform'] = 0
                new_courses.append(course)
            count += 1

        print('Processed', count)
        Course.upsert_courses(new_courses)
        print('saving to DB')
