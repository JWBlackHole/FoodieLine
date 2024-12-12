import getpass
import os
from textwrap import dedent

import requests

# from langchain.chat_models.ollama import ChatOllama

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.agents import tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)

from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import tool
from langchain.agents import AgentExecutor

@tool
def sum(a: int, b: int) -> int:
    """Sum up number1:a and number2:b.

    Args:
        a (int): number1
        b (int): number2

    Returns:
        int: sum of 'a' and 'b'
    """
    
    print("In sum tool.")
    return a + b

@tool
def count_char_in_string(s: str, c: str) -> int:
    """Calculate how many certain single character:c in the string:s.

    Args:
        s (str): string to search the character.
        c (str): character that we want to know the number.

    Returns:
        int: how many character:c in string:s.
    """
    
    print("In count char tool.")
    count = 0
    for i in s:
        if(c == i):
            count += 1
    return count

class MyModel():
    
    def __init__(self):
        self.api_key = os.environ['OPENAI_API_KEY']
        self.llm   = ChatOpenAI(model="gpt-4o-mini", api_key = self.api_key)
        self.tools = [sum, count_char_in_string]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are very powerful assistant, but don't know current events",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | self.llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        
    def invoke(self, input_text: str):
        return self.agent_executor.invoke({
            'input': input_text,
        })