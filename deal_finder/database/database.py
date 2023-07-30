import os
from dotenv import load_dotenv
from pymongo import MongoClient
from database.product_tracker import ProductTrackerService

load_dotenv()

class Database:
    def __init__(self) -> None:
       database_url = os.getenv('DATABASE_URL')

       if not database_url:
           # TODO: Notify via email
           print("DATABASE_URL not provided")

       self.__client = MongoClient(database_url)
       self.__database = self.__client['deals']

       self.product_tracker = ProductTrackerService(self.__database['product_tracker'])
