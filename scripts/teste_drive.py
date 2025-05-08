from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

edge_path = 'C:/GitHub/Automatizador/msedgedriver.exe'

options = Options()
options.use_chromium = True

service = Service(edge_path)
driver = webdriver.Edge(service=service, options=options)
driver.get("https://www.google.com")
