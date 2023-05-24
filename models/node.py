class Node:
    def __init__(self, file_type, location, name, sentences=None, code_sentences=None):
        if code_sentences is None:
            code_sentences = []
        if sentences is None:
            sentences = []
        self.type = file_type
        self.location = location
        self.name = name
        self.sentences = sentences
        self.code_sentences = code_sentences
