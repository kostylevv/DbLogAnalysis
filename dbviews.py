#!/usr/bin/env python2.7

import psycopg2

"""Creates views, i.e. virtual tables,
necessary to execute log analysis queries"""


def init_views(db):
        c = db.cursor()

        """This view creates a virtual table of article slugs
        and the number of times those slugs appear in the log"""
        c.execute("""create or replace view mp_arts as select distinct articles.slug,
                count(log.id) as num
                from articles join log on log.path like '%'||articles.slug
                group by articles.slug;""")

        """This view creates a virtual table of total number of requests
        for every day in a log"""
        c.execute("""create or replace view total as
                        select date(time) as log_date, count(*) as requests
                        from log group by date(time);""")
