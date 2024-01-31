from dotenv import dotenv_values

# Context window for GPT-3.5-Turbo
CONTEXT_WINDOW = 16300

# File size limit of 10 MB
FILE_SIZE_LIMIT = 10 * 1024 * 1024

# OpenAI model to use
MODEL_NAME = "gpt-3.5-turbo-1106"

# Load OPENAI_API_KEY from env variables
OPENAI_API_KEY = dotenv_values().get("OPENAI_API_KEY")
