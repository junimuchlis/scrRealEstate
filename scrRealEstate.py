# Importing the libraries
import requests
from bs4 import BeautifulSoup

#url = 'http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/'
req = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})


content = req.content
# print(content)
soup = BeautifulSoup(content,'html.parser')

#Extract all data
data = soup.find_all("div",{"class":"propertyRow"})
#print(data)

#extract price
data[0].find("h4",{"class":"propPrice"}).text
data[0].find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")

# retrieve page numbers in websites

page_num= soup.find_all("a",{"class":"Page"})[-1].text
#print(page_num)
#print(type(page_num))


l=[]

# Crawling all the webpages containing data

base_url= "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

for page in range(0,int(page_num)*10,10):
    print(base_url+str(page)+".html")
    req = requests.get(base_url+str(page)+".html",headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    content = req.content
    soup= BeautifulSoup(content,"html.parser")
    all= soup.find_all("div",{"class":"propertyRow"})

    
    # List the prices,address and other details from the webpage
    # We are creating a list of dictionaries containing property attributes in order to decrease time

    for item in all:
        d= {}
        
        d["Address"]= item.find_all("span",{"class":"propAddressCollapse"})[0].text
        
        try:
            d["Locality"]= item.find_all("span",{"class":"propAddressCollapse"})[1].text
            
        except:
            d["Locality"]= None
        
        d["Price"]= item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")

        try:
            d["Beds"]= item.find("span",{"class":"infoBed"}).find("b").text

        except:          # For attributes of type "None"
            d["Beds"]= None

        try:
            d["Area"]= item.find("span",{"class":"infoSqFt"}).find("b").text

        except:          # For attributes of type "None"
            d["Area"]= None

        try:
            d["Full Baths"]= item.find("span",{"class":"infoValueFullBath"}).find("b").text

        except:          # For attributes of type "None"
            d["Full Baths"]= None

        try:
            d["Half Baths"]= item.find("span",{"class":"infoValueHalfBath"}).find("b").text

        except:          # For attributes of type "None"
            d["Half Baths"]= None

        for column_group in item.find_all("div",{"class":"columnGroup"}):
            #print(column_group)
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}), column_group.find_all("span",{"class":"featureName"})):
                #print(feature_group.text, feature_name.text)
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]= feature_name.text

        l.append(d)

# Converting the list of dictionaries (l) into a pandas' dataframe (df)

import pandas as pd
df= pd.DataFrame(l)
#print(df)

# export the dataframe into a csv file

df.to_csv("results/Output_realEstate.csv")



