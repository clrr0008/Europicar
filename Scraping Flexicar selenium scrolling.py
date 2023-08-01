import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


# User agent
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")


""" SCROLLING """

#scrollingScript = """ document.getElementsByClassName('MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-3')[0].scroll(0, 20000) """


""" DRIVER, ABRIR PÁGINA WEB """


driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
driver.get('https://www.flexicar.es/segunda-mano/#/km_to/119000/year_from/2011/year_to/2023')

# Esperamos unos segundos para que se cargue por completo y ahorramos problemas
sleep(random.uniform(1.0, 5.0))


"""DENTRO DE PÁGINA WEB PRINCIPAL"""

try: # Encerramos todo en un try para que si no aparece el discilamer, no se caiga el codigo
  cookies = driver.find_element(By.XPATH, '//div[@id="boxWrapper"]//div[@class="MuiBox-root jss449 jss447"]')
  cookies.click() # lo obtenemos y le damos click
except Exception as e:
  print ("error en cookies, el error es: ", e)
  None


""" HACEMOS SCROLL PARA OBTENER MAS HTML"""

sleep(random.uniform(1.0, 5.0))
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


sleep(random.uniform(1.0, 5.0))


# SCROLLS = 0
# while (SCROLLS != 2): # Decido que voy a hacer 3 scrollings
#   driver.execute_script(scrollingScript) # Ejecuto el script para hacer scrolling del contenedor
#   sleep(random.uniform(3, 5)) # Entre cada scrolling espero un tiempo
#   SCROLLS += 1




























input("Esperando que no se cierre webdriver: ")



















