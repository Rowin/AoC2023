import yaml

class Config:
    def __init__(self):
        with open("config.yaml", "r") as config_file:
            config_variables = yaml.safe_load(config_file)

        self.session_id = config_variables['session_id']
        self.year = config_variables['year']


config = Config()
