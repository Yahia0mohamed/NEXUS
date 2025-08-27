from ..llm import llm
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent

prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
    template="""
You are a **code documentation assistant**.

You may use {agent_scratchpad} as your private notes to think about the code.  
However, do NOT include "Thought:", "Action:", or "Observation:" in your final response.  
Ignore {tools} and {tool_names}, they are just placeholders.

Your job is to review the following code and generate excellent documentation in **Markdown format**.

The documentation must include:
- **Overview** of the code
- **Classes** and their purpose
- **Functions/Methods** with parameters, return values, and exceptions
- **Usage examples**
- **Limitations/edge cases**

Do **not** modify the code. Only describe it.

Begin!

Code to document:
{input}

Final Answer (Markdown documentation only):
"""
)

# Create a simple agent with no tools (just an LLM following the prompt)
agent = create_react_agent(
    llm=llm,
    tools=[],   # ✅ no tools
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    return_intermediate_steps=False  # ✅ we only want final docs
)

class CodeDocumentationAgent:
    def __init__(self, agent, executor):
        self._agent = agent
        self._executor = executor
    
    def run_task(self, code: str):
        """Run the code documentation task with the given code input."""
        try:
            response = self._executor.invoke({"input": code})
            return response["output"] + "\n" + "-" * 50 + "\n"
        except Exception as e:
            return f"⚠️ Error while running task: {str(e)}\n"

def getAgent():
    return CodeDocumentationAgent(agent, agent_executor)