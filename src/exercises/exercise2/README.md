# Exercise 2  

For this exercise, please write a Python application that processes two data files:

1. A PostgreSQL table containing student data
2. A MongoDB collection containing teacher data

From these data stores, generate an output file in JSON listing:

1. Each student
2. The teacher the student has
3. The class ID the student is scheduled for

Assumptions:
* An analyst with no Python coding ability should be able to setup and run the 
app using the directions provided.
* The software will run on a machine with limited resources, and it may not be 
possible to read all the data into memory at one time.
  
## Database Servers
* You have to have postgressql and mongo db up and running, see steps to deploy below.
* [Steps to deploy and start postgresql and mongodb instances in the docker container](../../database/README.md)