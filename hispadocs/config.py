import yaml


class Config(dict):
    def __init__(self, path):
        self.file = path
        super(Config, self).__init__()

    def read(self):
        self.update(yaml.load(open(self.file), yaml.Loader))
