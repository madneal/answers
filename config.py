import yaml

config_file = 'config/config.yaml'


def load_config():
    with open(config_file, 'r', encoding='utf8') as f:
        config = yaml.load(f)
    return config


if __name__ == '__main__':
    print(load_config()['baidu_ocr'])