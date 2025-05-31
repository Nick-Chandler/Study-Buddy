import openai
import base64
import requests
import boto3

# Set up S3 client
# See Notepad

# S3 bucket and key
bucket_name = 'study-buddy-app'
s3_key = 'uploads/Math_Concepts_Practice_Exam_1.pdf'  # the file's key inside S3
file = s3.download_file(bucket_name, s3_key, 'Math_Concepts_Practice_Exam_1.pdf')


response = openai.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "user", "content": [
      {"type": "text", "text": "Describe what's in this image."},
      { 'type': 'file', 'file_url': { 'url': url } }
    ]}
  ]
)

# Extract usage
prompt_tokens = response.usage.prompt_tokens
completion_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens

print(f"Prompt tokens: {prompt_tokens}")
print(f"Completion tokens: {completion_tokens}")
print(f"Total tokens: {total_tokens}")
# Print the response
print("Response:", response.choices[0].message.content)