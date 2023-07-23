import os
from dotenv import load_dotenv
from pymongo import MongoClient
from database.productTracker import ProductTrackerService

load_dotenv()

class Database:
    def __init__(self) -> None:
       databaseURL = os.getenv('DATABASE_URL')

       if not databaseURL:
           # TODO: Notify via email
           print("DATABASE_URL not provided")

       self.__client = MongoClient(databaseURL)
       self.__database = self.__client['deals']

       self.productTracker = ProductTrackerService(self.__database['product-tracker'])
