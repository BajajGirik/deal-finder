from typing import List, Optional, TypedDict
from pymongo.collection import Collection
from bson import ObjectId

class ProductTrackerModel(TypedDict):
    _id: ObjectId
    # This is a custom name provided by the user.
    # Should be unique
    name: str
    # Keeping this as an array as users might wanna track prices from multiple websites
    # We will only be supporting amazon links only (Planning to support flipkart links in future)
    url: List[str]
    # price below which a notification will be sent to the user via the channel_id
    price_threshold: float
    # This will be the discord's channel id where the updates would be posted
    channel_id: str
    # The user id who requested tracking the product
    user_id: str


class ProductTrackerService:
    def __init__(self, collection: Collection[ProductTrackerModel]) -> None:
        self.__collection = collection

    def findById(self, id: str) -> Optional[ProductTrackerModel]:
        doc = self.__collection.find_one({ "_id": ObjectId(id) })
        return doc

    def findByUserId(self, userId: str) -> List[ProductTrackerModel]:
        docs = list(self.__collection.find({ "user_id": userId }))
        return docs

    def findByNameForUser(self, name: str, userId: str) -> Optional[ProductTrackerModel]:
        doc = self.__collection.find_one({ "name": name, "user_id": userId })
        return doc
