#!/usr/bin/env python2.7

import psycopg2
from datetime import datetime, date
from dbviews import init_views

DBNAME = "news"

try:
    db = psycopg2.connect(database=DBNAME)
    init_views(db)

    print DBNAME.upper() + " database analysis:"
    print "\n"

    c = db.cursor()
    c.execute("""select distinct articles.title, count(log.id) as num
                from articles join log on log.path like '%'||articles.slug
                group by articles.title order by num desc limit 3; """)
    pop_arts = c.fetchall()
    print "Three most viewed articles are: "
    for entity in pop_arts:
        print str(entity[0]) + " - " + str(entity[1]) + " views"

    c.execute("""select authors.name, sum(mp_arts.num) as vs
              from  authors, mp_arts, articles
                where mp_arts.slug = articles.slug
                and articles.author = authors.id
                group by authors.name order by vs desc;""")
    pop_authors = c.fetchall()
    print "\n"
    print "The most popular article authors of all time are: "
    for entity in pop_authors:
        print str(entity[0]) + " - " + str(entity[1]) + " views"

    c.execute("""select total.log_date,
                (select count(*) from log where status='404 NOT FOUND'
                    and date(log.time) = total.log_date
                )::float / count(*) * 100 as failed_requests
                from log, total
                where total.log_date = date(log.time)
                group by total.log_date, total.requests
                order by total.log_date;""")
    fail_days = c.fetchall()
    print "\n"
    print "Days on which more than 1% of requests lead to errors are:"
    for entity in fail_days:
        if float(entity[1] > 1.0):
            log_date_str = str(entity[0])
            formatter_string = "%Y-%m-%d"
            log_date = datetime.strptime(log_date_str, formatter_string)
            print log_date.strftime('%d, %b %Y') +\
                " - " + "{0:.2f}%".format(entity[1])
    db.close()
except psycopg2.Error as e:
        print "An exception occured: " + str(e)
