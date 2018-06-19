import json

class __Secrets(object):
    def __init__(self):
        try:
            with open('secrets.json', 'r') as file:
                self.secrets = json.loads(file.read())
        except FileNotFoundError:
            raise FileNotFoundError('Decrypt the secrets.ejson file before using!')

    def __getitem__(self, key):
        return self.secrets[key]

secrets = __Secrets()
