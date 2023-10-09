## kanw import kapoies vivliothikes kathws kai to app mou

from flask import render_template,request,jsonify,json
import sqlite3
from myproject import app

## dimiourgw mia sunartisi stin opoia kanw connect tin database mou kai diavazw tis grammes
## kai kanw return to conn wste na to xrisimopoiw ousiastika tin database mou stis upoloipes methodous

def get_db_connection():  
    conn = sqlite3.connect('project.db')
    with conn:
        conn.row_factory = sqlite3.Row       
    return conn


##dimiourgw ta routes mou
@app.route('/')

@app.route('/home')
def homepage():
    return render_template('homepage.html',title='Home Page')
    
## se auto to route exw ton pinaka me tis plirofories sugkekrimena sto 'Greek Hospitals'
@app.route('/secondpage')
def secondpage():
    conn = get_db_connection()
    wantedTable = conn.execute('SELECT * FROM Data').fetchall()
    return render_template('secondpage.html',title = 'Second Page',wantedTable=wantedTable)

## auto to route einai to 'Searching For Hospitals' opou xrisimopoiw kai tis 2 methodous GET kai Post

## stin periptwsi tis get stelnw ta dedomena mou stin selida wste na ta apotipwsw sta select options mou
## kai stin periptwsi tis POST diladi molis patithei to koubi submit lamvanw ta dedomena sumfwna me ta select options
## kai ektelw mia epeksergasia mesw tis database kai sto telos krataw ta dedomena pou thelw na steilw pisw
## pio sugkekrimena to onoma twn nosokomeiwn,tis x kai y suntetagkemes,tin dieuthinsi kai to tilefwno


@app.route('/thirdpage',methods = ['GET','POST'])
def thirdpage():
    conn = get_db_connection()
    cur = conn.cursor()
    ##periptwsi GET
    if request.method == 'GET':
    
        ##edw vazw ta dedomena gia ta select <to ti tha fainetai sta options>
        beds = conn.execute('SELECT DISTINCT H_beds FROM Data ORDER BY H_beds').fetchall()
        regions =conn.execute('SELECT DISTINCT H_region FROM Data ORDER BY H_region').fetchall()
        categories = conn.execute('SELECT DISTINCT H_category FROM Data ORDER BY H_category').fetchall()
        
        conn.close()
        ##stelnw ta dedomena gia na diatupwthoun
        return render_template('thirdpage.html',title = 'Third Page', beds=beds,regions=regions,categories=categories)
    ##periptwsi POST
    else:
        ##lamvanw ta dedomena pou einai se JSON morfi kai ta apothikeuw se 3 diaforetikes metavlites gia na ta aksiopoiisw
        mydict = request.get_json()
        result = json.loads(mydict)
        region = result.get("regionval")
        category = result.get("categoryval")
        bed = result.get("bedsval")

        ## xrisimopoiw kapoia if statements gia oles tis periptwseis pou borei na ginoun sta select options
        ##kai apothikeuw ta apotelesmata sto filteredAxis
        if(region == "Select Region" and category == "Select Category"):
            filteredAxis = cur.execute('SELECT H_name,H_xaxis,H_yaxis,H_address,H_phone FROM Data WHERE H_beds = ?',(bed,)).fetchall()
        elif(region == "Select Region" and bed == "Select Number of Beds"):
            filteredAxis = cur.execute('SELECT H_name,H_xaxis,H_yaxis,H_address,H_phone FROM Data WHERE H_category = ?',(category,)).fetchall()
        elif(category == "Select Category" and bed == "Select Number of Beds"):
            filteredAxis = cur.execute('SELECT H_name,H_xaxis,H_yaxis,H_address,H_phone FROM Data WHERE H_region = ?',(region,)).fetchall()
        elif(category == "Select Category"):
            filteredAxis = cur.execute('SELECT H_name,H_xaxis,H_yaxis,H_address,H_phone FROM Data WHERE H_region = ? AND H_beds = ?',(region,bed)).fetchall()
        elif(region == "Select Region"):
            filteredAxis = cur.execute('SELECT H_name,H_xaxis,H_yaxis,H_address,H_phone FROM Data WHERE H_category = ? AND H_beds = ?',(category,bed)).fetchall()
        elif(bed == "Select Number of Beds"):
            filteredAxis = cur.execute('SELECT H_name,H_xaxis,H_yaxis,H_address,H_phone FROM Data WHERE H_category = ? AND H_region = ?',(category,region)).fetchall()
        else:
            filteredAxis = cur.execute('SELECT H_name,H_xaxis,H_yaxis,H_address,H_phone FROM Data WHERE H_category = ? AND H_region = ? AND H_beds = ?',(category,region,bed)).fetchall()

        counter = 0
        
        dictionary = {}
        dictionary3 = {}

        ## gia kathe row mesa sto filteredAxis prosthetw mesa sto dictionary ta dedomena pou thelw na steilw pisw
        for row in filteredAxis:
            
            counter = counter +1
            dictionary[counter] = {}
            dictionary[counter]['hospital'] = row['H_name']
            dictionary[counter]['y'] = row['H_yaxis']
            dictionary[counter]['x'] = row['H_xaxis']
            dictionary[counter]['address'] = row['H_address']
            dictionary[counter]['phone'] = row['H_phone']

            ##kai ta vazw mesa se ena allo dictionary wste na exei tin JSON morfi kai na boresw na ta steilw 

            dictionary3[counter] = dictionary[counter]

       

        conn.close()
        return jsonify(dictionary3)

