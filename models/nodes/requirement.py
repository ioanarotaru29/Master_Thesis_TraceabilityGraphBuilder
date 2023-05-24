class Requirement:
    def __init__(self, location, name, description):
        self.location = location
        self.name = name
        self.sentences = description.split('\n')