from ..llm import llm
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
    template="""
You are a code reviewer assistant. Review the following code and optimize it to follow best practices **Markdown format**.
Ignore {tools} and {tool_names}, they are just placeholders.

Use the following format:
Question: The code to review
Thought: First, understand the purpose of the code. Always consider what improvements can be made.
Action: Optimize the code, suggest changes, and explain the reasoning behind them.
Action Input: The specific input to the action
Observation: The result of the action
... (this Thought/Action/Action Input/Observation cycle can repeat as needed)
Thought: I now know the final answer
Final Answer: The final answer to the original input question

Begin!
Question: {input}
Thought: {agent_scratchpad}
"""
)

agent = create_react_agent(
    llm=llm,
    tools=[],
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
    return_intermediate_steps=True
)

class CodeReviewAgent:
    def __init__(self, agent, executor):
        self._agent = agent
        self._executor = executor
    
    def run_task(self, code: str):
        """Run the code review task with the given code input."""
        try:
            # Run the agent
            response = self._executor.invoke({"input": code})
            return response['output'] + "-" * 50 + "\n"
            
        except Exception as e:
            print(f"⚠️ An error occurred while running the task: {str(e)}\n")

def getAgent():
    return CodeReviewAgent(agent, agent_executor)