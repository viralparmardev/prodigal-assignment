# Viral Parmar's solution to Prodigal's assignment

Link to the problem statement and requirements: 

https://www.notion.so/Develop-API-using-a-mongoDB-database-hosted-on-MongoDB-Atlas-ef7e2d2078fa45a6af2d21c33fe5d72a


## Tools and Technologies

I've used Flask and PyMongo to develop this solution, with PyCharm as my IDE of choice and Postman for API testing.

The deployment resides on Heroku as a Gunicorn sever. No AWS EC2 instances were harmed during the making of the solution.


**Deployment URL:** https://prodigal-viralparmardev.herokuapp.com/students (change the endpoint for the different cases)


**Postman collection:** https://www.getpostman.com/collections/5c70a1ff3cf064f1c1b5


## Things I would have changed in the DB

I might have created a separate collection of classes just to separate out the concern of classes and grades

I'd also introduce caching over the frequency accessed elements like the class_id and student_id


## Things I could not do in this submission (due to short of time)

Implementing the logic to add grades

Removal of duplicates in classes taken by a student by finding better grades

---

Hope you liked my submission... any feedback is most welcome!

Thanks and regards,

Viral Parmar

https://viralparmar.ml
