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


""" DRIVER, ABRIR PÁGINA WEB """


driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
driver.get('https://www.coches.net/segunda-mano/')


# Esperamos unos segundos para que se cargue por completo y ahorramos problemas
sleep(random.uniform(1.0, 5.0))


