#import requests
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import os
#from selenium.webdriver.firefox.options import Options
#from selenium.common.exceptions import NoSuchElementException

def read_url(url):

    chrome_options = webdriver.ChromeOptions()

    #iniciar sessão de browser 
    #driver = webdriver.Chrome("C:/Meu/chatbot/fakenews-api-py") 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    #url = 'https://www.cartacapital.com.br/cartaexpressa/parana-pesquisas-em-minas-lula-lidera-com-41-bolsonaro-tem-33-e-ciro-fica-com-6/?utm_source=terra_capa_noticias&utm_medium=referral'
    driver.get(url)

    #obter o título
    title = driver.title

    #obter a notícia (apenas os dois paragrafos com len > 150 caracteres)
    elements = driver.find_elements(By.TAG_NAME, 'p')
    #obter os primeiros 3 paragrafos da notícia
    num = 0
    body = ""
    for e in elements:
        if(len(e.text)>150):
            body += e.text
            num+=1
        if num >2:
            break

    #procurar o autor. Normalmente tem a palavra "autor" na class da tag. Como é case sensitivo, usa-se "utor" na pesquisa
    autors = driver.find_elements(By.XPATH, "//*[contains(@class,'uthor')]")
    autor_txt = ""
    autor = ""
    for e in autors:
        if (len(e.text)>0):
            autor_txt = e.text
            autor = autor_txt.replace('por ', '').replace('Por ', '')
            p = re.search("\n", autor)
            if int(0 if p is None else p.start()) > 0:
                autor = autor[0:p.start()]
            break

    #obter a data da noticia. Muitas vezes vem no texto junto ao autor, outras vezes vem à parte e aí pesquisa-se por "date" na class
    dt = ""
    p=re.search(r"\d{2}[\/.-]\d{2}[\/.-]\d{4}", autor_txt)

    #verificar se encontra uma data no nome de autor com formato dd-mm-aaaa
    if int(0 if p is None else p.start()) > 0:
        dt = autor_txt[p.start():p.start()+10]
    elif (dt == ""):
        p=re.search(r"\d{4}[\/.-]\d{2}[\/.-]\d{2}", autor_txt)
        #verificar se encontra uma data no nome de autor com formato aaaa-mm-dd
        if int(0 if p is None else p.start()) > 0:
            dt = autor_txt[p.start():p.start()+10]
        else:
            #procurar uma tag com data
            data = driver.find_elements(By.XPATH, "//*[contains(@class,'date')]")
            for e in data:
                if(len(e.text)>0):
                    dt = e.text
                    break

    print ("titulo:", title)
    print ('autor:', autor)
    print ('data:', dt)
    print ('notícia:', body)

    driver.quit()
    return title, autor, dt, body