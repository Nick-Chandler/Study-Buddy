import tiktoken

# Choose encoding for your model (e.g., "cl100k_base" for GPT-3.5/4)
enc = tiktoken.get_encoding("cl100k_base")

text = """Large Language Models (LLMs) such as GPT-4, Claude, Gemini, and Llama have become foundational in today’s AI landscape, powering everything from chatbots and search engines to code assistants and creative tools. Their strengths and weaknesses are becoming more clear as adoption spreads and their limitations are explored in practical scenarios.

Strengths

First and foremost, LLMs are exceptional at understanding and generating natural language. They excel at producing coherent, contextually relevant, and fluent text, making them highly effective for tasks like text completion, summarization, translation, paraphrasing, and answering questions. Their ability to adapt style, tone, and vocabulary to suit different prompts is impressive, allowing them to simulate a wide range of personas or writing styles.

LLMs are also very strong at knowledge recall, especially for general facts, cultural references, and mainstream scientific or technical knowledge up to their training cutoff. They can provide solid answers to common questions across a huge variety of domains. Their breadth of coverage—due to exposure to massive, diverse datasets—means they can often handle unusual or ambiguous prompts gracefully, inferring user intent with minimal context.

For structured tasks like code generation, LLMs show notable capability, frequently producing functional code snippets in dozens of programming languages and frameworks. They can explain code, debug simple errors, and help users understand documentation or technical specifications. In creative contexts, LLMs can generate stories, poems, slogans, and brainstorming lists, providing inspiration or a starting point for human creators.

Finally, LLMs are powerful for multilingual applications. Modern models support translation, code-switching, and cross-lingual summarization for many languages, lowering barriers for international users.

Weaknesses

Despite these strengths, LLMs have notable weaknesses. A primary limitation is their reliance on static training data. They do not “know” about events or facts that emerged after their last update. This means their knowledge can quickly become stale, especially in fast-changing fields like current events, technology, or sports. While retrieval-augmented methods can help, most LLMs will confidently assert outdated or incorrect facts if not grounded with up-to-date information.

LLMs also tend to be weak at complex reasoning, logic puzzles, and mathematical problem-solving beyond basic algebra or arithmetic. Their answers may sound plausible but be incorrect, since they rely on pattern recognition, not true understanding or symbolic logic. This can lead to “hallucinations,” where the model fabricates details, citations, or technical information. When generating code, LLMs sometimes output code that looks right but fails in subtle ways or doesn’t run at all.

Another weakness is their limited ability to handle highly specialized, niche, or private knowledge that is underrepresented in their training data. They can struggle with ambiguity, multi-step instructions, or tasks requiring persistent memory or personal context across multiple sessions.

Bias is another major issue: LLMs can reflect and amplify societal biases present in their training data. They may produce stereotypical, insensitive, or otherwise inappropriate outputs unless carefully constrained or filtered.

Finally, LLMs lack true “understanding” or intentionality. They do not have beliefs, goals, or experiences—they predict words based on patterns. This limits their use in applications requiring genuine comprehension, trust, or ethical decision-making.

Conclusion

Overall, LLMs are powerful language tools with broad utility, especially for general knowledge, language tasks, and creative applications. However, their limitations in reasoning, up-to-date accuracy, bias, and true understanding must be recognized for responsible use."""

# Encode the string to tokens
tokens = enc.encode(text)

# Get the number of tokens
num_tokens = len(tokens)

print("Number of tokens:", num_tokens)
