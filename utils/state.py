from typing import Dict, List, Optional, TypedDict, Any
from enum import Enum

class AgentType(Enum):
    SCIENTIST = "Scientist"
    PHILOSOPHER = "Philosopher"

class DebateState(TypedDict):
    topic: str
    current_round: int
    current_agent: Optional[AgentType]
    
    # New structured memory format
    # "turns": [{"round":1, "agent":"...", "text":"...", "meta":{...}}]
    turns: List[Dict[str, Any]]
    
    # Context slices for agents
    agent_a_memory: List[str] # Keeping as simplified list for now, or can be derived
    agent_b_memory: List[str]
    
    agent_a_context: str
    agent_b_context: str
    
    is_complete: bool
    winner: Optional[str]
    judgment: str
    summary: str

def create_initial_state() -> DebateState:
    return {
        "topic": "",
        "current_round": 0,
        "current_agent": None,
        "turns": [],
        "agent_a_memory": [],
        "agent_b_memory": [],
        "agent_a_context": "",
        "agent_b_context": "",
        "is_complete": False,
        "winner": None,
        "judgment": ""
    }