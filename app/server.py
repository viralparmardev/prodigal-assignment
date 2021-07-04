from flask import Flask
from flask_restful import Api


from endpoints.courses import GetDetailedScoresForAStudentInACourse, GetDetailedScoresForACourseOfAStudent
from endpoints.students import GetAllStudents, GetListOfClassesForAStudent, GetAggregatePerformanceInEachClass
from endpoints.classes import GetAllClasses, GetListOfStudentsTakingACourse, GetAggregatePerformanceOfEachStudent, \
    GetGradesForAParticularCourse


app = Flask(__name__)
api = Api(app)

api.add_resource(GetDetailedScoresForAStudentInACourse, '/class/<class_id>/student/<student_id>')
api.add_resource(GetDetailedScoresForACourseOfAStudent, '/student/<student_id>/class/<class_id>')

api.add_resource(GetAllStudents, '/students')
api.add_resource(GetListOfClassesForAStudent, '/student/<student_id>/classes')
api.add_resource(GetAggregatePerformanceInEachClass, '/student/<student_id>/performance')

api.add_resource(GetAllClasses, '/classes')
api.add_resource(GetListOfStudentsTakingACourse, '/class/<class_id>/students')
api.add_resource(GetAggregatePerformanceOfEachStudent, '/class/<class_id>/performance')
api.add_resource(GetGradesForAParticularCourse, '/class/<class_id>/final-grade-sheet')


if __name__ == '__main__':
    app.run(debug=True)
