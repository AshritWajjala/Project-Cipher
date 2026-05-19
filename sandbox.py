import subprocess
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import time

llm = ChatOllama(model="qwen3:8b", temperature=0)

import asyncio


p1 = subprocess.run("cat /home/lucifer/convo.txt", shell=True, capture_output=True, text=True)

p2 = subprocess.run("grep -n **Whitelisting:**", shell=True, capture_output=True, input=p1.stdout, text=True)

print(p2.stdout)