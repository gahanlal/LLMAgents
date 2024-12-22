import openai
import requests
from bs4 import BeautifulSoup


class PromptAgent:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.prompts = []  # Store original and refined prompts
        self.feedback = ""  # Initialize feedback as an empty string

    def get_user_input(self):
        print("Please enter the initial prompt:")
        self.prompts.append(input("> "))  # Store the initial prompt

    def explain_prompt(self):
        print(f"Initial prompt:")
        print(self.prompts[-1])
        print("This prompt will be refined to guide a language model effectively based on the frameworks provided.")

    def get_feedback_input(self):
        print("Please provide feedback on the prompt:")
        self.feedback = input("> ")

    def web_search(self, query):
        print("Searching the web for additional information...")
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = []

            for result in soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd"):
                search_results.append(result.get_text())

            return search_results[:5]  # Return the top 5 search results
        else:
            print("Failed to fetch search results.")
            return []

    def refine_prompt_initial(self):
        print("Refining prompt with OpenAI for the first time...")

        initial_prompt = self.prompts[0]  # Use the initial prompt given by the user
        search_results = self.web_search(initial_prompt)
        additional_info = " ".join(search_results)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",  # Specify the chat model you want to use
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an experienced Prompt Maker Agent tasked with refining prompts for a language model to generate high-quality responses based on user initial prompt.\n\n"
                        "Select the best structure of the framework provided additional info and initial prompt given by the user:\n"
                        "1. APE: Action, Purpose, Expectation\n"
                        "   - Action: Define the job or activity to be done.\n"
                        "   - Purpose: Discuss the intention or goal.\n"
                        "   - Expectation: State the desired outcome.\n\n"
                        "2. RACE: Role, Action, Context, Expectation\n"
                        "   - Role: Specify the role of ChatGPT.\n"
                        "   - Action: Detail what action is needed.\n"
                        "   - Context: Provide relevant details of the situation.\n"
                        "   - Expectation: Describe the expected outcome.\n\n"
                        "3. COAST: Context, Objective, Actions, Scenario, Task\n"
                        "   - Context: Set the stage for the conversation.\n"
                        "   - Objective: Describe the goal.\n"
                        "   - Actions: Explain the actions needed.\n"
                        "   - Scenario: Describe the scenario.\n"
                        "   - Task: Describe the task.\n\n"
                        "4. TAG: Task, Action, Goal\n"
                        "   - Task: Define the specific task.\n"
                        "   - Action: Describe what needs to be done.\n"
                        "   - Goal: Explain the end goal.\n\n"
                        "5. RISE: Role, Input, Steps, Expectation\n"
                        "   - Role: Specify the role of ChatGPT.\n"
                        "   - Input: Describe the information or resources.\n"
                        "   - Steps: Ask for detailed steps.\n"
                        "   - Expectation: Describe the desired result.\n\n"
                        "6. TRACE: Task, Request, Action, Context, Example\n"
                        "   - Task: Define the specific task.\n"
                        "   - Request: Describe what you are asking for.\n"
                        "   - Action: State the action you need.\n"
                        "   - Context: Provide the context or situation.\n"
                        "   - Example: Give an example to illustrate your point.\n\n"
                        "7. ERA: Expectation, Role, Action\n"
                        "   - Expectation: Describe the desired result.\n"
                        "   - Role: Specify the role of ChatGPT.\n"
                        "   - Action: Specify what actions need to be taken.\n\n"
                        "8. CARE: Context, Action, Result, Example\n"
                        "   - Context: Set the stage or context for the discussion.\n"
                        "   - Action: Describe what you want to be done.\n"
                        "   - Result: Describe the desired outcome.\n"
                        "   - Example: Give an example to illustrate your point.\n\n"
                        "9. ROSES: Role, Objective, Scenario, Expected Solution, Steps\n"
                        "   - Role: Specify ChatGPT's role.\n"
                        "   - Objective: State the goal or aim.\n"
                        "   - Scenario: Describe the situation.\n"
                        "   - Solution: Define the desired outcome.\n"
                        "   - Steps: Ask for actions needed to reach the solution.\n"
                        "10.TAG: Task, Action, Goal"
                        "   - Task: Clearly state what you need.\n"
                        "   - Define the Action: Specify how ChatGPT should approach the task.\n"
                        "   - End with the Goal: Make sure ChatGPT knows why you're asking for this task.\n"
                        "11.COSTAR: Objective, Style, Tone, Audience, Response"
                        "   - Objective: Clearly defining the task directs the LLM’s focus.\n"
                        "   - Style: Specifying the desired writing style aligns the LLM response.\n"
                        "   - Tone: Setting the tone ensures the response resonates with the required sentiment.\n"
                        "   - Audience: Identifying the intended audience tailors the LLM’s response to be targeted to an audience.\n"
                        "   - Response: Providing the response format, like text or json, ensures the LLM outputs, and help build pipelines.\n "
                        "12.RTF: Role, Task, Format"
                        "   - Role: Defining the “Character” of the AI\n"
                        "   - Task: Outlining the Desired Action\n"
                        "   - Format: Structuring the Response\n\n"
                        "When you have selected the framework, make it as detailed as possible which should cover everything to make the response the best. "
                        "It is mandatory to explain why you chose the framework that you decided to use for the refinement"
                        "Use the additional info from web search to cover parts which the coder might have missed when making the prompt."
                        "Based on these frameworks, refine the initial prompt considering the user's feedback to ensure it is clear, comprehensive, and aligned with expectations.\n\n"
                        f"Initial prompt: {initial_prompt}\n\n"
                        f"Additional information from web search: {additional_info}"
                    )
                },
            ],
            max_tokens=15000,  # Adjust based on the expected length of the response
            temperature=0.7,  # Adjust based on the desired creativity of the response
            stop=None  # Adjust based on any custom stopping conditions
        )

        if 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
            refined_prompt = response['choices'][0]['message']['content'].strip()
            self.prompts.append(refined_prompt)  # Store the refined prompt
            print("Refined prompt:")
            print(refined_prompt)
        else:
            print("Unexpected response format from OpenAI API.")
            print(response)  # Print the entire response for debugging

    def refine_prompt_with_feedback(self):
        print("Refining prompt with OpenAI using feedback...")

        initial_prompt = self.prompts[0]  # Use the initial prompt given by the user
        recent_refined_prompt = self.prompts[-1]  # Use the most recent refined prompt

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",  # Specify the chat model you want to use
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an experienced Prompt Maker Agent tasked with refining prompts for a language model to generate high-quality responses based on user feedback.\n\n"
                        "Select the best structure of the framework provided, for usecase , additional info and initial prompt given by the user:\n"
                        "1. APE: Action, Purpose, Expectation\n"
                        "   - Action: Define the job or activity to be done.\n"
                        "   - Purpose: Discuss the intention or goal.\n"
                        "   - Expectation: State the desired outcome.\n\n"
                        "2. RACE: Role, Action, Context, Expectation\n"
                        "   - Role: Specify the role of ChatGPT.\n"
                        "   - Action: Detail what action is needed.\n"
                        "   - Context: Provide relevant details of the situation.\n"
                        "   - Expectation: Describe the expected outcome.\n\n"
                        "3. COAST: Context, Objective, Actions, Scenario, Task\n"
                        "   - Context: Set the stage for the conversation.\n"
                        "   - Objective: Describe the goal.\n"
                        "   - Actions: Explain the actions needed.\n"
                        "   - Scenario: Describe the scenario.\n"
                        "   - Task: Describe the task.\n\n"
                        "4. TAG: Task, Action, Goal\n"
                        "   - Task: Define the specific task.\n"
                        "   - Action: Describe what needs to be done.\n"
                        "   - Goal: Explain the end goal.\n\n"
                        "5. RISE: Role, Input, Steps, Expectation\n"
                        "   - Role: Specify the role of ChatGPT.\n"
                        "   - Input: Describe the information or resources.\n"
                        "   - Steps: Ask for detailed steps.\n"
                        "   - Expectation: Describe the desired result.\n\n"
                        "6. TRACE: Task, Request, Action, Context, Example\n"
                        "   - Task: Define the specific task.\n"
                        "   - Request: Describe what you are asking for.\n"
                        "   - Action: State the action you need.\n"
                        "   - Context: Provide the context or situation.\n"
                        "   - Example: Give an example to illustrate your point.\n\n"
                        "7. ERA: Expectation, Role, Action\n"
                        "   - Expectation: Describe the desired result.\n"
                        "   - Role: Specify the role of ChatGPT.\n"
                        "   - Action: Specify what actions need to be taken.\n\n"
                        "8. CARE: Context, Action, Result, Example\n"
                        "   - Context: Set the stage or context for the discussion.\n"
                        "   - Action: Describe what you want to be done.\n"
                        "   - Result: Describe the desired outcome.\n"
                        "   - Example: Give an example to illustrate your point.\n\n"
                        "9. ROSES: Role, Objective, Scenario, Expected Solution, Steps\n"
                        "   - Role: Specify ChatGPT's role.\n"
                        "   - Objective: State the goal or aim.\n"
                        "   - Scenario: Describe the situation.\n"
                        "   - Solution: Define the desired outcome.\n"
                        "   - Steps: Ask for actions needed to reach the solution.\n"
                        "10.TAG: Task, Action, Goal"
                        "   - Task: Clearly state what you need.\n"
                        "   - Define the Action: Specify how ChatGPT should approach the task.\n"
                        "   - End with the Goal: Make sure ChatGPT knows why you're asking for this task.\n"
                        "11.COSTAR: Objective, Style, Tone, Audience, Response"
                        "   - Objective: Clearly defining the task directs the LLM’s focus.\n"
                        "   - Style: Specifying the desired writing style aligns the LLM response.\n"
                        "   - Tone: Setting the tone ensures the response resonates with the required sentiment.\n"
                        "   - Audience: Identifying the intended audience tailors the LLM’s response to be targeted to an audience.\n"
                        "   - Response: Providing the response format, like text or json, ensures the LLM outputs, and help build pipelines.\n "
                        "12.RTF: Role, Task, Format"
                        "   - Role: Defining the “Character” of the AI\n"
                        "   - Task: Outlining the Desired Action\n"
                        "   - Format: Structuring the Response\n\n"
                        "When you have selected the framework, make it as detailed as possible which should cover everything to make the response the best. "
                        "It is mandatory to explain why you chose that framework"
                        "Based on these frameworks, refine the initial prompt considering the user's feedback to ensure it is clear, comprehensive, and aligned with expectations.\n\n"
                        f"Initial prompt: {initial_prompt}\n"
                        f"Most recent refined prompt: {recent_refined_prompt}\n"
                        f"User feedback: {self.feedback}"
                    )
                },
            ],
            max_tokens=12000,  # Adjust based on the expected length of the response
            temperature=0.7,  # Adjust based on the desired creativity of the response
            stop=None  # Adjust based on any custom stopping conditions
        )

        if 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
            refined_prompt = response['choices'][0]['message']['content'].strip()
            self.prompts.append(refined_prompt)  # Store the refined prompt
            print("Refined prompt:")
            print(refined_prompt)
        else:
            print("Unexpected response format from OpenAI API.")
            print(response)  # Print the entire response for debugging

    def get_user_feedback(self):
        print("Are you satisfied with the prompt? (y/n)")
        feedback = input("> ").lower()
        if feedback == "y":
            print("Great! Your prompt is finalized.")
            print("Final prompt:")
            print(self.prompts[-1])  # Show the most recent prompt
            return True
        elif feedback == "n":
            self.get_feedback_input()  # Get detailed feedback from the user
            self.refine_prompt_with_feedback()  # Refine the prompt with feedback
            print("Updated refined prompt:")
            print(self.prompts[-1])  # Show the refined prompt
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
            return self.get_user_feedback()

    def interact(self):
        self.get_user_input()
        self.explain_prompt()
        self.refine_prompt_initial()  # Initial refinement without feedback
        satisfied = False
        while not satisfied:
            satisfied = self.get_user_feedback()


# Usage
api_key = ''
agent = PromptAgent(api_key)
agent.interact()
