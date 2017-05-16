## Udacity Full Stack Nanodegree
## Log Analysis Project submission

### General Description
This program is a reporting tool that use information from hypothetical newspaper site
database and discover what kind of articles the site's readers like.

The database called "News" and contains newspaper articles, as well as the web server log for the site.
The log has a database row for each time a reader loaded a web page.

The program is intended to perform analysis to answer the following questions:
1. What are the most popular three articles of all time? Which articles have been accessed the most?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### How to install and run
1. Install Virtual Box and Vagrant as specified here [here](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
2. Run up vagrant with **vagrant up**, then log into it with **vagrant ssh**
3. Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
Unzip this file after downloading it. The file inside is called **newsdata.sql**. Put this file into the vagrant directory,
which is shared with your virtual machine.
4. Load data with following command: **psql -d news -f newsdata.sql**
If this command gives an error message, such as —
psql: FATAL: database "news" does not exist
psql: could not connect to server: Connection refused
— this means the database server is not running or is not set up correctly.
Usually this means that your VM was not configured right,
and will need to be reinstalled before you can continue with the project.
5. Put **log_analysis.py** and **dbviews.py** to your vagrant directory.
6. Run program with **python log_analysis.py**

Program should give an output close to **output_example.txt** or raise an error.

### Notes

Program use views i.e. virtual tables, to execute log analysis queries.
These views are:
+ **mp_arts** - creates a virtual table of article slugs
and the number of times those slugs appear in the log and
specified as follows:
```
create or replace view mp_arts as select distinct articles.slug,
        count(log.id) as num
        from articles join log on log.path like '%'||articles.slug
        group by articles.slug;
```

+ **total** - virtual table of total number of requests
for every day in a log and
specified as follows:
```
create or replace view total as
                select date(time) as log_date, count(*) as requests
                from log group by date(time);
```
Views are created with a "create or replace" command so you don't
need to create them manually via psql prior to launch the program.
