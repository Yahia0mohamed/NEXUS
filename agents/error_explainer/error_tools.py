from ddgs import DDGS
from langchain.tools import Tool

class StackOverflowErrorAnalyzer:
    def __init__(self, llm):
        self.llm = llm
        self.search = DDGS()
    
    def search_stackoverflow_error(self, error_message: str) -> str:
        """
        Search for error solutions on StackOverflow and format into 4 main points
        """
        try:
            # Enhanced search query for StackOverflow
            search_query = f"site:stackoverflow.com {error_message} solution"
            
            # Get search results
            search_results = self.search.run(search_query)
            
            # Format the analysis prompt
            analysis_prompt = f"""
            Based on the following search results about the error "{error_message}", 
            please analyze and format the information into exactly 4 main points:

            Search Results:
            {search_results}

            Format your response as follows:

            **PROBLEM:**
            [Clearly describe what the error is and when it typically occurs]

            **EXPLANATION:**
            [Explain why this error happens and the underlying technical reasons]

            **SOLUTION:**
            [Provide the most effective solution(s) to fix this error]

            **HOW TO AVOID:**
            [List preventive measures and best practices to avoid this error in the future]

            Make each section concise but comprehensive. Focus on practical, actionable information.
            """
            
            # Get LLM analysis
            response = self.llm.invoke(analysis_prompt)
            
            return response.content
            
        except Exception as e:
            return f"Error analyzing StackOverflow results: {str(e)}"
    
    def search_general_programming_error(self, error_message: str, programming_language: str = "") -> str:
        """
        Search for programming error solutions with language specification
        """
        try:
            # Build search query
            if programming_language:
                search_query = f"site:stackoverflow.com {programming_language} {error_message} solution fix"
            else:
                search_query = f"site:stackoverflow.com {error_message} programming solution fix"
            
            search_results = self.search.run(search_query)
            
            analysis_prompt = f"""
            Analyze this {programming_language + ' ' if programming_language else ''}programming error: "{error_message}"
            
            Based on these StackOverflow search results:
            {search_results}
            
            Structure your analysis in exactly these 4 sections:

            **PROBLEM:**
            - What is this error?
            - When does it typically occur?
            - What are the symptoms?

            **EXPLANATION:**
            - Why does this error happen?
            - What are the underlying technical reasons?
            - What conditions trigger this error?

            **SOLUTION:**
            - Step-by-step fix for this error
            - Code examples if applicable
            - Alternative solutions if available

            **HOW TO AVOID:**
            - Best practices to prevent this error
            - Code patterns to follow
            - Tools or techniques for early detection

            Be specific and practical in your recommendations.
            """
            
            response = self.llm.invoke(analysis_prompt)
            return response.content
            
        except Exception as e:
            return f"Error in general programming error analysis: {str(e)}"

def create_stackoverflow_tools(llm):
    """Create StackOverflow analysis tools"""
    
    analyzer = StackOverflowErrorAnalyzer(llm)
    
    def stackoverflow_error_search(error_message: str) -> str:
        """Search StackOverflow for error solutions and format in 4 points"""
        return analyzer.search_stackoverflow_error(error_message)
    
    def programming_error_search(query: str) -> str:
        """
        Search for programming error with optional language specification.
        Format: 'error_message' or 'language: error_message'
        """
        if ': ' in query:
            language, error_message = query.split(': ', 1)
            return analyzer.search_general_programming_error(error_message, language.strip())
        else:
            return analyzer.search_stackoverflow_error(query)
    def duckduckgo_search(query: str) -> str:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                return "\n".join(f"{r['title']}: {r['href']}" for r in results)
        except Exception as e:
            return f"Search error: {str(e)}"
    
    return [
        Tool(
            name="StackOverflowErrorAnalyzer",
            description="Search StackOverflow for error solutions and format into Problem/Explanation/Solution/Prevention points. Input should be the error message or error code.",
            func=stackoverflow_error_search
        ),
        Tool(
            name="ProgrammingErrorSearch", 
            description="Search for programming error solutions with optional language specification. Format: 'python: IndexError' or just 'IndexError'",
            func=programming_error_search
        ),
        Tool(
            name="DuckDuckGoSearch",
            description="General-purpose web search using DuckDuckGo",
            func=duckduckgo_search
        ),  # Keep general search as backup
    ]