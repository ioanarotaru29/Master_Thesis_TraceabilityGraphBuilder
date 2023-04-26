import json
import re

import psutil
from stanfordcorenlp import StanfordCoreNLP


def transform(word):
    # Underline
    new_word = word.replace('_', ' ')
    # Camel Case
    if not new_word.isupper():
        new_word = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', new_word))
    return new_word.lower()


class TextSanitizer:
    CORE_NLP_PATH = '/Users/ioanarotaru/Desktop/Disertatie/Model/Utils/stanford-corenlp-4.5.4'
    PROPERTIES = {'annotators': 'tokenize,ssplit,pos,lemma',
                  'pipelineLanguage': 'en',
                  'outputFormat': 'json'}
    ALLOWED_PARTS_OF_SPEECH = [
        'VB',  # Verb, base form
        'VBD',  # Verb, past tense
        'VBG',  # Verb, gerund or present participle
        'VBN',  # Verb, past participle
        'VBP',  # Verb, non-3rd person singular present
        'VBZ',  # Verb, 3rd person singular present
        'VP',  # Verb Phrase
        'NN',  # Noun, singular or mass
        'NNS',  # Noun, plural
        'NNP',  # Proper noun, singular
        'NNPS',  # Proper noun, plural
        'NP'  # Noun Phrase
    ]

    def __init__(self):
        try:
            self.__nlp = StanfordCoreNLP(self.CORE_NLP_PATH)
        except psutil.AccessDenied:
            print('AccessDenied. Please try running as admin...')

    def sanitize(self, sentence, use_transform=True, use_entity_recognition=False):
        if self.__nlp is None:
            return None

        terms_to_be_used = sentence
        properties = self.PROPERTIES
        if use_transform:
            terms_to_be_used = list(map(lambda x: transform(x), sentence.split()))
            terms_to_be_used = ' '.join(terms_to_be_used)
        if use_entity_recognition:
            properties['annotators'] += ',ner'
        annotations = self.__nlp.annotate(terms_to_be_used, properties=properties)
        annotations = json.loads(annotations)

        sanitized_keywords = []
        terms_json = annotations.get('sentences') or []
        for term_json in terms_json:
            tokens = term_json['tokens']
            for token in tokens:
                if token['ner'] != 'O':
                    sanitized_keywords.append(token['ner'].lower())
                elif token['pos'] in self.ALLOWED_PARTS_OF_SPEECH:
                    sanitized_keywords.append(token['lemma'].lower())
        # print(set(sanitized_keywords))
        return sanitized_keywords
