#!/usr/bin/env python3
import psycopg2
from operator import itemgetter
from time import gmtime, strftime
def reomveDup(list):
    NewList = []
    for e in list:
        if e not in NewList:
            NewList = e
    return NewList


def display(list1,list2,list3):

    time = strftime("%a, %d %b %Y %X", gmtime())
    print("Report in time", time + "\n"
    ,"\nThe Three Top articles are:")
    j = 0
    while len(list1) > j:
        print("{} - {} views".format(list1[j],list1[j+1]))
        j += 2
    print("\nAnd for a most popular authors:")
    for i in list2:
        if i[1] == 0:
            break
        print("{} - {} views".format(i[0],i[1]))

    for i in list3:
        print("\nAnd in", i[0],"The error rate was - ", i[1],"%")

def main():
    # connect to the database.
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # start to answer the first question.
    query = """select title,slug, path, count(path) as views
    from log full join articles on 1 = 1
    where status = '200 OK'
    group by path,slug, title
    order by views desc;"""
    c.execute(query)
    TopThree = c.fetchall()

    # filter the table to meet the desired result.
    Top3 = []
    AppendList = []
    count = 0
    for i in TopThree:
        if count == 3:
            break
        if len(i[2]) > 1: # check the validity of the path.
            ArticleName = i[2][9:]
            if i[1] == ArticleName:
                AppendList.append(i[0])
                AppendList.append(i[3])
                Top3.append(AppendList)
                count += 1

    Top3 = reomveDup(Top3) # removeing the duplicated result.
    # The Top3 result has the answer for question 1. ready to print it.

    # start to answer the second question.
    query = """select authors.name,articles.title,slug, path,
            count(path) as views
            from log full join
            (articles join authors on articles.author = authors.id) on 1 = 1
            where status = '200 OK'
            group by name,path,slug, title
            order by views desc;"""
    c.execute(query)
    data = c.fetchall()

    # filter the table to meet the desired result.
    ViewsArticle = []
    AuthorsList = []
    for i in data:
        if len(i[3]) > 1: # check the validity of the path.
            ArticleName = i[3][9:]
            if i[2] == ArticleName:
                ViewsArticle.append(i[4])
                AuthorsList.append(i[0])
    # calculate the totals of articles viewer to each author.
    Total = []
    Adding = []
    Avoid = []
    t = 0
    Findex = 0
    index = []
    for i in AuthorsList:
        for j in AuthorsList:
            if j not in Avoid:
                if i == j:
                    index.append(Findex)
            Findex += 1
        Adding.append(i)
        Avoid.append(i)
        for k in index:
            t += ViewsArticle[k]
        Adding.append(t)
        Findex = 0
        t = 0
        index = []
        Total.append(Adding)
        Adding = []

    # convert the insider list to tuple.
    Total = [tuple(i) for i in Total]
    # Order it from large to small viewers.
    Total = sorted(Total, key=itemgetter(1), reverse=True)
    # The Total result has the answer for question 2. ready to print it.

    # start to answer the third question.
    query = """select *
    from AllAccess join AccessError on AllAccess.date = AccessError.date; """
    c.execute(query)
    AllStat = c.fetchall()

    # filter the table to meet the desired result.
    HighRate = []
    add = []
    for i in AllStat:
        ErrorRequest = i[3] / i[1] * 100 # calculate the error rate.
        if ErrorRequest > 1.0:
            add.append(i[0])
            add.append(ErrorRequest)
            HighRate.append(add)
        add = []
    # The HighRate result has the answer for question 3. ready to print it.

    # sending each result to display it.
    display(Top3,Total,HighRate)
    db.close()

main()
