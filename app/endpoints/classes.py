from flask_restful import Resource

from common.database import db
from common.config import STUDENTS_COLLECTION, GRADES_COLLECTION


class GetAllClasses(Resource):
    def get(self):
        grades_collection = db[GRADES_COLLECTION]
        classes_list = grades_collection.find(
            {},
            {
                "_id": 0,
                "class_id": 1
            }
        )

        return list(classes_list)


class GetListOfStudentsTakingACourse(Resource):
    def get(self, class_id):
        try:
            class_id = int(class_id)
        except ValueError:
            return "Please pass an integer as class_id", 400

        grades_collection = db[GRADES_COLLECTION]
        student_list_for_class_id = grades_collection.find(
            {
                "class_id": class_id
            },
            {
                "_id": 0,
                "student_id": 1
            }
        )
        student_list_for_class_id = list(student_list_for_class_id)
        if not student_list_for_class_id:
            return "No class found with this class_id", 404

        students_collection = db[STUDENTS_COLLECTION]
        students_master_list = list(students_collection.find())

        students_master_dict = {}
        for student in students_master_list:
            students_master_dict[student["_id"]] = student["name"]

        for student in student_list_for_class_id:
            student["student_name"] = students_master_dict[student["student_id"]]

        response = {
            "class_id": class_id,
            "students": list(student_list_for_class_id)
        }

        return response


class GetAggregatePerformanceOfEachStudent(Resource):
    def get(self, class_id):
        try:
            class_id = int(class_id)
        except ValueError:
            return "Please pass an integer as class_id", 400

        grades_collection = db[GRADES_COLLECTION]
        class_student_and_marks_list = grades_collection.aggregate(
            [
                {
                    "$match": {
                        "class_id": class_id
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "student_id": 1,
                        "total_marks":  {
                            "$toInt": {
                                "$sum": "$scores.score"
                            }
                        }
                    }
                }
            ]
        )
        class_student_and_marks_list = list(class_student_and_marks_list)
        if not class_student_and_marks_list:
            return "No class found with this class_id", 404

        students_collection = db[STUDENTS_COLLECTION]
        students_master_list = list(students_collection.find())

        students_master_dict = {}
        for student in students_master_list:
            students_master_dict[student["_id"]] = student["name"]

        for student in class_student_and_marks_list:
            student["student_name"] = students_master_dict[student["student_id"]]

        response = {
            "class_id": class_id,
            "students": list(class_student_and_marks_list)
        }

        return response


class GetGradesForAParticularCourse(Resource):
    def get(self, class_id):
        try:
            class_id = int(class_id)
        except ValueError:
            return "Please pass an integer as class_id", 400

        grades_collection = db[GRADES_COLLECTION]
        class_student_and_marks_list = grades_collection.aggregate(
            [
                {
                    "$match": {
                        "class_id": class_id
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "student_id": 1,
                        "scores": 1
                    }
                }
            ]
        )
        class_student_and_marks_list = list(class_student_and_marks_list)
        if not class_student_and_marks_list:
            return "No class found with this class_id", 404

        students_collection = db[STUDENTS_COLLECTION]
        students_master_list = list(students_collection.find())

        students_master_dict = {}
        for student in students_master_list:
            students_master_dict[student["_id"]] = student["name"]

        for index, student in enumerate(class_student_and_marks_list):
            marks_list = class_student_and_marks_list[index]["scores"]
            total_marks = 0
            homework_counter = 0

            for item in marks_list:
                if item["type"] == "homework":
                    homework_counter += 1
                    item["type"] += str(homework_counter)

                int_marks = int(item["score"])
                item["marks"] = int_marks
                total_marks += int_marks
                del item["score"]

            marks_list.append({
                "type": "total",
                "marks": total_marks
            })

            del student["scores"]
            student["details"] = marks_list
            student["student_name"] = students_master_dict[student["student_id"]]

            # TODO add grade logic
            student["grade"] = "A"

        response = {
            "class_id": class_id,
            "students": list(class_student_and_marks_list)
        }

        return response
