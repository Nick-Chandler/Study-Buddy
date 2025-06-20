from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import UserFile, Embedding
from .utils import split_pages_to_binary_files, generate_embedding_for_pdf_page
import openai

@receiver(post_delete, sender=UserFile)
def delete_userfile_file(sender, instance, **kwargs):
  print("Fired post_delete signal for UserFile")
  if instance.file:
    instance.file.delete(save=False)

@receiver(post_save, sender=UserFile)
def create_embeddings_for_userfile(sender, instance, created, **kwargs):
  if not created:
    return

  # Read PDF binary content from the file
  instance.file.seek(0)
  pdf_binary = instance.file.read()

  # Split PDF into binary pages
  page_binaries = split_pages_to_binary_files(pdf_binary)

  # For each page, generate embedding and save to Embedding model
  for page_binary in page_binaries:
    embedding_data = generate_embedding_for_pdf_page(page_binary)
    Embedding.objects.create(
      file_id=instance,
      embedding=embedding_data
    )
