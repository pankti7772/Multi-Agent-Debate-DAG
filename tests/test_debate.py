import unittest
from utils.state import create_initial_state, AgentType, DebateState
from utils.config import Config
from nodes.debate_controller import DebateController
from nodes.memory_node import MemoryNode
from utils.logger import DebateLogger

class MockLogger(DebateLogger):
    def __init__(self):
        self.logs = []
        self.log_file = "mock_log.jsonl"
    def log_step(self, step_name, content):
        self.logs.append((step_name, content))

class TestDebateLogic(unittest.TestCase):
    def setUp(self):
        self.logger = MockLogger()
        self.controller = DebateController(self.logger)
        self.memory = MemoryNode(self.logger)
        
    def test_turn_enforcement(self):
        """Test that controller strictly enforces alternating turns based on 'turns' list"""
        state = create_initial_state()
        
        # Initially, it's Scientist's turn
        state = self.controller.execute(state)
        self.assertEqual(state["current_agent"], AgentType.SCIENTIST)
        
        # Mock a turn taken
        state["turns"].append({"agent": "Scientist", "text": "Logic and evidence are key.", "round": 1})
        
        # Next should be Philosopher
        state = self.controller.execute(state)
        self.assertEqual(state["current_agent"], AgentType.PHILOSOPHER)
        
        # Mock another turn taken
        state["turns"].append({"agent": "Philosopher", "text": "What is the meaning of truth?", "round": 1})
        
        # Next should be Scientist
        state = self.controller.execute(state)
        self.assertEqual(state["current_agent"], AgentType.SCIENTIST)

    def test_repetition_check(self):
        """Test detection of repeated arguments in 'turns' list"""
        state = create_initial_state()
        state["turns"] = [
            {"agent": "Scientist", "text": "Artificial Intelligence presents significant existential risks to humanity.", "round": 1},
            {"agent": "Philosopher", "text": "I agree with the premise of risks.", "round": 1},
            # Highly repetitive argument
            {"agent": "Scientist", "text": "Artificial Intelligence presents significant existential risks to humanity.", "round": 2} 
        ]
        
        is_repetitive = self.controller._check_repetition(state)
        self.assertTrue(is_repetitive)

    def test_coherence_check(self):
        """Test detection of topic drift"""
        state = create_initial_state()
        state["topic"] = "Climate Change Solutions"
        
        # Coherent argument
        state["turns"] = [{"agent": "Scientist", "text": "Climate change require urgent solutions.", "round": 1}]
        self.assertTrue(self.controller._check_coherence(state))
        
        # Drifting argument (no keywords like climate, change, solutions, carbon, emissions)
        state["turns"] = [{"agent": "Scientist", "text": "The price of bananas is increasing.", "round": 1}]
        self.assertFalse(self.controller._check_coherence(state))

    def test_memory_context(self):
        """Test that memory node provides relevant context slices"""
        state = create_initial_state()
        state["turns"] = [
            {"agent": "Scientist", "text": "Data proves X.", "round": 1},
            {"agent": "Philosopher", "text": "But what about Y?", "round": 1}
        ]
        
        # Execute MemoryNode to refresh context
        state = self.memory.execute(state)
        
        # Scientist's next turn context should have Philosopher's last point
        self.assertIn("But what about Y?", state["agent_a_context"])
        self.assertIn("YOUR PREVIOUS POINT", state["agent_a_context"])
        self.assertIn("Data proves X.", state["agent_a_context"])

if __name__ == '__main__':
    unittest.main()
