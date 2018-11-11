import psycopg2

def main():
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    anotherQ = True
    while anotherQ:
        print("1) What are the most popular three articles of all time? \n",
             "2) Who are the most popular article authors of all time? \n",
             "3) On which days did more than 1% of requests lead to errors?")
        Vnum = input("Chooes the question you wanna the database answer above by number: ")
        if Vnum == "1":
            c.execute("select path, count(path) as views from log where status = '200 OK' group by path order by views desc limit 3 offset 1;")
            TopThree = c.fetchall()
            for i in TopThree:
                articleName = i[0][9:]
                articleName = articleName.replace('-',' ')
                articleName = articleName.capitalize()
                print(articleName, "-" , i[1],"views")
        elif Vnum == "2":
            c.execute("select path, count(path) as views from log where status = '200 OK' group by path order by views desc limit 1 offset 1;")
            Mostarticle = c.fetchone()
            Mostarticles = Mostarticle[0][9:]
            Mostarticles = Mostarticles.replace('-',' ')
            Mostarticles = Mostarticles.capitalize()
            query = ("select authors.name, articles.title from articles,authors where authors.id = articles.author;")
            c.execute(query)
            fetch = c.fetchall()
            for quma in fetch:
                findQuma = quma[1].find(',')
                if quma[1][:findQuma] == Mostarticles:
                    print("The most popular article authors is",quma[0])
                    break;
        elif Vnum == "3":
            c.execute("select date(time) as date, count(status) as access from log group by date;")
            AllStat = c.fetchall()
            c.execute("select date(time) as date, count(status) as error from log where status != '200 OK' group by date;")
            AllError = c.fetchall()
            for i in AllStat:
                for j in AllError:
                    if i[0] == j[0]:
                        p = (j[1] / i[1]) * 100.0
                        if p >= 1:
                            print("in Date ", j[0], " The requests error was more than %1.")
        else:
            print("Ops! you Choose the wrong question (number) choose the right one.\n")
        if Vnum == "3" or Vnum == "1" or Vnum =="2":
            AnotherTry = input("Another Question? (Y\\N)")
            if AnotherTry == "N" or AnotherTry == "n":
                anotherQ = False
                db.close()

main()
print("Program Stopped, Thank you :)")
