import google.generativeai as genai
from utils.state import DebateState, AgentType
from utils.config import Config
from utils.logger import DebateLogger

class AgentANode:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
        self.client = None
        
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            self.client = True # Flag to indicate active client
        else:
            print("⚠️ Warning: GEMINI_API_KEY not found. Agent A running in Mock Mode.")

    def execute(self, state: DebateState) -> DebateState:
        # Check if it's our turn
        if state["current_agent"] != AgentType.SCIENTIST:
            return state
            
        # Get memory context
        context = state.get("agent_a_context", "")
        
        # Generate argument
        argument = self._generate_argument(state, context)
        
        # Log to system log
        self.logger.log_step(f"ROUND_{state['current_round']}_SCIENTIST", argument)
        
        # Print to console
        print(f"\n[Round {state['current_round']}] Scientist: {argument}")
        
        # Update turns list (structured memory)
        new_turn = {
            "round": state["current_round"],
            "agent": Config.AGENT_A_PERSONA,
            "text": argument,
            "meta": {
                "timestamp": "auto-generated",
                "relevance_score": 1.0 
            }
        }
        state["turns"].append(new_turn)
        
        return state

    def _generate_argument(self, state: DebateState, context: str) -> str:
        """Generate argument using Gemini"""
        
        prompt = f"""You are a {Config.AGENT_A_PERSONA} in a debate about: "{state['topic']}".
        
Context from previous turns:
{context}

Your goal: Provide a strong, logical argument from a scientific perspective.
Limit your response to 2-3 concise sentences.

Your argument (Round {state["current_round"]}/8):"""

        if not self.client:
            # Fallback for simulation without API key
            return f"[Mock Scientist Argument] Based on the topic '{state['topic']}', statistical analysis suggests a high correlation between logic and evidence."

        try:
            # Gemini generation
            generation_config = genai.types.GenerationConfig(
                temperature=0.0 if Config.SEED else 0.7,
                max_output_tokens=150
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text.strip()
            
        except Exception as e:
            self.logger.log_step("ERROR_SCIENTIST", f"Failed to generate argument: {str(e)}")
            return f"[Error generating scientific argument: {str(e)}]"