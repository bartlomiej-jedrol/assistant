import os
import json
import logging
from openai import OpenAI

import argparse

parser = argparse.ArgumentParser()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get the test argument
parser.add_argument('--test', action='store_true')
args = parser.parse_args()


def lambda_handler(event, context):
    """Sample pure Lambda function"""

    body = json.loads(event['body'])
    query = body['query']
    print(f'Query: {query}\n')

    messages = []
    messages.append(
        {
            'role': 'system',
            'content': """As an assistant you extract tags from a description of the url. Tags are separated by comma.
            examples```
            U: https://gist.github.com/JonnyDavies/4c0f23270d04fc0f4ea4e446ed8e496a aws sam running developing lambda locally including api gateway template.yaml
            A: aws,sam,lambda,api gateway,template.yaml            
            ```
            """,
        }
    )
    messages.append({'role': 'user', 'content': query})

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    completion = openai_client.chat.completions.create(
        messages=messages, model='gpt-4', temperature=0
    )
    response = completion.model_dump()
    llm_response = response['choices'][0]['message']['content']
    print(f"{llm_response}\n")

    return {'statusCode': 200, 'body': 'response'}


# Test the Lambda handler locally
if args.test:
    with open('events/event.json', 'r') as test_json:
        test_event = json.load(test_json)
    context = ''

    lambda_handler(event=test_event, context=context)
