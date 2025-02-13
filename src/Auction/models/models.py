import abc

from Auction.dao.mongoDAO import MongoDao


class Model(abc.ABC):
    def __init__(self, model_id):
        self.id = model_id

    def to_dict(self):
        raise NotImplementedError

    @staticmethod
    def from_dict(data):
        raise NotImplementedError

    def create(self, dao: MongoDao):
        raise NotImplementedError

    @staticmethod
    def filter(query: dict, dao: MongoDao):
        raise NotImplementedError

    def update(self, dao: MongoDao):
        raise NotImplementedError

    def delete(self, dao: MongoDao):
        raise NotImplementedError
