#INSTALACION LIBRERIAS
!pip install selenium
!pip install BeautifulSoup4
!pip install pandas

#IMPORTACION DE LIBRERIAS
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

#DEFINICION DE CHROMEDRIVER
driver = webdriver.Chrome(executable_path=r'C:/chromedriver_win32/chromedriver.exe')

#DEFINICION DE ARREGLOS Y URL PARA WEBSCRAPPING
company=[]
area=[]
description=[]
address=[]
region=[]
driver.get('https://www.edina.com.ec/Buscador?b=empresas&c=ecuador&pagina=1')

#OBTENEMOS EL CODIGO FUENTE DE LA VISTA
content = driver.page_source

#ALMACENAMOS LA ESTRUCTURA HTML
soup = BeautifulSoup(content)

#VISUALIZAMOS EL CODIGO FUENTE
print(content)

#ALMACENAMOS LOS DIFERENTES DATOS QUE NOS PROPORCIONA LA PAGINA
for a in soup.findAll('div', attrs={'class':'place-post__content'}):
    companyName=a.find('a',href=True, attrs={'itemprop':'name'})
    areaCompany=a.find('p',attrs={'class':'place-post__description'})
    descriptionCompany=a.find('p',attrs={'itemprop':'streetAddress'})
    addressCompany=a.find('span',attrs={'itemprop':'addressLocality'})
    regionCompany=a.find('span',attrs={'itemprop':'addressRegion'})
    
    company.append(companyName.text)
    area.append(areaCompany.text)
    description.append(descriptionCompany.text) 
    address.append(addressCompany.text)
    region.append(regionCompany.text)
    
#ALMACENAMOS EN UN DATAFRAME LOS DATOS RECOLECTADOS
df = pd.DataFrame({'Company':company,'Description':description,'Area':area,'Region':region,'Address':address})

#IMPRIMIMOS EL DATAFRAME
print(df)

#DEFINIMOS UNA FUNCION PARA LIMPIAR LOS ESPACIOS EN EL DATAFRAME
def trim_all_columns(df):
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)
    
#LIMPIAMOS LOS ESPACIOS EN EL DATAFRAME
df = trim_all_columns(df)

#REMOVEMOS COMILLAS Y COMAS DE LAS COLUMNAS DEL DATAFRAME
df["Company"].replace({',': ' ','"':' '}, inplace=True)
df["Description"].replace({',': ' ','"':' '}, inplace=True)
df["Area"].replace({',': ' ','"':' '}, inplace=True)
df["Region"].replace({',': ' ','"':' '}, inplace=True)
df["Address"].replace({',': ' ','"':' '}, inplace=True)

#IMPRIMIMOS EL DATAFRAME
print(df)

#ALMACENAMOS EL DATAFRAME EN UN CSV
df.to_csv('Company.csv', index=False, encoding='utf-8')
