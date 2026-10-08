import os
import asyncio
import time

from dotenv import load_dotenv
from crewai import LLM, Agent, Task, Process, Crew
from crewai_tools import SerperDevTool, FileReadTool


# Fixing for Groq + CrewAI cache_breakpoint issue
import crewai.llms.cache as crewai_cache
crewai_cache.mark_cache_breakpoint = lambda msg : msg


def get_sleep(output):
    time.sleep(100)

load_dotenv()
search_tool = SerperDevTool(max_usage_count=1)
file_tool = FileReadTool()

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key = os.getenv("GROQ_API_KEY"),
    temperature = 0.3
)

# def llm():
#     time.sleep(80)

#     return LLM(
#             model="groq/openai/gpt-oss-120b",
#             api_key = os.getenv("GROQ_API_KEY"),
#             temperature = 0.3
#         )

# response = llm.call("what is AI in 10 words?")
# print(response)



# Agent :- 1
researcher = Agent(
    role = "Senior Research Agent",
    goal = " Research the  topic and collect accurate, useful information.",
    backstory = (
        "You are an expert researcher. You collect key facts, trends, examples, and references from reliable sources."
    ),
    tools = [search_tool, file_tool],
    llm=llm,
    verbose = True
)


#Agent :- 2
analyst = Agent(
    role = "Content Analyst Agent",
    goal = "Analyze the research and extract the most important insights.",
    backstory = (
        "You are  an expert content strategist. You convert raw research into structured insights, key points, and a clear content uotline."
    ),
    llm = llm,
    verbose = True
)


#Agent :- 3
writer = Agent(
    role = "Blog writer Agent",
    goal = " Write a begineerpfriendly blog post from the analyzed insights.",
    backstory = (
        "You are clear and practical blog writer. You explain complex topics in simple language with examples."
    ),
    llm = llm,
    verbose = True
)

#agent :- 4
editor = Agent(
    role = "Editor Agent",
    goal = "Improve clarity, gramar, flow, and final presentation",
    backstory = (
        "You are an experinced editor. You polish content and make it easy to read, structured, and professional."
    ),
    llm = llm,
    verbose = True
)


def build_blog_crew(topic : str):
    research_task = Task(
        description= (
            f"Research the topic: {topic}, collect important facts, use cases, bigineer-friendly examples, and useful references."
        ),
        expected_output= (
            "A structured research summary with key facts, examples, use cases, and references."
        ),
        agent= researcher,
        callback=get_sleep
    )

    analysis_task = Task(
        description=(
            f"Analyze the research for the topic: {topic}. Create a clear blog outline with key sections and main points."
        ),
        expected_output=(
            "A blog outline with introduction, main sections, examples and collections, and not reach above 5000"
        ),
        agent= analyst,
        context=[research_task],
        callback=get_sleep
    )

    writing_task = Task(
        description=(
            f"write a complete beginner-friendly blog post on: {topic}. Use the outline and research. keep it simple, structured and practical."
        ),
        expected_output=(
            "A complete blog post with tittle, introductions, headings, examples, and conclusion. and not reach above 5000"
        ),
        agent= writer,
        context= [research_task, analysis_task],
        callback=get_sleep
    )


    editing_task = Task(
        description=(
            "Review and improve the blog post. Fix gramar, improve flow, make it more readable and add a strong final summary."
        ),
        expected_output=(
            "Final polished blog post ready to publish."
        ),
        agent= editor,
        context=[writing_task]
    )

    crew = Crew(
        agents= [ researcher, analyst, writer, editor],
        tasks= [research_task, analysis_task, writing_task, editing_task],
        process= Process.sequential,
        verbose=True
    )

    return crew

if __name__ == "__main__" :
    topic = input("Enter blog topic: ")
    crew = build_blog_crew(topic)

    result = asyncio.run(crew.kickoff_async())
    # result  = crew.kickoff()

    print("\n\n================================================Final Blog=======================================\n")
    print(result)