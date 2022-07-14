from bs4 import BeautifulSoup
from re import sub
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PRODUCT_URL = "https://goldapple.ru/makijazh"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0"
}
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(PRODUCT_URL)

driver.set_window_size(1920, 1080)
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(4)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")
categories = soup.find_all("div", class_="product-item-category-title")
brand_names = soup.find_all("span", class_="catalog-brand-name-span")
product_names = soup.find_all("span", class_="catalog-product-name-span")
prices = soup.find_all("span", class_="price")

driver.close()
driver.quit()

Base = declarative_base()


class Price(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    brand_name = Column(String(64))
    product_name = Column(String(64))
    price = Column(String(16))
    price_int = Column(Numeric(10, 2))
    update_date = Column(DateTime)


engine = create_engine("sqlite:///goldapple.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)


def add_product(category, brand_name, product_name, price, price_int):
    is_exist = session.query(Price).filter(Price.product_name == product_name).all()
    if not is_exist:
        session.add(
            Price(
                category=category,
                brand_name=brand_name,
                product_name=product_name,
                price=price,
                price_int=price_int,
                update_date=datetime.now()
            )
        )
        session.commit()


for item in range(0, len(product_names)):
    add_product(categories[item].get_text().strip(),
                brand_names[item].get_text(),
                product_names[item].get_text(),
                prices[item].get_text(),
                int(sub("[^0-9]", "", prices[item].get_text()))
                )
