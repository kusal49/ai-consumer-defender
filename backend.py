
import os
from dotenv import load_dotenv

# LangChain Imports
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables once when the module is imported
load_dotenv()

def validate_keys():
    #Checks if API keys are present.
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY is missing in .env")
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY is missing in .env")

def get_legal_agent():
    
    #Initializes and returns the LangChain Agent Executor.
    
    # 1. Validate environment
    validate_keys()

    # 2. Define Tools
    # max_results=1 is enough for a legal check; prevents reading too much noise.
    search_tool = TavilySearchResults(
        max_results=1,
        search_depth="basic", 
        include_answer=True,
        include_raw_content=False
    )
    tools = [search_tool]

    # 3. Initialize LLM (Llama 3 via Groq)
    # This model is optimized for speed and works great for drafting letters.
    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.1-8b-instant", 
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # 4. System Prompt
    system_prompt = """
    You are a Consumer Rights Lawyer.
    
    INSTRUCTIONS:
    1. Search for the law ONCE.
    2. Even if the search result is not perfect, WRITE THE LETTER immediately based on what you found.
    3. NEVER search twice.
    4. If you cannot find the specific section, quote "General Consumer Rights".
    5.
    - TONE: Professional, firm, and authoritative. Avoid emotional language; rely on factual assertions and legal consequences.
    - LANGUAGE: Use assertive terminology such as "Material Breach," "Deficiency in Service," "Unfair Trade Practice," and "Time is of the Essence.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 5. Create Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # 6. Create Executor
    # verbose=True helps you see the "Thinking" process in the terminal
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        max_iterations=2,     # Stop after 2 steps (Search -> Write)
        handle_parsing_errors=True # Recover if Llama messes up JSON
    )
    return agent_executor