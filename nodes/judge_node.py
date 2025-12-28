import google.generativeai as genai
from utils.state import DebateState
from utils.config import Config
from utils.logger import DebateLogger

class JudgeNode:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
        self.client = None
        
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            self.client = True
        else:
            print("⚠️ Warning: GEMINI_API_KEY not found. Judge running in Mock Mode.")

    def execute(self, state: DebateState) -> DebateState:
        print("\n=== JUDGE EVALUATION ===")
        print("Analyzing debate arguments...\n")
        
        # 1. Generate Summary
        summary = self._generate_summary(state)
        state["judgment"] = summary # Store in judgment or separate field
        
        self.logger.log_step("JUDGE_SUMMARY", summary)
        print(f"[Judge] Summary of debate:\n{summary}\n")
        
        # 2. Determine Winner
        verdict = self._evaluate_winner(state)
        state["winner"] = verdict["winner"]
        state["judgment"] += f"\n\nWinner: {verdict['winner']}\nReasoning: {verdict['reasoning']}"
        
        self.logger.log_step("JUDGE_WINNER", f"Winner: {verdict['winner']}")
        self.logger.log_step("JUDGE_REASONING", verdict["reasoning"])
        
        print(f"[Judge] Winner: {verdict['winner']}")
        print(f"Reason: {verdict['reasoning']}\n")
        print("="*50 + "\n")
        
        return state

    def _generate_summary(self, state: DebateState) -> str:
        """Summarize the full debate using Gemini"""
        
        # Build full transcript from turns
        transcript = "\n".join([f"{t['agent']}: {t['text']}" for t in state["turns"]])
        
        prompt = f"""You are an impartial Debate Judge. Summarize the following debate on '{state['topic']}' in 2-3 sentences. Focus on the main clash between the two sides.

Debate Transcript:
{transcript}

Summary:"""

        if not self.client:
            return "Mock Judge Summary: The debate explored various facets of the topic with both sides presenting structured arguments."

        try:
            generation_config = genai.types.GenerationConfig(
                temperature=0.5,
                max_output_tokens=200
            )
            response = self.model.generate_content(prompt, generation_config=generation_config)
            return response.text.strip()
            
        except Exception as e:
            self.logger.log_step("ERROR_SUMMARY", f"Failed to generate summary: {str(e)}")
            return f"Summary generation failed: {str(e)}"

    def _evaluate_winner(self, state: DebateState) -> dict:
        """Decide the winner using Gemini"""
        
        transcript = "\n".join([f"{t['agent']}: {t['text']}" for t in state["turns"]])
        
        prompt = f"""You are an expert Debate Judge. Evaluate the following debate on '{state['topic']}'.
        
Criteria:
1. Logical consistency
2. Use of evidence/reasoning
3. Rebuttal effectiveness

Transcript:
{transcript}

Who won? The {Config.AGENT_A_PERSONA} or the {Config.AGENT_B_PERSONA}?
Provide the output in this format:
WINNER: [Persona Name]
REASONING: [1-2 sentences explaining why]

Your evaluation:"""

        if not self.client:
            return {
                "winner": "Scientist",
                "reasoning": "Mock Evaluation: The Scientist provided more data-driven points in this simulated run."
            }

        try:
            generation_config = genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=250
            )
            response = self.model.generate_content(prompt, generation_config=generation_config)
            evaluation = response.text.strip()
            
            # Parse the response
            lines = evaluation.split('\n')
            winner = "Tie"
            reasoning = "Unable to determine winner"
            
            for line in lines:
                if "WINNER:" in line:
                    winner = line.split(":", 1)[1].strip().strip("[]")
                elif "REASONING:" in line:
                    reasoning = line.split(":", 1)[1].strip()
            
            return {
                "winner": winner,
                "reasoning": reasoning
            }
            
        except Exception as e:
            self.logger.log_step("ERROR_EVALUATION", f"Failed to evaluate winner: {str(e)}")
            return {
                "winner": "Error",
                "reasoning": f"Evaluation failed: {str(e)}"
            }