from ..llm import llm
from agents.error_explainer.error_tools import create_stackoverflow_tools
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent



tools = create_stackoverflow_tools(llm= llm)

prompt_template = """
You are an expert software debugging assistant. You specialize in analyzing error messages and providing comprehensive solutions.
You have access to the following tools:
{tools}
When a user presents an error, use the StackOverflowErrorAnalyzer tool to search for solutions and format them properly.
Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
Begin!
Question: {input}
Thought:{agent_scratchpad}
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["input", "agent_scratchpad"],
    partial_variables={
        "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
        "tool_names": ", ".join([tool.name for tool in tools])
    }
)


agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
    return_intermediate_steps=True
)

class ErrorExplainerAgent:
    def __init__(self, agent, executor):
        self._agent = agent
        self._executor = executor
    
    def run_task(self, error: str):
        """Run the code review task with the given code input."""
        try:
            # Run the agent
            response = self._executor.invoke({"input": error})
            return response['output'] + "-" * 50 + "\n"
            
        except Exception as e:
            print(f"⚠️ An error occurred while running the task: {str(e)}\n")


def getAgent():
    return ErrorExplainerAgent(agent, agent_executor)