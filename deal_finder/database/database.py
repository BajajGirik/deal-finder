import os
from dotenv import load_dotenv
from pymongo import MongoClient
from database.product_tracker import ProductTrackerService
from constants import ERROR_NOTIFICATION_EMAIL_ADDRESSES
from notification.notification import Notification

load_dotenv()


class Database:
    def __init__(self) -> None:
        database_url = os.getenv("DATABASE_URL")
        database_name = os.getenv("DATABASE_NAME")

        if not database_url or not database_name:
            notification = Notification()

            message = "Missing environment variable(s): "
            if not database_url and not database_name:
                message += "DATABASE_URL and DATABASE_NAME\n"
            elif not database_url:
                message += "DATABASE_URL\n"
            else:
                message += "DATABASE_NAME\n"

            message += "Please check your .env file to resolve this error."

            notification.email.send_email(
                message, "Missing ENV", ERROR_NOTIFICATION_EMAIL_ADDRESSES
            )
            raise Exception("Missing ENV")

        self.__client = MongoClient(database_url)
        self.__database = self.__client[database_name]

        self.product_tracker = ProductTrackerService(self.__database["product_tracker"])
