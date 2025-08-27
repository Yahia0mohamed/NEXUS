from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ..llm import llm

from agents.code_generator.CodeGeneratorAgent import getAgent as getCodeGenAgent
from agents.code_reveiwer.CodeReviewAgent import getAgent as getCodeReviewAgent
from agents.error_explainer.ErrorExplainerAgent import getAgent as getErrorExplainerAgent
from agents.code_documentor.CodeDocumentationAgent import getAgent as getCodeDocAgent



class NexusChatAgent:
    def __init__(self):
        self._agents={
            "generate": getCodeGenAgent(),
            "review": getCodeReviewAgent(),
            "error": getErrorExplainerAgent(),
            "doc": getCodeDocAgent()
        }
        _router_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are an intelligent router that decides which specialized agent should handle a query.

Agents available:
- "generate": for generating or creating new code
- "review": for reviewing, improving, or optimizing existing code
- "error": for explaining or fixing error messages, exceptions, or bugs
- "doc": for writing documentation, explaining code, or generating usage docs

User query: "{query}"

Answer ONLY with one word: generate, review, error, or doc.
"""
)
        self._router_chain = LLMChain(prompt=_router_prompt, llm=llm)

    def route(self, user_input: str) -> str:
        """Use LLM chain to decide which agent to use"""
        try:
            result = self._router_chain.run(query=user_input)
            route = result.strip().lower()
            if route in self._agents:
                return route
        except Exception:
            pass
        return "review"
    
    def chat(self, user_input: str) -> str:
        """Route query and forward it to the chosen agent"""
        agent_key = self.route(user_input)
        agent = self._agents[agent_key]

        # Assuming each agent has `run_task` or similar entrypoint
        response = agent.run_task(user_input)

        return f"🤖 [{agent_key.upper()} AGENT]:\n{response}"