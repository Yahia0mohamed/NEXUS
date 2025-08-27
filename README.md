<p align="center">
<h1><strong>NEXUS</strong> (Neural eXpert for Unified coding Solutions)</h1>
</p>



🚀 AI-powered coding assistant for intelligent code generation, automated reviews, and optimization.  
Built with **LLMs** and **LangChain**, designed to boost developer productivity by **40%+**.
---


## ✨ Features
- **Code Generation** – Generate new code snippets or full implementations from natural language prompts.
- **Code Review** – Review and optimize code for clarity, performance, and best practices.
- **Error Explainer** – Analyze error messages, tracebacks, and bugs, and suggest fixes from StackOverflow and LLM reasoning.
- **Documentation Generator** – Automatically create clean, developer-friendly documentation for your codebase.
- **Smart Router** – Dynamically routes user queries to the right agent (`generate`, `review`, `error`, `doc`).

---

## ⚙️ System Architecture
NEXUS is built with a modular agent-based architecture:
- **NexusAgent** – Central router that decides which agent handles the user query.
- **CodeGenAgent** – Responsible for creating new code.
- **CodeReviewAgent** – Analyzes, improves, and optimizes existing code.
- **ErrorExplainerAgent** – Uses DuckDuckGo + LLMs to find and explain solutions for errors.
- **CodeDocAgent** – Generates documentation and explanations for given code.
- **Tools Layer** – Integrates StackOverflow search, general error analyzers, and custom LangChain tools.

<p align="center">
  <img src=".assets/NEXUS%20-%20system%20architure.svg" alt="SYSARCH" />
</p>

## 🔄 Workflow
- The user provides input to the NexusAgent.
- The NexusAgent analyzes the input and routes tasks to the appropriate agents. For example, if the user requests code generation, the task is routed to the CodeGenAgent. If the user provides code with an error, the task is routed to the ErrorExplainerAgent.
- Each agent performs its assigned task, leveraging the LLM for reasoning and, in the case of the ErrorExplainerAgent, external resources like DuckDuckGo Search and StackOverflow.
- The agents return their results to the NexusAgent.
- The NexusAgent aggregates the results and formulates the final output for the user.
- The Assistant Output is presented to the user.

<p align="center">
  <img src=".assets/NEXUS - workflow.svg" alt="WRKFLW" />
</p>

---

## 🖥️ Example Usage
```bash
$ python main.py

 _   _ _______  ___   _ ____  
| \ | | ____\ \/ / | | / ___| 
|  \| |  _|  \  /| | | \___ \ 
| |\  | |___ /  \| |_| |___) |
|_| \_|_____/_/\_\\___/|____/ 

Welcome to NEXUS — your favorite Code Assistant 🤖

Sample queries:

* "generate code for binary search in Python"
* "review my C++ linked list implementation"
* "fix error: AttributeError: 'DDGS' object has no attribute 'name'"
* "create documentation for my FastAPI service"
```


```
git clone https://github.com/Yahia0mohamed/NEXUS
cd NEXUS
pip install -r requirements.txt
```


