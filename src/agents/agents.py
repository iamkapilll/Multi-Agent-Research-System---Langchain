# ============================================================
# IMPORTS
# ============================================================

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Our custom tools
from src.tools.tools import web_search, scrape_url

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

# Loads GROQ_API_KEY and other variables from .env
load_dotenv()


# ============================================================
# MODEL INITIALIZATION
# ============================================================

# Using Groq instead of OpenAI
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ============================================================
# 1st AGENT: SEARCH AGENT
# ============================================================

def build_search_agent():

    return create_agent(
        model=llm,

        # This agent can ONLY use the web search tool
        tools=[web_search],
    )


# ============================================================
# 2nd AGENT: READER AGENT
# ============================================================

def build_reader_agent():

    return create_agent(
        model=llm,

        # This agent can scrape/read webpages
        tools=[scrape_url],
    )


# ============================================================
# WRITER CHAIN
# ============================================================

# Prompt for converting collected research into a report
writer_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        "You are an expert research writer. "
        "Write clear, structured and insightful reports."
    ),

    (
        "human",
        """Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""
    ),
])



# Prompt → LLM → String output
writer_chain = (
    writer_prompt | llm | StrOutputParser()
)


# ============================================================
# CRITIC CHAIN
# ============================================================

# Prompt for checking the quality of the generated report
critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        "You are a sharp and constructive research critic. "
        "Be honest and specific."
    ),

    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""
    ),
])


# Prompt → LLM → String output
critic_chain = (
    critic_prompt | llm | StrOutputParser()
) 