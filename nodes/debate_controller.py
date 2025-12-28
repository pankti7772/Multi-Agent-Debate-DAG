from utils.state import DebateState, AgentType
from utils.config import Config
from utils.logger import DebateLogger

class DebateController:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
    
    def execute(self, state: DebateState) -> DebateState:
        """Control debate flow and turn management"""
        
        # Enforce strict 8-round limit (4 per agent = 8 turns total)
        if len(state["turns"]) >= Config.MAX_ROUNDS:
            state["is_complete"] = True
            self.logger.log_step("DEBATE_COMPLETE", 
                               f"Debate completed after {len(state['turns'])} turns")
            print("=== DEBATE COMPLETED ===\n")
            return state
            
        # Core Logic Enhancement: Repetition & Coherence Checks
        if self._check_repetition(state):
            self.logger.log_step("WARNING", "Repetitive argument detected.")
            print("⚠️ Warning: Argument repetition detected.")

        if not self._check_coherence(state):
            self.logger.log_step("WARNING", "Topic drift detected.")
            print("⚠️ Warning: Argument may be drifting from the topic.")

        # For the very first call, let scientist go first
        if len(state["turns"]) == 0:
            state["current_agent"] = AgentType.SCIENTIST
            state["current_round"] = 1
            return state
            
        # Strict Turn Enforcement:
        # If the last speaker was Scientist, next MUST be Philosopher
        last_turn = state["turns"][-1]
        if last_turn["agent"] == Config.AGENT_A_PERSONA:
             state["current_agent"] = AgentType.PHILOSOPHER
        else:
             state["current_agent"] = AgentType.SCIENTIST
        
        # Update round number (1-indexed)
        # 1-2 turns = Round 1
        # 3-4 turns = Round 2 ...
        state["current_round"] = (len(state["turns"]) // 2) + 1
        
        # Log current state
        self.logger.log_step("CONTROLLER", {
            "round": state["current_round"],
            "next_agent": state["current_agent"].value,
            "turns_count": len(state["turns"])
        })
        
        return state

    def _check_coherence(self, state: DebateState) -> bool:
        """Lightweight check for topic drift"""
        if not state["turns"] or not state["topic"]:
            return True
            
        latest_arg = state["turns"][-1]["text"].lower()
        topic_words = set(w for w in state["topic"].lower().split() if len(w) > 2)
        
        if not topic_words:
            return True
            
        # Check if at least one key topic word is mentioned
        return any(word in latest_arg for word in topic_words)

    def _check_repetition(self, state: DebateState) -> bool:
        """Check if the latest argument is substantially repeated"""
        if len(state["turns"]) < 2:
            return False
            
        latest_arg = state["turns"][-1]["text"].lower()
        previous_args = [t["text"].lower() for t in state["turns"][:-1]]
        
        # Basic word overlap check
        latest_words = set(w for w in latest_arg.split() if len(w) > 3)
        if not latest_words:
            return False
            
        for prev_arg in previous_args:
            prev_words = set(w for w in prev_arg.split() if len(w) > 3)
            if not prev_words:
                continue
                
            overlap = len(latest_words.intersection(prev_words))
            # 70% word overlap threshold for repetition
            if overlap > len(latest_words) * 0.7:
                return True
        
        return False