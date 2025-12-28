#!/usr/bin/env python3
"""
Test basic setup and imports
"""

from utils.config import Config
def test_imports():
    """Test all our imports work"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from utils.state import DebateState, AgentType
        from utils.logger import DebateLogger
        from utils.config import Config
        print("✅ Utils imports successful")
        
        # Test node imports
        from nodes.user_input_node import UserInputNode
        from nodes.agent_a_node import AgentANode
        from nodes.agent_b_node import AgentBNode
        from nodes.debate_controller import DebateController
        from nodes.memory_node import MemoryNode
        from nodes.judge_node import JudgeNode
        print("✅ Node imports successful")
        
        # Test external libraries
        from groq import Groq
        from langgraph.graph import StateGraph, START, END
        print("✅ External library imports successful")
        
        print("\n🎉 All imports working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports()