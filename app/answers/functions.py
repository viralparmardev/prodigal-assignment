from common.config import STUDENTS_COLLECTION, GRADES_COLLECTION


def func_q1(db):
    # Question: How many distinct students do we have data for?
    students_collection = db[STUDENTS_COLLECTION]
    distinct_students_represented_in_data = students_collection.distinct("_id").length
    return distinct_students_represented_in_data


def func_q2(db):
    # Question: How many different courses are represented in the data?
    grades_collection = db[GRADES_COLLECTION]
    different_courses_represented_in_data = grades_collection.distinct("class_id").length
    return different_courses_represented_in_data
