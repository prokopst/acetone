"""
This tutorial is more like an extension of tutorial01, but instead of instance registration
it uses json to load configuration and load the right dependencies.
"""

import json
# import the container from tutorial01
from tutorials.tutorial01.dependencies import dependencies


def main():
    # The library does not do on file handling or format specific parsing logic.
    # You'll parse it and pass the dictionary to the container.
    with open('configuration.json') as file:
        configuration = json.load(file)
        dependencies.load_from_dicts(configuration)


if __name__ == '__main__':
    main()
