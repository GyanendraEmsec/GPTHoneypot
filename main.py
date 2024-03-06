import openai
from openai import OpenAI

openai.api_key = "sk-jlHxIRaDhOmOSj5Xj4KXT3Blbkxxxxxxxxxxxxxxxxxxxxxxxxxx"

paymentPrompt = """I want you to act as a Pyment Gateway service.
I will type card number,cardholder's name, expiry date, CVV, and you will reply with the result.Show each process in new line.

Question: """

sqlPrompt = """I want you to act as a SQL service.
I will type SQL query, and you will reply with the result.

Question: """

mongoDBPrompt = """I want you to act as a MongoDB service.
I will type MongoDB query, and you will reply with the result.

Question: """

elasticsearchPrompt = """I want you to act as a Elasticsearch service.
I will type Elasticsearch query, and you will reply with the result.

Question: """

redisPrompt = """I want you to act as a Redis service.
I will type Redis query, and you will reply with the result.

Question: """

PostgreSQLPrompt = """I want you to act as a PostgreSQL service.
I will type PostgreSQL query, and you will reply with the result.

Question: """

service = input("Select the service: ")

prompt = ""
syntaxAnalyzer = ""

# Map the selected service to the respective prompt and syntax analyzer
if service == "MySql":
    prompt = sqlPrompt
    syntaxAnalyzer = 'Check the MySql syntax of this query and give error like MySql service: '
elif service == "mongoDB":
    prompt = mongoDBPrompt
    syntaxAnalyzer = 'Check the mongoDB syntax of this query and give error like mongoDB service: '
elif service == "elasticsearch":
    prompt = elasticsearchPrompt
    syntaxAnalyzer = 'Check the elasticsearch syntax of this query and give error like elasticsearch service: '
elif service == "Redis":
    prompt = redisPrompt
    syntaxAnalyzer = 'Check the Redis syntax of this query and give error like Redis service: '
elif service == "PostgreSQL":
    prompt = PostgreSQLPrompt
    syntaxAnalyzer = 'Check the PostgreSQL syntax of this query and give error like PostgreSQL service: '
elif service == "payment":
    prompt = paymentPrompt
else:
    # Default to SQL prompt if service is not recognized
    prompt = sqlPrompt
    syntaxAnalyzer = 'Check the MySql syntax of this query and give error like MySql service: '

# Initialize the language model
client = OpenAI(api_key="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")
# llm = client.completions.create(model="text-davinci-003")

while True:
    query = input("> ")
    if query == 'exit':
        print('Bye!')
        break
    
    if syntaxAnalyzer:
        isValid = client.completions.create(model="gpt-3.5-turbo-instruct" , prompt=syntaxAnalyzer + query)
        test_list = ["OK", "Ok", "Correct", "No Error", "No error", "No Errors", "No errors"]
        res = any(ele in isValid.choices[0].text for ele in test_list)
        
        if not res and service != 'MySql':
            res = True

        if res:
            prompt += query + "\nAnswer:\n"
            answer = client.completions.create(model="gpt-3.5-turbo-instruct" , prompt=prompt)
            print(answer.choices[0].text)
        else:
            print(isValid.choices[0].text)
    else:
        answer = client.completions.create(model="gpt-3.5-turbo-instruct" ,prompt=prompt + query + "\nAnswer:\n")
        print(answer.choices[0].text)

    print("\n\n")
