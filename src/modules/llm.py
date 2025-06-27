from modules.adapter_abstract import LLMAdapter
import subprocess
import re

from openai import OpenAI

client = OpenAI(api_key="APIKEY")


def parse_code_output(code_output: str) -> str:
    """
    Code is returned within the ''' ''' block. The first word is the
    programming language. This function returns a single string
    containing all code blocks concatenated with correct syntax.

    returns:
        a single string containing all code blocks with correct syntax
    """

    if '''```''' not in code_output:
        return code_output

    code_pattern = r"```(\w+)\s+(.*?)```"
    matches = re.findall(code_pattern, code_output, re.DOTALL)

    code_combined = ""
    for match in matches:
        code_combined += match[1].strip() + "\n\n"

    return code_combined.strip()


class LLM(LLMAdapter):

    def __init__(self):
        self.handle_code_process = None

    def initialize(self) -> int:
        return 1

    def process_code_prompt(self, code_prompt: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "only transform the code provided. Do not add extra code."},
                {"role": "user", "content": code_prompt}
            ],
            stream=False
        )
        return parse_code_output(response.choices[0].message.content)

    def get_name(self) -> str:
        return "GPT-4o"

    def close(self) -> int:
        return 1
