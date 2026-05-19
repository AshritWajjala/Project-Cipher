import subprocess
from langchain_ollama import ChatOllama
import ollama
from langchain_core.prompts import ChatPromptTemplate
import time
import hashlib

# llm = ChatOllama(model="qwen3:8b", temperature=0)

# import asyncio


# p1 = subprocess.run("cat /home/lucifer/convo.txt", shell=True, capture_output=True, text=True)

# p2 = subprocess.run("grep -n **Whitelisting:**", shell=True, capture_output=True, input=p1.stdout, text=True)

# print(p2.stdout)


# Turning a plain text string into a SHA-256 hex digest
from pathlib import Path
import os
# env_p = Path(".env")

# path = Path(__file__).resolve().parent.parent.parent / ".env"
# print(path)
# if os.path.exists(path):
#     print("ash")
