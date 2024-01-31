import tiktoken

from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import (
    MapReduceDocumentsChain,
    ReduceDocumentsChain,
    StuffDocumentsChain,
)

from config import CONTEXT_WINDOW, MODEL_NAME, OPENAI_API_KEY
from prompts import map_template, reduce_template

# Encoder used by model, for counting tokens
encoder = tiktoken.get_encoding("cl100k_base")


# --------------------- Langchain Setup ---------------------

# Initialise OpenAI model with low temperature for reliable summarisations
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name=MODEL_NAME)

# Initialise map chain to be used whenever the file provided has content
# length that exceeds the context window for the model. Then, summarise
# each file chunk of size CONTEXT_WINDOW separately and then summarise
# the summaries in order to obtain the final result in the reduce chain
map_prompt = PromptTemplate.from_template(map_template)
map_chain = LLMChain(llm=llm, prompt=map_prompt)

# Initialise a reduce chain that takes the summaries and combines them
reduce_prompt = PromptTemplate.from_template(reduce_template)
reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

# Takes a list of documents, combines them into a single
# string, and passes this to an LLMChain
combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain, document_variable_name="docs"
)

# Combines and iteratively reduces the mapped documents
reduce_documents_chain = ReduceDocumentsChain(
    # This is final chain that is called.
    combine_documents_chain=combine_documents_chain,
    # If documents exceed context for `StuffDocumentsChain`
    collapse_documents_chain=combine_documents_chain,
    # The maximum number of tokens to group documents into.
    token_max=CONTEXT_WINDOW,
)

# Combining documents by mapping a chain over them, then combining results
map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_documents_chain,
    document_variable_name="docs",
    return_intermediate_steps=False,
)

# Text splitter for splitting long documents into chunks of CONTEXT_WINDOW
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=CONTEXT_WINDOW, chunk_overlap=0
)

# Initialise a chain for obtaining a summary when the document content
# fits in the CONTEXT_WINDOW, just summarise the document and return
llm_chain = LLMChain(llm=llm, prompt=map_prompt)
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="docs")
