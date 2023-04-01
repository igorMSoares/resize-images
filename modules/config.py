import json

class Config:
  @classmethod
  def default_args(cls):
    with open("./config.json", "r") as config_file:
        return json.load(config_file)["default_args"];
