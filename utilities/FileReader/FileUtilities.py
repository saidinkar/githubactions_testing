import logging
import os


class FileUtilities:
    def __init__(self):
        pass

    @staticmethod
    def get_cwd():
        current_dir = os.getcwd()
        logging.info("Get the current working directory")
        return current_dir