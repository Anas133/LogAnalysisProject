Project Description:

This project is a Log Analysis for answer three questions from a database, these questions are:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors?

Requirements:

1.PostgreSQL
2.Python (i'm using python3, so i recommend it).
3.Database.
4.vagrant 

Database Set-up:

1. download the database newsdata.sql, it's too large I can't upload it to the github.
2. put the newsdata.sql to the vagrant file.
3. create the news by using the command psql -d news -f newsdata.sql.
4. connect to the database from python 
   db = psycopg2.connect("dbname=news")
5. creating views:

CREATE VIEW AccessError as
            select date(time) as date, count(status) as error 
            from log 
            where status != '200 OK' 
            group by date;

Create view AllAccess as 
            select date(time) as date, count(status) as access 
            from log
            group by date;

How to run?
python3 project.py

