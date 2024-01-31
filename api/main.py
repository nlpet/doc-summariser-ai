import uvicorn
import logging

from fastapi import FastAPI, File, UploadFile, HTTPException
from langchain.docstore.document import Document

from config import FILE_SIZE_LIMIT, CONTEXT_WINDOW
from tools import encoder, stuff_chain, map_reduce_chain, text_splitter

app = FastAPI()
logger = logging.getLogger("uvicorn.info")


@app.post("/api/summarise")
async def summarise(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        logger.warning(f"Invalid file type for file {file.filename} provided")
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Endpoint only supports .txt files",
        )

    content = await file.read()

    if len(content) > FILE_SIZE_LIMIT:
        raise HTTPException(status_code=413, detail="File too large")

    file.file.seek(0)
    content = content.decode("utf-8")
    n_tokens = len(encoder.encode(content))

    logger.info(f"Content provided has {n_tokens} tokens")

    if n_tokens > CONTEXT_WINDOW:
        logger.info("Running a map-reduce chain (content size exceeds context window)")
        n_calls = round(n_tokens / CONTEXT_WINDOW)

        if n_calls >= 5:
            logger.info("This may take a while, going to run {n_calls} map jobs")

        chain = map_reduce_chain
        docs = [
            Document(page_content=t, metadata={"source": "local"})
            for t in text_splitter.split_text(content)
        ]
    else:
        logger.info("Running a summarisation chain")
        chain = stuff_chain
        docs = [Document(page_content=content, metadata={"source": "local"})]

    try:
        result = chain.invoke(docs)
        logger.info(result["output_text"])
    except Exception as exc:
        logger.error(f"Could not obtain summary: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    return {"filename": file.filename, "summary": result["output_text"]}


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s"

    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)
