from ..llm import llm
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate


prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
    template="""
You are a code generator. Generate the code, optimize it and follow best practices given requirments **Markdown format**.
Ignore {tools} and {tool_names}, they are just placeholders.

Use the following format:
Question: the code requirments
Thought: First, understand the requirments. Always consider best practices and software proficiency.
Action: Generate the code and explain the reasoning behind the generated code.
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

class CodeGeneratorAgent:
    def __init__(self, agent, executor):
        self._agent = agent
        self._executor = executor
    
    def run_task(self, requirments: str):
        """Run the code generation task with the given requirments input."""
        try:
            # Run the agent
            response = self._executor.invoke({"input": requirments})
            return response['output'] + "-" * 50 + "\n"
            
        except Exception as e:
            print(f"⚠️ An error occurred while running the task: {str(e)}\n")

def getAgent():
    return CodeGeneratorAgent(agent, agent_executor)