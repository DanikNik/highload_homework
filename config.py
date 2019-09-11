import os


class Config:
    def __init__(self):
        self.config_data = {}

    def read_config(self):
        config_path = "/etc/httpd.conf"
        if os.environ.get("PY_NGINX_CONFIG_PATH") is not None:
            config_path = os.environ.get("PY_NGINX_CONFIG_PATH")

        with open(config_path, "r") as config_file:
            data = config_file.read()
            self.config_data = dict(map(lambda x: x.split(" "), data.strip("\n\r\t ").split("\n")))
