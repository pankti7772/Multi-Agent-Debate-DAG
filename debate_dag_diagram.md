# Multi-Agent Debate DAG Diagram

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	user_input(user_input)
	agent_a(agent_a)
	agent_b(agent_b)
	controller(controller)
	memory(memory)
	judge(judge)
	__end__([<p>__end__</p>]):::last
	__start__ --> user_input;
	agent_a --> memory;
	agent_b --> memory;
	controller -.-> agent_a;
	controller -.-> agent_b;
	controller -.-> judge;
	memory --> controller;
	user_input --> controller;
	judge --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc

```