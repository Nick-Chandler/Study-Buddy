from django.core.management.base import BaseCommand
import openai
import csv
import api.models

class Command(BaseCommand):
  help = 'Retrieve all messages for a given OpenAI thread and write only the text content to messages.csv'

  def handle(self, *args, **kwargs):

    try:
      assistant = api.models.OpenAIAssistant.objects.filter(model="gpt-4.1-mini").first()
      assistant_id = assistant.assistant_id
      print(f"Updating assistant with ID: {assistant_id}")
      if not assistant_id:
        print("No assistant found with the specified model.")
        return
      new_instructions = """
        You are helpful with general knowledge questions and queries.

        When formatting your responses, use markdown for all structure and styling:
        - Use **bold** and *italics* for emphasis.
        - Use numbered or bulleted lists where appropriate.
        - For code examples, use fenced code blocks with the correct language specified (e.g., ```python).
        - For math equations:
          - Use single dollar signs $...$ for inline math.
          - Use double dollar signs $$...$$ for display (block) math.
          - Write equations using standard LaTeX syntax.
        - Only use markdown, do not use HTML.

        IMPORTANT:  
        Do NOT use \( ... \) or \[ ... \] for math. ONLY use $ ... $ for inline math and $$ ... $$ for block math.

        **For example:**
        Incorrect: (A+B)^2 = (B+A)^2  
        Incorrect: \((A+B)^2 = (B+A)^2\)  
        Correct: $$(A+B)^2 = (B+A)^2$$

        Your responses will be rendered using ReactMarkdown and KaTeX, so formatting must follow these conventions for proper display.
        """

      openai.beta.assistants.update(
        assistant_id,
        instructions=new_instructions
      )
      
      assistant.instructions = new_instructions
      assistant.save()
      self.stdout.write(self.style.SUCCESS(f"Assistant {assistant_id} updated successfully."))
      self.stdout.write(self.style.SUCCESS(f"New Assistant Instructions {assistant.instructions} updated successfully."))
    except Exception as e:
      self.stdout.write(self.style.ERROR(f"Error updating assistant {assistant_id}: {e}"))
      return
      
