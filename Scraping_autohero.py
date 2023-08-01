from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# User agent
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

)


""" DRIVER, ABRIR PÁGINA WEB """

driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
driver.get('https://www.autohero.com/es/search/?sort=distance_asc&yearMin=2011&yearMax=2023&mileageMax=125000') #filtro kms y años y ordenado asc kms
# solo hay 1800 coches con filtros en esta pagina.

# Esperamos unos segundos para que se cargue por completo y ahorramos problemas
sleep(random.uniform(1.0, 5.0))


"""DENTRO DE PÁGINA WEB PRINCIPAL"""

try: # Encerramos todo en un try para que si no aparece el discilamer, no se caiga el codigo
  cookies = driver.find_element(By.XPATH, '//button[@class="button___2R6qU size-sm___3TKQS default___1FRAY"]')
  cookies.click() # lo obtenemos y le damos click
except Exception as e:
  print ("error en cookies, el error es: ", e)
  None

sleep(random.uniform(1, 3))


"""COMO EXISTE HTML DINÁMICO, PARA CARGAR LOS COCHES HAY QUE HACER SCROLLING, POR LO QUE VAMOS A IR OBTENIENDO LOS COCHES 
CARGADOS Y HACIENDO SCROLLING Y ASI SUCESIVAMENTE. PARA ELLO VAMOS A DEFINIR DOS FUNCIONES (OBTENER LINKS Y SCROLLING)"""

lista_urls = []

def sacar_links_coches_autohero(): # con esta funcion metemos en una lista los links de los coches que estan cargados en body
    # vamos a dormir el driver hasta que este cargado por completo la info que queremos:
    sacar_links = driver.find_elements(By.XPATH, '//a[@data-qa-selector="ad-card-link"]')

    for tag in sacar_links:
        global lista_urls
        lista_urls.append(tag.get_attribute('href'))


def scroll_autohero(): # hacemos scroll a la página, hasta el final y cargamos otros cuantos coches sin perder ninguno por el camino,
                        # no antes sin dormir a la funcion para no ser detectados como bot.
    sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(random.uniform(1, 5))




""" UNA VEZ TENEMOS LAS FUNCIONES DE NUESTROS MECANISMOS PARA SCRAPEAR LOS LINKS DE LOS COCHES, CREAMOS LA LISTA: """
""" PERO HASTA CUANDO VAMOS A IR LLENANDO LA LISTA? VEAMOS """

while len(lista_urls) < 1000:
    sacar_links_coches_autohero()
    scroll_autohero()


############### COMPROBAR QUE LISTA ES CORRECTA ####################
# print(lista_urls)
print(len(lista_urls))
# for i in range(0,100):
#     for j in range(0,100):
#         if i != j:
#             if lista_urls[i] == lista_urls[j]:
#                 print(i, "----", j)








""" UNA VEZ QUE TENEMOS LA LISTA DE URLS DE LOS COCHES, VAMOS A IR OBTENIENDO LA INFORMACION EN CADA UNO DE SUS DETALLES, URLS """
""" COMO LA CARGA DE HTML DE CADA URL, ES DINAMICA PERO LA CARGA PREVIA MUESTRA LA INFORMACION QUE NECESITAMOS, VAMOS A USAR SCRAPY """


""" -------------------- SCRAPY VERTICAL DETALLES CADA COCHE -------------------- """

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup



""" PARA CADA URL CON BUCLE: """

# no hay bucle, le metemos la lista en start url

""" CARGADOR DE ITEM """

class coche(Item): #ESTO ES PARA DARSELO LUEGO AL CARGADOR DE ITEMS
    Marca = Field()
    Modelo = Field()
    Version = Field()
    Precio = Field()
    Combustible = Field()
    Año = Field()
    Kms = Field()
    Potencia = Field()
    Puertas = Field()
    Cambio = Field()
    Color = Field()


""" CRAWLER, SPIDER MOVIENDOSE POR DIFERENTES SITIOS """

class autohero(Spider): # CLASE CORE - SPIDER   LA QUE SE VA A MOVER Y BUSCAR LA INFORMACIÓN.
    name = "cochessegundamanoautohero"  # nombre, puede ser cualquiera

    # Forma de configurar el USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'FEED_EXPORT_FIELDS': ['Marca', 'Modelo', 'Version', 'Precio', 'Combustible', 'Año', 'Kms', 'Potencia', 'Puertas', 'Cambio', 'Color'],
        'CONCURRENT_REQUESTS': 1  # numero de requerimientos concurrentes
    }

    # URL SEMILLA (por cada url de cada coche) aqui le metemos nuestra lista de urls que obtuvimos en el primer paso.
    start_urls = lista_urls[0:500]

    """ DEFINIMOS FUNCION DENTRO DE FUNCION SPIDER, ESTA ES EL PARSEADOR QUE VA A RELLENAR LOS ITEM QUE BUSCAMOS """

    # Funcion que se va a llamar cuando se haga el requerimiento a la URL semilla
    def parse(self, response): # self porque es una funcion dentro de otra funcion, self hace referencia a parametro anterior.
        sel = Selector(response)
        item = ItemLoader(coche(), sel ) # cargador de items

        """ RELLENAMOS LOS ITEMS """

        item.add_xpath('Marca', '//h1[contains(@class, "vehicleContainerTitle___oJOal")]/text()')
        item.add_xpath('Modelo', '//h1[contains(@class, "vehicleContainerTitle___oJOal")]/text()')
        item.add_xpath('Version', '//span[@class="subtitleText___1yQKH"]/text()')
        item.add_xpath('Precio', '//p[@data-qa-selector="vehicle-info-price"]/text()')
        item.add_xpath('Combustible', '//div[@class="list___1nOdk"]/div[@data-qa-selector="motor-info-element-undefined"]//span[@class="listItemValue___1IWSE"]/text()')
        item.add_xpath('Año', '//div[@class="list___1nOdk"]/div[@data-qa-selector="motor-info-element-builtYear"]//span[@class="listItemValue___1IWSE"]/text()')
        item.add_xpath('Kms', '//div[@class="list___1nOdk"]/div[@data-qa-selector="motor-info-element-mileage"]//span/text()')
        item.add_xpath('Potencia', '//div[@class="list___1nOdk"]/div[@data-qa-selector="motor-info-element-power"]//span/text()')
        item.add_xpath('Puertas', '//div[@data-qa-selector="feature-section-item-doorCount-body"]/text()')
        item.add_xpath('Cambio', '//div[@class="list___1nOdk"]/div[@data-qa-selector="motor-info-element-gearType"]//span/text()')
        item.add_xpath('Color', '//div[@data-qa-selector="feature-section-item-color-body"]/text()')


        yield item.load_item()


""" EJECUCION CON TERMINAL """

# # scrapy runspider Scraping_autohero.py -o CSV_Scraping_autohero4.csv -t csv












