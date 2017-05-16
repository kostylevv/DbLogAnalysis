Udacity Full Stack Nanodegree
Log Analysis Project submission

How to run?
To run program simply copy log_analysis.py to your Vagrant directory
and write: python log_analysis.py in the terminal.
No additional preparation such as adding views (see below) is needed.
Program is written in Python 2.7.

Program Design
The program is intended to perform analysis on database log table to answer
the following questions:
1. What are the most popular three articles of all time? Which articles have been accessed the most?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

So the design is very straightforward: there are three sql-requests to answer
corresponding questions.

As required by specification almost all work is done by sql-requests.
Python code only include iteration on cursor and formatting output.

Two last queries use views:
For popular authors requests - mp_arts view:
"create view mp_arts as select distinct articles.slug,
count(log.id) as num from articles join log on log.path like '%'||articles.slug
group by articles.slug order by num desc;"

For request failure days - total view:
"create view total as select date(time) as log_date, count(*) as requests
from log group by date(time);"

However views are created with a "create or replace" command so you don't
need to create them manually via psql prior to launch the program.
