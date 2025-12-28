#!/usr/bin/env python3
"""
Generate DAG diagram for the Multi-Agent Debate System
"""

from langgraph.graph import StateGraph, START, END
from utils.state import DebateState
from utils.logger import DebateLogger
from utils.config import Config
from nodes.user_input_node import UserInputNode
from nodes.agent_a_node import AgentANode
from nodes.agent_b_node import AgentBNode
from nodes.debate_controller import DebateController
from nodes.memory_node import MemoryNode
from nodes.judge_node import JudgeNode

def create_dag_diagram():
    """Create and save the DAG diagram"""
    
    print("Generating DAG diagram...")
    
    # Initialize logger and nodes
    logger = DebateLogger("dag_generation.log")
    user_input = UserInputNode(logger)
    agent_a = AgentANode(logger)
    agent_b = AgentBNode(logger)
    controller = DebateController(logger)
    memory = MemoryNode(logger)
    judge = JudgeNode(logger)
    
    # Create the workflow (same as in main.py)
    workflow = StateGraph(DebateState)
    
    # Add nodes
    workflow.add_node("user_input", user_input.execute)
    workflow.add_node("agent_a", agent_a.execute)
    workflow.add_node("agent_b", agent_b.execute)
    workflow.add_node("controller", controller.execute)
    workflow.add_node("memory", memory.execute)
    workflow.add_node("judge", judge.execute)
    
    # Add edges (simplified version for diagram)
    workflow.add_edge(START, "user_input")
    workflow.add_edge("user_input", "controller")
    
    # Conditional routing
    def route_to_agent(state):
        if state.get("is_complete", False):
            return "judge"
        elif state.get("current_agent") and state["current_agent"].value == Config.AGENT_A_PERSONA:
            return "agent_a"
        else:
            return "agent_b"
    
    workflow.add_conditional_edges(
        "controller",
        route_to_agent,
        {
            "agent_a": "agent_a",
            "agent_b": "agent_b", 
            "judge": "judge"
        }
    )
    
    workflow.add_edge("agent_a", "memory")
    workflow.add_edge("agent_b", "memory")
    workflow.add_edge("memory", "controller")
    workflow.add_edge("judge", END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Compile the graph
    app = workflow.compile()
    
    try:
        # Generate the diagram using graphviz if possible
        print("Generating DAG visualizations...")
        
        try:
            # draw_png returns bytes
            image_data = app.get_graph().draw_png()
            with open("debate_dag.png", "wb") as f:
                f.write(image_data)
            print("✅ DAG saved to: debate_dag.png")
        except Exception as e:
            print(f"⚠️ draw_png failed: {e}")

        # For PDF, use graphviz library directly if possible
        try:
            import graphviz
            # LangGraph can generate dot if pygraphviz/pydot is present, 
            # but we can also manually define it to be safe
            dot = graphviz.Digraph(comment='Multi-Agent Debate DAG')
            dot.attr(rankdir='TB', size='8,5')
            
            dot.node('START', 'Start', shape='circle')
            dot.node('user_input', 'User Input', shape='box')
            dot.node('controller', 'Controller', shape='diamond')
            dot.node('agent_a', f'Agent A ({Config.AGENT_A_PERSONA})', shape='box')
            dot.node('agent_b', f'Agent B ({Config.AGENT_B_PERSONA})', shape='box')
            dot.node('memory', 'Memory', shape='box')
            dot.node('judge', 'Judge', shape='box')
            dot.node('END', 'End', shape='circle')
            
            dot.edge('START', 'user_input')
            dot.edge('user_input', 'controller')
            dot.edge('controller', 'agent_a', label='scientist turn')
            dot.edge('controller', 'agent_b', label='philosopher turn')
            dot.edge('controller', 'judge', label='debate complete')
            dot.edge('agent_a', 'memory')
            dot.edge('agent_b', 'memory')
            dot.edge('memory', 'controller')
            dot.edge('judge', 'END')
            
            dot.render('debate_dag', format='pdf', cleanup=True)
            print("✅ DAG saved to: debate_dag.pdf")
        except Exception as ge:
            print(f"⚠️ Graphviz PDF rendering failed: {ge}")
        
        # Also save Mermaid as reference
        mermaid_data = app.get_graph().draw_mermaid()
        with open("debate_dag_diagram.md", "w") as f:
            f.write("# Multi-Agent Debate DAG Diagram\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_data)
            f.write("\n```")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")
        return False

if __name__ == "__main__":
    create_dag_diagram()