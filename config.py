import yaml

def read():
    with open("config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print("An error occurred parsing config.yaml")
            print(exc)
