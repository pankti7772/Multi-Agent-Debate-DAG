# Multi-Agent Debate DAG using LangGraph

## VIDEO WALKTHROUGH LINK :
https://drive.google.com/file/d/1RZlKhjKBvdZWL6ymKhEE2GHjFoOooj_B/view?usp=share_link

A sophisticated debate system built with LangGraph that enables AI agents to engage in structured debates while maintaining context and memory.

## Overview

This system orchestrates debates between two AI agents with distinct personas (default: Scientist vs Philosopher) on user-provided topics. The debate follows a directed acyclic graph (DAG) structure:
- **Two Debating Agents**: Present alternating arguments.
- **Memory Preservation**: Unified JSON-based memory ensures coherent discussion.
- **Impartial Judge**: Evaluates the debate and declares a winner.

**v2.0 Update**: The system now uses **Google Gemini** (`gemini-1.5-flash` by default) for high-performance, cost-effective inference.

## Key Features (v2.0 Upgrade)

- **Strict 8-Round Enforcement**: Precise turn-taking (4 arguments per agent) managed by a central controller.
- **Structured JSON Memory**: Unified memory system for production-grade storage.
- **Automated Logical Checks**:
    - **Repetition Detection**: Warns agents about repeating similar arguments.
    - **Topic Drift Validation**: Ensures arguments remain relevant to the declared topic.
- **Production Logging**: Detailed JSON Lines (`.jsonl`) logging with timestamps.
- **Deterministic Behavior**: Support for a `--seed` flag to ensure reproducible debate outcomes.
- **Professional PDF Reports**: Generate high-quality debate transcripts and judging summaries.
- **CLI Interface**: Robust CLI for full configuration (`--topic`, `--seed`, etc.).

## Folder Structure

```plaintext
Multi-Agent-Debate-DAG/
├── nodes/               # LangGraph Node Implementations
│   ├── agent_a_node.py  # Scientist Agent (Gemini)
│   ├── agent_b_node.py  # Philosopher Agent (Gemini)
│   ├── debate_controller.py # Logic & Flow Enforcement
│   ├── judge_node.py    # Evaluation & Verdict (Gemini)
│   ├── memory_node.py   # Context Slicing & Storage
│   └── user_input_node.py # Entry point
├── utils/               # Shared Utilities
│   ├── config.py        # Centralized Settings (Gemini Config)
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
# venv\Scripts\activate  # Windows
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. **Environment Setup**:
   Create a `.env` file (copy from `.env.example`) and add your Google Gemini API key:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   ```
   > **Note**: Get your key from [Google AI Studio](https://aistudio.google.com/).

## Usage

### Running a Debate (CLI)
Run a full debate with a custom topic. If no API key is found, the system will run in **Mock Mode** for demonstration purposes.

```bash
python main.py --topic "Should AI be regulated like medicine?" --seed 42
```

**CLI Arguments:**
- `--topic`: The subject of the debate.
- `--seed`: Integer for deterministic behavior (requires `temperature=0` internally).
- `--log-path`: Path to save the structured JSONL log file (default: `logs/debate_log.jsonl`).
- `--agent-a`: Persona name for Agent A (e.g., "Physicist").
- `--agent-b`: Persona name for Agent B (e.g., "Theologian").

### Generating a PDF Report
After a debate completes, generate a professional-grade report of the transcript and judgment:

```bash
python scripts/generate_report.py logs/debate_log.jsonl debate_report.pdf
```

### Visualizing the DAG
To generate the Mermaid visualization of the debate architecture:

```bash
python scripts/generate_dag.py
```

## Testing & Verification
We maintain high standards for logic enforcement. Run the provided unit tests to verify turn-taking, repetition detection, and coherence checks:

```bash
python -m pytest tests/test_debate_logic.py
```

## Contributing / Customization

The system is designed for easy extension:
1. **Adding New Agents**: Create new node files in `nodes/` leveraging `google.generativeai`.
2. **Modifying Rules**: Update validation logic in `debate_controller.py`.
3. **Extending Memory**: Enhance memory structures in `memory_node.py`.

## License

MIT License - Feel free to use and modify as needed.
