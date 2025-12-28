from utils.config import Config
from utils.state import DebateState, AgentType
from utils.logger import DebateLogger
from typing import Dict, List, Any

class MemoryNode:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
    
    def execute(self, state: DebateState) -> DebateState:
        """Update and manage memory for agents"""
        
        # Update context slices for the NEXT agent's turn
        state["agent_a_context"] = self.get_relevant_context(state, Config.AGENT_A_PERSONA)
        state["agent_b_context"] = self.get_relevant_context(state, Config.AGENT_B_PERSONA)
        
        # Log memory state
        self.logger.log_step("MEMORY_UPDATE", {
            "total_turns": len(state["turns"]),
            "latest_turn": state["turns"][-1] if state["turns"] else None
        })
        
        return state
    
    def get_relevant_context(self, state: DebateState, agent_persona: str) -> str:
        """
        Provides each agent only the memory relevant to their next turn.
        Requirement: 'provide each agent only the memory relevant to their next turn'
        """
        if not state["turns"]:
            return "No previous arguments."
            
        relevant_text = "--- RELEVANT DEBATE HISTORY ---\n"
        
        # Get last turn
        last_turn = state["turns"][-1]
        
        if last_turn['agent'] == agent_persona:
            relevant_text += f"YOUR PREVIOUS ARGUMENT: {last_turn['text']}\n"
            # Try to find the opponent's previous argument if available
            opp_turn = next((t for t in reversed(state["turns"][:-1]) if t['agent'] != agent_persona), None)
            if opp_turn:
                relevant_text += f"OPPONENT'S LAST POINT: {opp_turn['text']}\n"
            else:
                relevant_text += "Opponent has not spoken yet.\n"
        else:
            relevant_text += f"OPPONENT'S LAST ARGUMENT ({last_turn['agent']}): {last_turn['text']}\n"
            # Get agent's own previous argument if it exists
            own_last_turn = next((t for t in reversed(state["turns"][:-1]) if t['agent'] == agent_persona), None)
            if own_last_turn:
                relevant_text += f"YOUR PREVIOUS POINT: {own_last_turn['text']}\n"
            
        return relevant_text