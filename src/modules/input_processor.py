import json

class InputProcessor:
    """
        A class that processes the input json file. The input json file contains
        the mode of the framework and the prompts for the framework. The
        prompts are stored in a list inside the json file.
    """

    def __init__(self, input_file):
        self.__prompts = []
        self.__input_file = input_file

    def process_input(self):
        """
        Processes the input json file.
        """
        with open(self.__input_file, "r") as f:
            input_json = json.load(f)
            self.__prompts = input_json["prompts"]
            
    def get_prompts(self):
        return self.__prompts

