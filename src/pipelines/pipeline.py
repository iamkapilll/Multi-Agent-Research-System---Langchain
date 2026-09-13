# ============================================================
# IMPORTS
# ============================================================

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)


# ============================================================
# RESEARCH PIPELINE
# ============================================================

def run_research_pipeline(topic: str) -> dict:

    # Dictionary to store everything produced by each step
    state = {}


    # ========================================================
    # STEP 1: SEARCH AGENT
    # ========================================================

    print("\n" + "=" * 50)
    print("STEP 1 - Search Agent is working...")
    print("=" * 50)

    # Create the Search Agent
    search_agent = build_search_agent()

    # Give the topic to the agent
    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    # Get the agent's final response
    state["search_results"] = search_result["messages"][-1].content

    print("\nSearch Results:\n", state["search_results"])


    # ========================================================
    # STEP 2: READER AGENT
    # ========================================================

    print("\n" + "=" * 50)
    print("STEP 2 - Reader Agent is scraping top resources...")
    print("=" * 50)

    # Create the Reader Agent
    reader_agent = build_reader_agent()

    # Give search results to the Reader Agent
    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Based on the following search results about '{topic}',
pick the most relevant URL and scrape it for deeper content.

Search Results:
{state["search_results"][:800]}
"""
            )
        ]
    })

    # Save scraped webpage content
    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped Content:\n", state["scraped_content"])


    # ========================================================
    # STEP 3: WRITER CHAIN
    # ========================================================

    print("\n" + "=" * 50)
    print("STEP 3 - Writer is drafting the report...")
    print("=" * 50)

    # Combine search results + scraped content
    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"

        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    # Send the combined research to the Writer
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal Report:\n", state["report"])


    # ========================================================
    # STEP 4: CRITIC
    # ========================================================

    print("\n" + "=" * 50)
    print("STEP 4 - Critic is reviewing the report...")
    print("=" * 50)

    # Send the generated report to the Critic
    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Report:\n", state["feedback"])


    # ========================================================
    # RETURN EVERYTHING
    # ========================================================

    return state