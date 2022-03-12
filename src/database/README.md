# Database Servers

Docker compose will run all needed development databases locally. 
A `docker-compose.yml` file has been provided. To startup the containaried local development environment, run:

> **Pre-requisite**:
>> You should have docker installed. If you are like me and using windows as your development enviroment
>> use this [link](https://docs.docker.com/desktop/windows/install/) to install docker desktop
>>> Using docker command  *'docker compose up'* to deploy container defined in docker-compose.yml

> What is docket compose
>> Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file
> to configure your application’s services. Then, with a single command, you create and start all the services from your configuration 

> Using sql driver psycopg2
>> pip install psycopg2

- cd src/database

## mongodb
- creates mongodb container
```
cd ./mongodb
docker compose up
```

### Connection Information
Here is connection information for the MongoDB data store:

```
username: testdb    
password: testdb    
database: testdb 
``` 

MongoDB collection: `teachers`
MongoDB GUI: http://localhost:8081

## postgresql
- creates a postgresql container
- cd src/database
```
cd ./postgresql
docker compose up
```

### Connection Information
Here is connection information for the PostgreSQL data store:

```
username: testdb    
password: testdb    
database: testdb 
``` 
PostgreSQL table: `students`
PostgreSQL GUI: http://localhost:8080  (make sure you put `postgres` as the server)

### Note: 
When writing code to connect to a data store, you should instead use **`localhost`** as the hostname.
