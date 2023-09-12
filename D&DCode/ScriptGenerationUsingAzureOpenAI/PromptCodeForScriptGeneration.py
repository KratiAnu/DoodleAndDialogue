#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
openai.api_type = "azure"
openai.api_base = "https://qnadevoai.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = ""

response = openai.Completion.create(
  engine="gpt-35-turbo",
  prompt="You are comedian bot named mr bean.\n\n###\nUser: Write me four funny dialogs between couple discussing about monthly budget.\nmr bean:  \n(START) ## \nHusband: Honey, I think we need to start budgeting our money better.\nWife: Budgeting? You mean like when you buy a new gadget every month?\nHusband: Well, those are essential gadgets!\nWife: Essential for what? Turning our house into a tech museum?\n(END) ##\n\n###\nUser: Write me four funny dialogs between two friends talking about party.\nmr bean:  \n(START) ##\nJohn: Bro I’ve invited 17 people to watch a movie, would you come?\nBro: ok John, but why so many people?\nJohn: Because the DVD said “Only 18+ viewers.”\nBro: Wait, what?\n(END) ##\n\n### \nUser: Write me four funny dialogs between two birds on a tree discussing about their recent achievement\nmr bean: \n(START) ##\n",
  temperature=0.7,
  max_tokens=100,
  top_p=0.8,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["(END) ##"])

# print the response    
print(response.choices[0]['text'])
output = response.choices[0]['text'].split('\n')

final_output = []

for a in output:
    if(a is None or len(a.split(': '))<2):
       continue
    final_output.append(a.split(': ')[1])

print(final_output)