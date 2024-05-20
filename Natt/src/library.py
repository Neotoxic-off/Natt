import os

class Library:
    def __init__(self, path: str):
        self.path: str = path
        self.collection: list[str] = []

        self.__build__()

    def __build__(self):
        self.collection = os.listdir(self.path)
