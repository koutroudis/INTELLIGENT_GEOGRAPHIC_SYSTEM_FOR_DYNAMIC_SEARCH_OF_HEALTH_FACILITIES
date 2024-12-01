
from faulthandler import disable
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from selenium.webdriver.chrome.options import Options


def scrap():


    with open('scraping.csv','w') as file:
        file.write("Name,Address,Locality,Region,Activities,yaxis,xaxis,phone,website\n")


    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches' , ['enable-logging'])


    driver = webdriver.Chrome('C:\Python310\Lib\site-packages\chromedriver.exe',options=options)
    driver.get('https://www.xo.gr/search/?what=medical+diagnostic+centres&lang=en')
    
    








    counter = 0

    for k in range(11):
        cords = []
        phoneslist = []
        weblist = []
        localitieslist = []
        addresseslist = []

        activitieslistfinal = []
        reglist = []
        nameslist = []
        phones = driver.find_elements_by_class_name('btn-toolbar')
        for phone in phones:
            try:
                ref = phone.find_element_by_xpath('.//div/a').get_attribute('href')
                phoneslist.append(ref)
            except:
                phoneslist.append('')
        counter = counter + len(phoneslist)
        
        
        websites = driver.find_elements_by_class_name('listingMainCallToActions')
        for website in websites:
            try:
                web = website.find_element_by_xpath('.//li/a').get_attribute('href')
                weblist.append(web)  
            except Exception:
                weblist.append('')
        

        

        coords = driver.find_elements_by_class_name('address')
        
        for coord in coords:
            try:
                coordinates = coord.find_element_by_xpath('.//span/a').get_attribute('onclick')
                split = coordinates.split()
            

                ##ycoordinate
                y1 = split[1]
                x1 = split[2]
                x2 = x1.split(',')
                x3 = x2[0]
                finalx = x3.replace("'",'')

                ##xcoordinate
                y2=y1.split('(')
                y3 = y2[1]
                y4 = y3.split(',')
                y5 = y4[0]
                finaly = y5.replace("'",'')
                
                cords.append([finaly,finalx])
            except Exception as ex:
                
                cords.append(['',''])
        
        
        

        addresses = driver.find_elements_by_class_name('listingAddressInfo')
        for address in addresses:
            try:
                
                add = address.find_element_by_xpath('.//span/span/span[@itemprop = "streetAddress"]')
                addresseslist.append(add.text)  
                
            except Exception:
                addresseslist.append('')

        
        localities = driver.find_elements_by_class_name('listingAddressInfo')
        for locality in localities:
            try:
                loc = locality.find_element_by_xpath('.//span/span/span[@itemprop = "addressLocality"]')
                localitieslist.append(loc.text)  
            except Exception:
                localitieslist.append('')
        

        activities = driver.find_elements_by_class_name('listingGreyArea')
        for activity in activities:
            activitieslist = []
            mystring = ''
            try:
                act = activity.find_element_by_xpath('.//ul').find_elements_by_tag_name('li')
                for a in act:
                    activitieslist.append(a.text) 
                for x in activitieslist:
                    mystring += '--' + x
                activitieslistfinal.append(mystring)
            except Exception:
                activitieslistfinal.append('')


        
        

        regions = driver.find_elements(By.XPATH,'//span[@itemprop="addressRegion"]')
        for region in regions:
            reglist.append(region.text)
        

        names = driver.find_elements(By.XPATH,'//h2/a/span[@itemprop="name"]')
        for name in names:
            nameslist.append(name.text)

        with open('scraping.csv','a') as file:
            

            for i in range(len(names)):
                file.write(nameslist[i] +';'+addresseslist[i]+';'+localitieslist[i]+';'+reglist[i]+';'+activitieslistfinal[i] +';'+cords[i][0] +';'+ cords[i][1]+
                ';'+ phoneslist[i]+';'+weblist[i]+'\n')
                
                

            try:
                cookies = driver.find_element(By.XPATH,'//*[@id="CookieGdprConsentBanner"]/div/div/div/button[1]').click()
                time.sleep(1)
            except:
                pass
            

            try:
                closead = driver.find_element(By.CSS_SELECTOR,'button[data-dismiss="adpremium-stickyfooter"]').click()
                time.sleep(1)
            except:
                pass
            

            try:
                
                next = driver.find_element_by_class_name('page_next').click()
                
                
            except:
                print('Done!')
                
            
            
            

            
        file.close()


