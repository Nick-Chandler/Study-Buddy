from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import UserFile, Chunk
import openai
from api import utils

@receiver(post_delete, sender=UserFile)
def delete_userfile_file(sender, instance, **kwargs):
  print("Fired post_delete signal for UserFile")
  if instance.file:
    print(instance.file.name)
    instance.file.delete(save=False)

@receiver(post_save, sender=UserFile)
def create_chunks_for_userfile(sender, instance, created, **kwargs):
  if not created:
    return
  
  # Extract text from the PDF file by page - List
  page_texts = utils.extract_text_per_page(instance)

  # For each page, generate embedding and save to Embedding model
  for i,text in enumerate(page_texts):
    embedding_vector = utils.generate_embedding_for_pdf_page(page_texts[i])
    Chunk.objects.create(
      file_id=instance,
      chunk_number=i + 1,
      text=text,
      embedding=embedding_vector,
    )
