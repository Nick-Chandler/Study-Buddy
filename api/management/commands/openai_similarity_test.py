from django.core.management.base import BaseCommand
import openai
import numpy as np

class Command(BaseCommand):
  help = 'Compare similarity of two strings using GPT embeddings'

  def handle(self, *args, **options):

    s1 = "Lebron James birthplace"
    s2 = "Akron, Ohio"
    strings = [s1, s2]

    embeddings = [
      openai.embeddings.create(
        input=s,
        model="text-embedding-3-large"
      ).data[0].embedding
      for s in strings
    ]

    def cosine_similarity(a, b):
      a = np.array(a)
      b = np.array(b)
      return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    sim = cosine_similarity(embeddings[0], embeddings[1])
    with open("api/similarity_result.txt", "a") as f:
      f.write(f"Cosine similarity between '{strings[0]}' and '{strings[1]}' is: {sim}\n")
    print(f"Cosine similarity between '{strings[0]}' and '{strings[1]}' is: {sim}")
