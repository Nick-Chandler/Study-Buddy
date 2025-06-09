from django.core.management.base import BaseCommand
import openai
import numpy as np

class Command(BaseCommand):
  help = 'Compare similarity of two strings using GPT embeddings'

  def handle(self, *args, **options):

    strings = ["Linear algebra is the branch of mathematics concerning linear equations such as linear maps such as and their representations in vector spaces and through matrices. Linear algebra is central to almost all areas of mathematics.",
    "In mathematics, specifically in linear algebra, matrix multiplication is a binary operation that produces a matrix from two matrices. For matrix multiplication, the number of columns in the first matrix must be equal to the number of rows in the second matrix. The resulting matrix, known as the matrix product, has the number of rows of the first and the number of columns of the second matrix. The product of matrices A and B is denoted as AB"]

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
