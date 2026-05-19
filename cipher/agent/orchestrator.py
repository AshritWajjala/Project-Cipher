from pydantic import BaseModel
import ollama
from cipher.agent.prompts import get_agent_prompt

class CommandPlan(BaseModel):
    intention: str
    execution_plan: str
    need_root_access: bool

def generate_command_plan(user_query: str) -> CommandPlan:
    """Translates raw user queries into a validated CommandPlan object."""
    response = ollama.generate(
        model='qwen3:8b', 
        prompt=get_agent_prompt(user_query),
        format=CommandPlan.model_json_schema()  
    )
    
    return CommandPlan.model_validate_json(response['response'])

