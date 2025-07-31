from django.core.management.base import BaseCommand
import openai
import numpy as np

class Command(BaseCommand):
  help = 'Compare similarity of two strings using GPT embeddings'

  def handle(self, *args, **options):

    s1 = """Rory McIlroy's third-round charge at the Open Championship was derailed in bizarre fashion Saturday when he unwittingly performed a trick shot at the 11th hole.

          With one swish of his club, McIlroy not only hit his designated ball out of the rough to the right of the fairway but also dug out another ball that had been buried underneath the turf.

          The second ball popped out of the ground, much to McIlroy's surprise. He picked it up and held it out in front of him, looking confused. "I have another golf ball," he said with a smile to those around him.

          McIlroy then laughed it off and tossed the mystery ball into a nearby bush. NBC Sports commentator and former caddie John Wood said a stunned McIlroy asked him if he had ever seen anything like it.

          His shot wound up being a poor one, not even reaching the green, and he couldn't get up and down for par. The bogey -- the first of his round -- dropped him to 2 under for the day and 5 under for the tournament at Royal Portrush.

          He rebounded from the bizarre moment with an eagle at No. 12 that drew a roar from the crowd.

          McIlroy birdied three of his first four holes then settled for all pars until the surprising moment on the 11th."""
    
    s2 = "Rory McIlroy's bad shot at the Open Championship"
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
