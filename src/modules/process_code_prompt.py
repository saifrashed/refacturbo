from modules.llm import LLM
import os


class ProcessCodePrompt:

    def __init__(self, prompts) -> None:
        self.__prompts = prompts

    def process_code_prompts(self, output_dir: None):
        """
        This function makes it possible to process a list of code prompts. This
        function communicates with the llms_interface to process the code prompts
        in parallel or sequentially. The large language model provides
        functions that can be used to process the code prompts sequentially or
        in parallel. The output is a list of dictionaries containing the model
        name, prompt and the output of the model.

        Returns:
            list: A list of dictionaries, where the dictionaries contain the
            keys 'model_name', 'prompt', and 'code'. If the mode
            is not valid, an empty list is returned.
        """
        output = []
        model = LLM()

        # Generate the code using the LLM
        model_name = model.get_name()
        if model.initialize() == 0:
            print(f"Error while initializing model {model_name}")
            models_with_initilization_error.append(model)
        else:
            for index, prompt in enumerate(self.__prompts):
                code = model.process_code_prompt(prompt)
                output.append({"model_name": model_name, "prompt": prompt, "code": code, "index": index})

        if output is None:
            return []

        # Check if the ouput directory exists
        if output_dir[-1] != "/":
            output_dir += "/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the output to a file, and add the filename to the dictionary
        for model_dict in output:
            print(model_dict.keys())

            filename = f"{model_dict['index']}.java"
            filename = output_dir + filename

            with open(filename, "w") as f:
                f.write(model_dict['code'])
                f.close()

            model_dict['filename'] = filename

        return output