from flask_restful import Resource

from app.common.database import db
from app.common.config import STUDENTS_COLLECTION, GRADES_COLLECTION


class GetDetailedScoresForAStudentInACourse(Resource):
    def get(self, class_id, student_id):
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

        try:
            class_id = int(class_id)
        except ValueError:
            return "Please pass an integer as class_id", 400

        grades_collection = db[GRADES_COLLECTION]
        class_student_and_marks_list = grades_collection.find(
            {
                "class_id": class_id,
                "student_id": student_id
            },
            {
                "_id": 0,
                "scores": 1
            }
        )
        class_student_and_marks_list = list(class_student_and_marks_list)
        if not class_student_and_marks_list:
            return "No class found with this class_id", 404
        else:
            marks_list = class_student_and_marks_list[0]["scores"]
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

        response = {
            "class_id": class_id,
            "student_id": student_id,
            "student_name": student_name,
            "marks": marks_list
        }

        return response


class GetDetailedScoresForACourseOfAStudent(GetDetailedScoresForAStudentInACourse):
    pass
