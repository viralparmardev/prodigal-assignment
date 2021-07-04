from flask_restful import Resource

from app.common.database import db
from app.common.config import STUDENTS_COLLECTION, GRADES_COLLECTION


class GetAllStudents(Resource):
    def get(self):
        students_collection = db[STUDENTS_COLLECTION]
        students_list = students_collection.aggregate(
            [
                {
                    "$project": {
                        "_id": 0,
                        "student_id": "$_id",
                        "student_name": "$name"
                    }
                }
            ]
        )

        return list(students_list)


class GetListOfClassesForAStudent(Resource):
    def get(self, student_id):
        try:
            student_id = int(student_id)
        except ValueError:
            return "Please pass an integer as student_id", 400

        students_collection = db[STUDENTS_COLLECTION]
        student_name_record = students_collection.find(
            {
                "_id": student_id
            }, {
                "_id": 0
            }
        )
        student_name_record = list(student_name_record)
        if not student_name_record:
            return "No student found with this student_id", 404
        student_name = student_name_record[0]["name"]

        grades_collection = db[GRADES_COLLECTION]
        classes_taken_by_student_list = grades_collection.find(
            {
                "student_id": student_id
            },
            {
                "_id": 0,
                "student_id": 0,
                "scores": 0
            }
        )

        response = {
            "student_id": student_id,
            "student_name": student_name,
            "classes": list(classes_taken_by_student_list)
        }

        return response


class GetAggregatePerformanceInEachClass(Resource):
    def get(self, student_id):
        try:
            student_id = int(student_id)
        except ValueError:
            return "Please pass an integer as student_id", 400

        students_collection = db[STUDENTS_COLLECTION]
        student_name_record = students_collection.find(
            {
                "_id": student_id
            }, {
                "_id": 0
            }
        )
        student_name_record = list(student_name_record)
        if not student_name_record:
            return "No student found with this student_id", 404
        student_name = student_name_record[0]["name"]

        grades_collection = db[GRADES_COLLECTION]
        student_classes_and_marks_list = grades_collection.aggregate(
            [
                {
                    "$match": {
                        "student_id": student_id
                    }

                },
                {
                    "$project": {
                        "_id": 0,
                        "class_id": 1,
                        "total_marks":  {
                            "$toInt": {
                                "$sum": "$scores.score"
                            }
                        }
                    }
                }
            ]
        )

        response = {
            "student_id": student_id,
            "student_name": student_name,
            "classes": list(student_classes_and_marks_list)
        }

        return response
