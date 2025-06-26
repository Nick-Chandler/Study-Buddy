import openai
from api import utils, models

def run_assistant2(user_id, thread_id, user_input, assistant, document_name, max_prompt_tokens=20000, debug=False):
  print("Starting run_assistant2 routine...")
  print("Using Assistant:", assistant.name, "with ID:", assistant.assistant_id, "and model:", assistant.model)
  print("thread_id", thread_id)
  #-----------------------------------------------------------#
  document = models.UserFile.objects.filter(user_id=user_id, filename=document_name).first()
  thread = models.OpenAIThread.objects.get(thread_id=thread_id, user_id=user_id)
  thread.save()
  chunks = document.chunk_similarity_scores(user_input, debug=True)
  relevalent_chunks = []
  context = create_context(chunks, user_input, threshold=0.9)
  msg = openai.beta.threads.messages.create(
  thread_id=thread_id,
  role='user',
  content=f""" Answer the following question to the best of your ability. 
  If needed use the context provided below if it will help you better answer the question:
  {user_input}

  ---context---
  {context}
  """
  )
  run = openai.beta.threads.runs.create(
      thread_id=thread_id,
      assistant_id=assistant.assistant_id,
      max_prompt_tokens=max_prompt_tokens
    )
  response = utils.get_latest_gpt_response(run, thread_id, print_all_messages=False)
  return response

  
def create_context(chunks,user_input, threshold=0.9):
  relevalent_chunks = []
  context = ""
  if chunks:
    print("Chunks Provided:", len(chunks))
    for chunk,sim in chunks:
      print("User Input:", user_input)
      print("Chunk:", chunk.text[:50], "...")
      print("Similarity Score:", sim)
      # If similarity scores are above a threshold, add chunk to content
      if sim > threshold:
        print(f"Adding chunk {chunk.chunk_number} to relevant chunks...")
        relevalent_chunks.append(chunk.text)
    #-----------------------------------------------------------#
  # combine all relevant chunks into a single content string
  if relevalent_chunks:
    context = "\n\n---chunk---\n\n".join(chunks)
    print("Combined Context Length:", len(context))
  return context