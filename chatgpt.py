import pandas as pd
import openai
import yaml

from strings import strip_code_block

# Load in config.yaml
with open('config.yaml', 'r') as file:
    yaml_dict = yaml.full_load(file)
    azure_keys = yaml_dict.get('azure_openai')
    AZURE_OPENAI_API_KEY = azure_keys.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = azure_keys.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = azure_keys.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_VERSION = azure_keys.get('AZURE_OPENAI_API_VERSION')

client = openai.AzureOpenAI(
  api_key = AZURE_OPENAI_API_KEY,
  api_version = AZURE_OPENAI_API_VERSION,
  azure_endpoint = AZURE_OPENAI_ENDPOINT
)

def execute_chatgpt_prompt(system_instructions, user_prompt):
    try:
        # Send the prompt to ChatGPT API
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,  # Or whichever engine you use
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=4000,  # Adjust token limit based on expected response size
            temperature=0.75,  # Control creativity
        )
        
        # Extract the response text
        generated_text = response.choices[0].message.content

        return generated_text
    except:
        pass
    return ""


def generate_code_from_user_question(metadata, sample_data, dataframe_name, user_question):
    column_names = metadata['columns']  # Assuming metadata contains column info
    description = metadata['description']
    shape = metadata['shape']
    
    system_instructions = f"""
    You are an assistant that helps generate python code.

    You are given the following dataset:
    Description: {description}
    Columns: {', '.join(column_names)}
    Sample Data: {sample_data.to_string(index=False)}
    Shape: {shape}
    
    Based on this dataset, generate python code to help answer the user's question.
    In your python code, please refer to the dataset as a Pandas DataFrame that already exists with the name: {dataframe_name}.
    In your python code, make sure to import any packages you need.
    Do NOT use any comments in the code.
    The output of your code should result in a string of less than 800000 characters. Store this output in a variable called 'result'.
    In your response, not include any other text before or after the generated Python code in your response.
    """

    # Use OpenAI API or similar to generate a response based on the prompt
    response = execute_chatgpt_prompt(system_instructions=system_instructions, user_prompt=user_question)

    return strip_code_block(response)


def generate_chatbot_response(output, user_question):
    system_instructions = f"""
    The following data is the result of the query:
    {output}
    
    Please provide an intelligble and accurate response to the user's question based on the data.
    If a clear answer cannot be provided, specify where there are uncertainties or what other information would be needed to answer the user's question.
    """

    # Use OpenAI API or similar to generate a response based on the prompt
    response = execute_chatgpt_prompt(system_instructions=system_instructions, user_prompt=user_question)
    
    return response
