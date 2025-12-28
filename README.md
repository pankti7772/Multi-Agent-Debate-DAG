# Multi-Agent Debate DAG using LangGraph

##VIDEO WALKTHROUGH LINK :
https://www.loom.com/share/8339ae87b87a430ea58ff6a44b60f417?sid=a6fa1214-33bd-4fe2-979a-2121f6a97d3b

A sophisticated debate system built with LangGraph that enables AI agents to engage in structured debates while maintaining context and memory.

## Overview

This system orchestrates debates between two AI agents with distinct personas (by default, a Scientist and a Philosopher) on user-provided topics. The debate follows a directed acyclic graph (DAG) structure, with each node handling specific aspects of the debate flow:

- Two debating agents present alternating arguments
- Memory preservation ensures coherent discussion
- An impartial judge evaluates and declares a winner

The agent personas are configurable via environment variables, allowing for diverse debate perspectives (e.g., Lawyer vs Economist, Artist vs Critic, etc.).

## Key Features (v2.0 Upgrade)

- **Strict 8-Round Enforcement**: Precise turn-taking (4 arguments per agent) managed by a central controller.
- **Structured JSON Memory**: Unified memory system using a `turns` JSON structure for production-grade storage.
- **Automated Logical Checks**:
    - **Repetition Detection**: Prevents agents from repeating substantially similar arguments.
    - **Topic Drift Validation**: Ensures arguments remain coherent and relevant to the debate topic.
- **Production Logging**: Detailed JSON Lines (`.jsonl`) logging with timestamps for structured analysis.
- **Deterministic Behavior**: Support for a `--seed` flag to ensure reproducible debate outcomes.
- **Professional PDF Reports**: Generate beautiful, high-quality debate transcripts and judging summaries.
- **CLI Interface**: Robust CLI for full debate configuration.

## Folder Structure

```plaintext
Multi-Agent-Debate-DAG/
├── nodes/               # LangGraph Node Implementations
│   ├── agent_a_node.py  # Scientist Agent
│   ├── agent_b_node.py  # Philosopher Agent
│   ├── debate_controller.py # Logic & Flow Enforcement
│   ├── judge_node.py    # Evaluation & Verdict
│   ├── memory_node.py   # Context Slicing & Storage
│   └── user_input_node.py # Entry point
├── utils/               # Shared Utilities
│   ├── config.py        # Centralized Settings
│   ├── logger.py        # JSONL Logger
│   ├── state.py         # Type Definitions (TypedDict)
├── scripts/             # Utility Scripts
│   ├── generate_dag.py     # DAG Mermaid/Image Generation
│   └── generate_report.py  # PDF Report Generator
├── tests/               # Validation Suite
│   └── test_debate.py   # Unit tests for flow & logic
├── main.py              # Application Entry Point
└── requirements.txt     # Project Dependencies
```

## Installation

1. Clone the repository and navigate to the directory:
```bash
git clone https://github.com/yourusername/debate_dag.git
cd debate_dag
```

2. Setup virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

3. Install requirements (including new PDF utilities):
```bash
pip install -r requirements.txt
pip install fpdf2  # Required for report generation
```

## Usage

### Running a Debate (CLI)
The v2.0 update introduces a robust CLI interface. You can run a full debate with custom personas and a reproducible seed:

```bash
python main.py --topic "Is AI sentient?" --seed 42 --log-path logs/debate.jsonl
```

**CLI Arguments:**
- `--topic`: The subject of the debate.
- `--seed`: Integer for deterministic behavior (requires `temperature=0` internally).
- `--log-path`: Path to save the structured JSONL log file.
- `--agent-a`: Persona name for Agent A (e.g., "Physicist").
- `--agent-b`: Persona name for Agent B (e.g., "Theologian").

### Generating a PDF Report
After a debate completes, generate a professional-grade report of the transcript and judgment:

```bash
python scripts/generate_report.py logs/debate.jsonl debate_report.pdf
```

### Visualizing the DAG
To generate the Mermaid visualization of the debate architecture:

```bash
python scripts/generate_dag.py
```

## Testing & Verification
We maintain high standards for logic enforcement. Run the provided unit tests to verify turn-taking, repetition detection, and coherence checks:

```bash
python -m unittest tests/test_debate.py
```

## Contributing / Customization

The system is designed for easy extension:

1. **Adding New Agents**: Create new node files in `nodes/` directory
2. **Modifying Rules**: Update validation logic in `debate_controller.py`
3. **Extending Memory**: Enhance memory structures in `memory_node.py`

## License

MIT License - Feel free to use and modify as needed.
