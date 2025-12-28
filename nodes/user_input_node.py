from utils.state import DebateState, AgentType
from utils.logger import DebateLogger

class UserInputNode:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
    
    def execute(self, state: DebateState) -> DebateState:
        """Get debate topic from user input with validation"""
        print("\n=== MULTI-AGENT DEBATE SYSTEM ===")
        print("Two AI agents will debate on your chosen topic.")
        print("Agent A: Scientist | Agent B: Philosopher")
        print("8 rounds total (4 arguments per agent)\n")
        
        # Get topic from user with validation
        while not state["topic"]:
            topic = input("Enter topic for debate: ").strip()
            
            # Simple sanitization
            topic = "".join(char for char in topic if char.isalnum() or char in " ,.?!-")
            
            if len(topic) < 10:
                print("Topic is too short. Please provide at least 10 characters.")
            elif len(topic) > 200:
                print("Topic is too long. Please limit to 200 characters.")
            elif topic:
                state["topic"] = topic
            else:
                print("Please enter a valid topic.")
        
        # Initialize debate state
        state["current_round"] = 1
        state["current_agent"] = AgentType.SCIENTIST  # Scientist goes first
        
        # Log the initialization
        self.logger.log_step("USER_INPUT", f"Debate Topic: {state['topic']}")
        self.logger.log_step("INITIALIZATION", 
                           f"Starting debate between {AgentType.SCIENTIST.value} and {AgentType.PHILOSOPHER.value}")
        
        print(f"\nStarting debate on: '{state['topic']}'")
        print(f"Round 1 - {state['current_agent'].value} will go first...\n")
        
        return state