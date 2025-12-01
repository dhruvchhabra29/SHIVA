import google.generative_ai as genai
import os

# CONFIGURATION
#Kaggle Secrets or environment variables for API Keys.
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=GOOGLE_API_KEY)

# CONCEPT 1: TOOLS (A simple calculator tool)
def calculator(expression):
    """Evaluates a mathematical expression."""
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"

tools = [calculator]

# CONCEPT 2: MULTI-AGENT / SYSTEM PROMPTS (Context Engineering)
# We define specific roles for the model to act as "Agents"

planner_prompt = """
You are the SHIVA Planner Agent.
Your goal is to break down a user request into logical steps.
If the user asks for a calculation, output the math expression clearly.
"""

executor_prompt = """
You are the SHIVA Executor Agent.
You have access to a calculator tool.
Take the plan provided and execute the necessary actions to give the user a final answer.
"""

# SIMULATING THE AGENT WORKFLOW
def run_shiva_agent(user_input):
    print(f"--- User Input: {user_input} ---")

    # Step 1: Planner Agent
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=planner_prompt)
    plan_response = model.generate_content(user_input)
    print(f"--- Planner Output: {plan_response.text} ---")

    # Step 2: Executor Agent (with Tool use)
    # Note: In a real ADK, this is automated. Here we simulate the handoff for the hackathon.
    executor_model = genai.GenerativeModel(
        'gemini-2.5-flash',
        tools=tools,
        system_instruction=executor_prompt
    )

    # Pass the plan + context to the executor
    chat = executor_model.start_chat(enable_automatic_function_calling=True)
    final_response = chat.send_message(f"Execute this plan: {plan_response.text}")

    print(f"--- SHIVA Output: {final_response.text} ---")
    return final_response.text

# RUN IT
# This demonstrates the "Concierge" aspect
run_shiva_agent("I need to split a dinner bill of $150 between 4 people. How much is that?")
