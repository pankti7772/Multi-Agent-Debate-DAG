#!/usr/bin/env python3
"""
Multi-Agent Debate DAG using LangGraph
Main application file
"""

import sys
import argparse
import random
from langgraph.graph import StateGraph, START, END
from utils.state import DebateState, create_initial_state
from utils.logger import DebateLogger
from utils.config import Config
from nodes.user_input_node import UserInputNode
from nodes.agent_a_node import AgentANode
from nodes.agent_b_node import AgentBNode
from nodes.debate_controller import DebateController
from nodes.memory_node import MemoryNode
from nodes.judge_node import JudgeNode

class DebateSystem:
    def __init__(self):
        # Initialize logger with configured path
        self.logger = DebateLogger(log_file=Config.LOG_PATH)
        self._initialize_nodes()
        self._create_graph()
    
    def _initialize_nodes(self):
        """Initialize all debate nodes"""
        self.user_input = UserInputNode(self.logger)
        self.agent_a = AgentANode(self.logger)
        self.agent_b = AgentBNode(self.logger)
        self.controller = DebateController(self.logger)
        self.memory = MemoryNode(self.logger)
        self.judge = JudgeNode(self.logger)
    
    def _create_graph(self):
        """Create the LangGraph workflow"""
        # Initialize the state graph
        workflow = StateGraph(DebateState)
        
        # Add nodes to the graph
        workflow.add_node("user_input", self.user_input.execute)
        workflow.add_node("agent_a", self.agent_a.execute)
        workflow.add_node("agent_b", self.agent_b.execute)
        workflow.add_node("controller", self.controller.execute)
        workflow.add_node("memory", self.memory.execute)
        workflow.add_node("judge", self.judge.execute)
        
        self.workflow = workflow

    def _add_graph_edges(self):
        """Add edges and conditional logic to the graph"""
        
        # Start with user input
        self.workflow.add_edge(START, "user_input")
        
        # After user input, go to controller
        self.workflow.add_edge("user_input", "controller")
        
        # From controller, decide which agent should speak
        self.workflow.add_conditional_edges(
            "controller",
            self._route_to_agent,
            {
                "agent_a": "agent_a",
                "agent_b": "agent_b", 
                "judge": "judge"
            }
        )
        
        # After each agent, update memory then back to controller
        self.workflow.add_edge("agent_a", "memory")
        self.workflow.add_edge("agent_b", "memory")
        self.workflow.add_edge("memory", "controller")
        
        # Judge ends the debate
        self.workflow.add_edge("judge", END)
        
        # Compile the graph
        self.app = self.workflow.compile()
    
    def _route_to_agent(self, state: DebateState) -> str:
        """Determine which node to route to based on state"""
        
        # If debate is complete, go to judge
        if state["is_complete"]:
            return "judge"
        
        # Route to appropriate agent based on current_agent
        if state["current_agent"].value == Config.AGENT_A_PERSONA:
            return "agent_a"
        elif state["current_agent"].value == Config.AGENT_B_PERSONA:
            return "agent_b"
        else:
            return "judge"  # Fallback
    
    def run_debate(self):
        """Execute the complete debate workflow"""
        
        try:
            print(f"Initializing Multi-Agent Debate System (Topic: {Config.TOPIC})...")
            self._add_graph_edges()
            
            # Initialize state
            initial_state = create_initial_state()
            initial_state["topic"] = Config.TOPIC
            
            # Run the workflow with increased recursion limit
            config = {"recursion_limit": 50}
            final_state = self.app.invoke(initial_state, config=config)
            
            # Final logging
            self.logger.log_step("DEBATE_COMPLETE", 
                               f"Final winner: {final_state['winner']}")
            
            print(f"\n🎉 Debate completed successfully!")
            print(f"📝 Full log saved to: {Config.LOG_PATH}")
            
            return final_state
            
        except Exception as e:
            error_msg = f"Debate execution failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.logger.log_step("ERROR", error_msg)
            return None

def parse_arguments():
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser(description='Multi-Agent Debate DAG')
    parser.add_argument('--topic', type=str, help='Topic for the debate')
    parser.add_argument('--seed', type=int, help='Random seed for deterministic behavior')
    parser.add_argument('--log-path', type=str, help='Path to log file')
    parser.add_argument('--agent-a', type=str, help='Persona for Agent A')
    parser.add_argument('--agent-b', type=str, help='Persona for Agent B')
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Update configuration
    config_updates = {}
    if args.topic: config_updates['TOPIC'] = args.topic
    if args.seed is not None: 
        config_updates['SEED'] = args.seed
        random.seed(args.seed)  # Set python random seed
    if args.log_path: config_updates['LOG_PATH'] = args.log_path
    if args.agent_a: config_updates['AGENT_A_PERSONA'] = args.agent_a
    if args.agent_b: config_updates['AGENT_B_PERSONA'] = args.agent_b
    
    Config.update(**config_updates)
    
    try:
        debate_system = DebateSystem()
        final_state = debate_system.run_debate()
        
        if final_state:
            return 0  # Success
        else:
            return 1  # Failure
            
    except KeyboardInterrupt:
        print("\n\nDebate interrupted by user.")
        return 1
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())