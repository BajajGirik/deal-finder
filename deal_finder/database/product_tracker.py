from typing import List, Optional, TypedDict
from pymongo.collection import Collection
from bson import ObjectId

URLType = List[str]

class ProductTrackerModel(TypedDict):
    _id: ObjectId
    # This is a custom name provided by the user.
    # Should be unique
    name: str
    # Keeping this as an array as users might wanna track prices from multiple websites
    # We will only be supporting amazon links only (Planning to support flipkart links in future)
    url: URLType
    # price below which a notification will be sent to the user via the channel_id
    price_threshold: float
    # This will be the discord's channel id where the updates would be posted
    channel_id: str
    # The user id who requested tracking the product
    user_id: str


class ProductTrackerService:
    def __init__(self, collection: Collection[ProductTrackerModel]) -> None:
        self.__collection = collection

    def find_all(self) -> List[ProductTrackerModel]:
        docs = list(self.__collection.find({}))
        return docs

    def find_by_id(self, id: str) -> Optional[ProductTrackerModel]:
        doc = self.__collection.find_one({ "_id": ObjectId(id) })
        return doc

    def find_by_user_id(self, user_id: str) -> List[ProductTrackerModel]:
        docs = list(self.__collection.find({ "user_id": user_id }))
        return docs

    def find_by_name(self, name: str, user_id: str) -> Optional[ProductTrackerModel]:
        doc = self.__collection.find_one({ "name": name, "user_id": user_id })
        return doc

    def insert(self, name: str, price_threshold: float, url: URLType, user_id: str, channel_id: str) -> str:
        # TODO: Find another way to construct object without passing "_id"
        # If we don't supply "_id", the typing breaks and compiler complains
        payload = ProductTrackerModel(_id=ObjectId(), name=name, price_threshold=price_threshold, url=url, channel_id=channel_id, user_id=user_id)
        result = self.__collection.insert_one(payload)
        return str(result.inserted_id)

    def delete_by_id(self, id: str) -> bool:
        res = self.__collection.delete_one({ "_id": ObjectId(id) })
        return res.deleted_count > 0
