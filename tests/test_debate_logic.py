import pytest
from utils.state import create_initial_state, AgentType
from utils.config import Config
from nodes.debate_controller import DebateController
from utils.logger import DebateLogger
import os

@pytest.fixture
def controller():
    logger = DebateLogger(log_file="test_log.jsonl")
    return DebateController(logger)

def test_turn_enforcement(controller):
    state = create_initial_state()
    
    # First turn should be Scientist
    state = controller.execute(state)
    assert state["current_agent"] == AgentType.SCIENTIST
    
    # Simulate Scientist spoke
    state["turns"].append({
        "round": 1,
        "agent": Config.AGENT_A_PERSONA,
        "text": "Science is observation.",
        "meta": {}
    })
    
    # Next should be Philosopher
    state = controller.execute(state)
    assert state["current_agent"] == AgentType.PHILOSOPHER
    
    # Simulate Philosopher spoke
    state["turns"].append({
        "round": 1,
        "agent": Config.AGENT_B_PERSONA,
        "text": "Philosophy is thinking.",
        "meta": {}
    })
    
    # Next should be Scientist
    state = controller.execute(state)
    assert state["current_agent"] == AgentType.SCIENTIST

def test_repetition_detection(controller):
    state = create_initial_state()
    
    # Add an argument
    state["turns"].append({
        "round": 1,
        "agent": Config.AGENT_A_PERSONA,
        "text": "The sky is blue because of Rayleigh scattering.",
        "meta": {}
    })
    
    # Add a repeated argument (same words)
    state["turns"].append({
        "round": 2,
        "agent": Config.AGENT_A_PERSONA,
        "text": "The sky is blue because of Rayleigh scattering.",
        "meta": {}
    })
    
    assert controller._check_repetition(state) is True

    # Add a non-repeated argument
    state["turns"][-1]["text"] = "Gravity pulls things down."
    assert controller._check_repetition(state) is False

def test_round_limit(controller):
    state = create_initial_state()
    
    # Fill up 8 turns
    for i in range(Config.MAX_ROUNDS):
        state["turns"].append({
            "round": (i // 2) + 1,
            "agent": Config.AGENT_A_PERSONA if i % 2 == 0 else Config.AGENT_B_PERSONA,
            "text": f"Argument {i}",
            "meta": {}
        })
    
    state = controller.execute(state)
    assert state["is_complete"] is True

def teardown_module(module):
    if os.path.exists("test_log.jsonl"):
        os.remove("test_log.jsonl")
