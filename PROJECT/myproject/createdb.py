

## kanw import tin sqlite3 kathws kai to csv gia tis parakatw energies
import sqlite3
import csv

def create():

    #create my Database
    connection = sqlite3.connect('project.db')

    ##exw dimiourgisei ena schema se morfi sql to opoio einai to table mou kai edw to anoigw gia diavasma
    with open('schema.sql') as f:
        connection.executescript(f.read())


    #create a cursor
    conn = connection.cursor()


    #print('my database created')

    #open csv for reading only
    file = open('bookFinal.csv','r')

    #read the lines from my csv file diaxwrizomeno me comma
    grammes = csv.reader(file,delimiter = ',')
    #agnow tin prwti grammi tou csv pou einai oi onomasies twn columns mou
    next(grammes)

    #dimiourgw ena query pou kanw insert ta sugkekrimena dedomena apo to csv arxeio
    queryGrammes = "INSERT INTO Data (H_name,H_region,H_category,H_beds,H_yaxis,H_xaxis,H_address,H_phone) VALUES (?,?,?,?,?,?,?,?)"

    result = "SELECT * FROM Data"
    rows = conn.execute(result).fetchall()



    if(len(rows) < 139):
        #pass my datas into my table
        conn.executemany(queryGrammes,grammes)


   

    

    scrapfile = open('scraping.csv','r')
    scrapgrammes = csv.reader(scrapfile,delimiter=';')
    next(scrapgrammes)
    
    
    scrapquery = "INSERT OR IGNORE INTO ScrapData (S_name,S_address,S_locality,S_region,S_activities,S_yaxis,S_xaxis,S_phone,S_website) VALUES (?,?,?,?,?,?,?,?,?)"

    conn.executemany(scrapquery,scrapgrammes)

    scrapResult = 'SELECT * FROM ScrapData'
    scrapRows = conn.execute(scrapResult).fetchall()
    


    testquery = 'SELECT S_yaxis,S_xaxis,S_locality,S_region FROM ScrapData ORDER BY S_region'
    test2query = conn.execute(testquery).fetchall()
    

    test3query = "SELECT COUNT(S_name) FROM ScrapData"
    test4query = conn.execute(test3query).fetchall()
    


   

    #print(rows)  




    #for r in ratingRows:
    #   print(r)

    connection.commit()

    connection.close()

