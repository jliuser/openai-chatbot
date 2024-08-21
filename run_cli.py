
# Example usage
import pandas as pd

from chatgpt import generate_chatbot_response, generate_code_from_user_question

full_dataset = pd.read_csv('DC_Public_Employee_Salary.csv')
sample_data = full_dataset.head(10)
metadata = {'description': 'this dataset contains salary data for public employees in DC',
            'columns': ['FIRST_NAME','LAST_NAME','JOBTITLE','DESCRSHORT','GRADE','COMPRATE','HIREDATE_STRING','GVT_TYPE_OF_APPT','OBJECTID'],
            'shape': full_dataset.shape}

while True:
    user_question = input("Enter a question or type 'exit' to end: ")
    if user_question.lower() == 'exit':
        break

    # Generate Code with OpenAI
    generated_code = generate_code_from_user_question(metadata, sample_data, "df", user_question)
    # print("Generated Code:\n", generated_code)

    try:
        # Execute the generated code
        namespace = {'df': full_dataset}
        exec(generated_code, namespace)

        # Retrieve the result
        if 'result' in namespace:
            result_df = namespace['result']
        else:
            result_df = None
    except:
        result_df = None

    # Generate Chatbot Response
    response = generate_chatbot_response(result_df, user_question)
    print(response)
