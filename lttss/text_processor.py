from config import LTTSSConfig
import re
import nltk

class TextProcessor:

    def __init__(self, lang :str):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        self.tokenizer = nltk.data.load(f'tokenizers/punkt/{lang}.pickle')

    def process_into_tokens(self, text : str) -> list[str]:
        text = self.clean_white_spaces(text)
        tokens = self.tokenize(text)
        tokens = self.clean_tokens(tokens)
        return tokens
    
    def clean_tokens(self, tokens) -> list[str]:
        clean_tokens = []
        for token in tokens:
            clean_token = self.clean_token(token)
            if clean_token is not None:
                clean_tokens.append(clean_token)
        return clean_tokens

    def clean_token(self, token):
        token = re.sub(r'\n+', '\n', token)
        token = re.sub(r'"+', ',,', token) # this is here for pauses. Piper is bad at handling silences for quotes and ellipses.
        token = re.sub(r'\s+', ' ', token)
        token = re.sub(r'\.(\.*\s*)*\.', '...', token) 
        token = re.sub(r'\.\.\.', ',,', token) # this is here for pauses. Piper is bad at handling silences for quotes and ellipses.
        token = token.strip(' \'-')
        if token == '' or token == '.':
            return None
        else: 
            return token
    
    def tokenize(self, text):
        text = re.sub(r'\n+', '\n', text)
        paragraphs = text.split('\n')
        print("paragraphs", paragraphs)
        tokens = []
        for paragraph in paragraphs:
            tokens.extend(self.tokenizer.tokenize(paragraph))
        return tokens

    def clean_white_spaces(self, text):
        text = re.sub(r'\t+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s\n+\s', '\n', text)
        return text
    
    def clean_text(self, text):
        text = re.sub(r'\n+', '. ', text)
        text = re.sub(r'[!?]+', '. ', text)
        text = re.sub(r'"+', ',,', text) # this is here for pauses. Piper is bad at handling silences for quotes and ellipses.
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\.(\s*\n*\t*?,)*\s*\n*\t*', '. ', text)
        text = re.sub(r',+(\s*\n*\t*?,)*\s*\n*\t*', ', ', text)

        return text