@app.route('/fourthpage',methods = ['GET','POST'])
def fourthpage():
    
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'GET':
        ##edw vazw ta dedomena gia ta select <to ti tha fainetai sta options>
        regions =conn.execute('SELECT DISTINCT H_region FROM Data ORDER BY H_region').fetchall()
        conn.close()
        ##stelnw ta dedomena gia na diatupwthoun
        return render_template('fourthpage.html',title = 'Fourth Page',regions=regions)
    ##periptwsi POST
    
    else:
        myregion = request.get_json()
        result = json.loads(myregion)
        region = result.get("regionval")
        
        ratingAxis = cur.execute('SELECT H_name,H_xaxis,H_yaxis,H_address,H_phone FROM Data WHERE H_region = ?',(region,)).fetchall()
        ratingCounter = 0
        
        dictionary = {}
        dictionary3 = {}

        ## gia kathe row mesa sto filteredAxis prosthetw mesa sto dictionary ta dedomena pou thelw na steilw pisw
        for row in ratingAxis:
            
            ratingCounter = ratingCounter +1
            dictionary[ratingCounter] = {}
            dictionary[ratingCounter]['hospital'] = row['H_name']
            dictionary[ratingCounter]['y'] = row['H_yaxis']
            dictionary[ratingCounter]['x'] = row['H_xaxis']
            dictionary[ratingCounter]['address'] = row['H_address']
            dictionary[ratingCounter]['phone'] = row['H_phone']

            ##kai ta vazw mesa se ena allo dictionary wste na exei tin JSON morfi kai na boresw na ta steilw 

            dictionary3[ratingCounter] = dictionary[ratingCounter]
        conn.close()
        return jsonify(dictionary3)


## xrisimopoiw auto to route wste na steilw dedomena apo to fourthpage mou me post  request
## kai xrisimopoiwntas ena akoma table mesa stin vasi mou prosthetw mesa dedomena pou 
##exw parei apo tin post 
##stin poreia diavazw auto to table kai upologizw ton meso oro twn asteriwn tou sugkekrimenou
## nosokomeiou kai mazi me to pio prosfato sxolio ta stelnw ksana me jsonify sto fourthpage


