from openai import OpenAI

def get_completion(prompt, model="gpt-3.5-turbo"):
  client = OpenAI(api_key='API_KEY')
  completion = client.chat.completions.create(
  model=model,
  messages=[{"role": "user", "content":prompt},])
  response = completion.choices[0].message.content
  return response

prompt = input("Enter Tweet:")
response = get_completion(prompt)
print(response)
