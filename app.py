# app.py

import warnings
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from utils import get_openai_api_key, get_serper_api_key
from langchain_openai import ChatOpenAI

# Suppress warnings
warnings.filterwarnings('ignore')

# Retrieve API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["SERPER_API_KEY"] = serper_api_key

# Initialize tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Function to initialize agents
def create_agents():
    data_analyst_agent = Agent(
        role="Data Analyst",
        goal="Monitor and analyze market data in real-time to identify trends and predict market movements.",
        backstory="Specializing in financial markets, this agent uses statistical modeling and machine learning to provide crucial insights.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool]
    )

    trading_strategy_agent = Agent(
        role="Trading Strategy Developer",
        goal="Develop and test various trading strategies based on insights from the Data Analyst Agent.",
        backstory="Equipped with a deep understanding of financial markets and quantitative analysis.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool]
    )

    execution_agent = Agent(
        role="Trade Advisor",
        goal="Suggest optimal trade execution strategies based on approved trading strategies.",
        backstory="Specializes in analyzing the timing, price, and logistical details of potential trades.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool]
    )

    risk_management_agent = Agent(
        role="Risk Advisor",
        goal="Evaluate and provide insights on the risks associated with potential trading activities.",
        backstory="Scrutinizes potential risks and offers safeguards.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool]
    )

    return [data_analyst_agent, trading_strategy_agent, execution_agent, risk_management_agent]

# Function to create tasks
def create_tasks(agents):
    data_analysis_task = Task(
        description="Monitor and analyze market data for the selected stock.",
        expected_output="Insights and alerts about significant market opportunities.",
        agent=agents[0]
    )

    strategy_development_task = Task(
        description="Develop trading strategies based on insights and risk tolerance.",
        expected_output="Trading strategies aligned with user risk tolerance.",
        agent=agents[1]
    )

    execution_planning_task = Task(
        description="Analyze approved strategies and suggest best execution methods.",
        expected_output="Execution plans for trades.",
        agent=agents[2]
    )

    risk_assessment_task = Task(
        description="Evaluate risks of proposed trading strategies and plans.",
        expected_output="Comprehensive risk analysis report.",
        agent=agents[3]
    )

    return [data_analysis_task, strategy_development_task, execution_planning_task, risk_assessment_task]

# Main function to set up and run the Crew
def run_financial_analysis(stock_selection, initial_capital, risk_tolerance, trading_strategy_preference):
    agents = create_agents()
    tasks = create_tasks(agents)
    
    financial_trading_crew = Crew(
        agents=agents,
        tasks=tasks,
        manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
        process=Process.hierarchical,
        verbose=True
    )

    # Inputs for execution
    financial_trading_inputs = {
        'stock_selection': stock_selection,
        'initial_capital': initial_capital,
        'risk_tolerance': risk_tolerance,
        'trading_strategy_preference': trading_strategy_preference,
        'news_impact_consideration': True
    }

    # Run the Crew
    result = financial_trading_crew.kickoff(inputs=financial_trading_inputs)
    return result

if __name__ == "__main__":
    stock_selection = 'AAPL'
    initial_capital = '100000'
    risk_tolerance = 'Medium'
    trading_strategy_preference = 'Day Trading'
    result = run_financial_analysis(stock_selection, initial_capital, risk_tolerance, trading_strategy_preference)
    print(result)