@app.route('/ratingpage',methods = ['POST','GET'])
def rating():

    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        
        mydict = request.get_json()
        result = json.loads(mydict)
        
        x = result.get('markerLng')
        y = result.get('markerLat')
        comments = result.get('txt')
        star = result.get('currentStar')
        dict1 = {}

        data_tupple = (y,x,star,comments)

        ratingsQuery = "INSERT INTO RatingData (R_H_yaxis,R_H_xaxis,R_rating,R_comments) VALUES (?,?,?,?)"



        cur.execute(ratingsQuery,data_tupple)

        avgQuery = cur.execute("SELECT AVG(R_rating) FROM RatingData WHERE R_H_yaxis = ? AND R_H_xaxis = ?",(y,x)).fetchall()
        countrating = cur.execute("SELECT COUNT(R_rating) FROM RatingData WHERE R_H_yaxis = ? AND R_H_xaxis = ?",(y,x)).fetchall()
        commentsQuery = cur.execute("SELECT R_comments FROM RatingData WHERE R_H_yaxis = ? AND R_H_xaxis = ? ORDER BY R_id DESC LIMIT 1",(y,x)).fetchall()

        conn.commit()
        conn.close()

        

        for rows2 in countrating:
            dict1['count'] = rows2[0]

        for rows in commentsQuery:
            dict1['comment'] = rows[0]
        
        for row in avgQuery:
            dict1['avg'] = row[0]
            
        
        #print(dict1)
        return jsonify(dict1)

@app.route('/scrapingpage',methods=['GET','POST'])
def scrapingpage():
    conn = get_db_connection()
    cur = conn.cursor()
    ##periptwsi GET
    if request.method == 'GET':
    
        ##edw vazw ta dedomena gia ta select <to ti tha fainetai sta options>
        localities = conn.execute('SELECT DISTINCT S_locality FROM ScrapData ORDER BY S_locality').fetchall()
        regions =conn.execute('SELECT DISTINCT S_region FROM ScrapData ORDER BY S_region').fetchall()
        
        
        conn.close()
        ##stelnw ta dedomena gia na diatupwthoun
        return render_template('scrapingpage.html', title = 'Scraping Page',localities=localities,regions=regions)
    ##periptwsi POST
    else:
        ##lamvanw ta dedomena pou einai se JSON morfi kai ta apothikeuw se 3 diaforetikes metavlites gia na ta aksiopoiisw
        mydict = request.get_json()
        result = json.loads(mydict)
        region = result.get("regionval")
        locality = result.get("localityval")
        

        ## xrisimopoiw kapoia if statements gia oles tis periptwseis pou borei na ginoun sta select options
        ##kai apothikeuw ta apotelesmata sto filteredAxis
        if(region == "Select Region"):
            scrapAxis = cur.execute('SELECT S_name,S_address,S_activities,S_yaxis,S_xaxis,S_phone,S_website FROM ScrapData WHERE S_locality = ?',(locality,)).fetchall()
        elif(locality == "Select Locality"):
            scrapAxis = cur.execute('SELECT S_name,S_address,S_activities,S_yaxis,S_xaxis,S_phone,S_website FROM ScrapData WHERE S_region = ?',(region,)).fetchall()
        else:
            scrapAxis = cur.execute('SELECT S_name,S_address,S_activities,S_yaxis,S_xaxis,S_phone,S_website FROM ScrapData WHERE S_region = ? AND S_locality = ?',(region,locality)).fetchall()
        

        counter = 0
        
        dictionary = {}
        dictionary3 = {}

        ## gia kathe row mesa sto filteredAxis prosthetw mesa sto dictionary ta dedomena pou thelw na steilw pisw
        for row in scrapAxis:
            
            counter = counter +1
            dictionary[counter] = {}
            dictionary[counter]['diagnostic'] = row['S_name']
            dictionary[counter]['address'] = row['S_address']
            dictionary[counter]['activities'] = row['S_activities']
            dictionary[counter]['y'] = row['S_yaxis']
            dictionary[counter]['x'] = row['S_xaxis']
            dictionary[counter]['phone'] = row['S_phone']
            dictionary[counter]['website'] = row['S_website']
            

            ##kai ta vazw mesa se ena allo dictionary wste na exei tin JSON morfi kai na boresw na ta steilw 

            dictionary3[counter] = dictionary[counter]

        

        conn.close()
        return jsonify(dictionary3)
    