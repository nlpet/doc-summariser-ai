## Document Summarisation API

This API provides AI generated summaries of documents. It uses langchain and OpenAI's GPT-3.5-Turbo by default. It creates a summarisation chain if the document length if within the context window of the model (16k tokens), or it utilises a map-reduce chain if it exceeds the context window. In the latter case, the document is split into chunks of at most `CONTEXT_WINDOW` length and each one is summarised individually and then the summaries are summarised to obtain the final result.

### Prerequisites

Before you begin, make sure you are in a Python virtual environment. This app has been tested with Python version 3.11.

The app requires an `OPENAI_API_KEY` to be present in the `.env` file.

### Usage

To run the app locally:

```
make install
make run
```

once running, you can request summaries from the app with:

```bash
curl -X POST "http://0.0.0.0:8000/api/summarise"  \
     -H "accept: application/json"  \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/example.txt"
```

and with Python using `requests`

```python
import requests

url = "http://0.0.0.0:8000/api/summarise"
files = {"file": open("example.txt", "rb")}

response = requests.post(url, files=files)
response.json()
```

### Docker Usage

To run the app in a docker container, run the following

```
make docker-run
```

this will create a docker container using the `Dockerfile` and run it.

Then, to request a summary with CURL from the app running in the docker container

```bash
curl -X POST "http://0.0.0.0:80/api/summarise"  \
     -H  "accept: application/json"  \
     -H  "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/example.txt"
```

and with Python using `requests`

```python
import requests

url = "http://0.0.0.0:80/api/summarise"
files = {"file": open("example.txt", "rb")}

response = requests.post(url, files=files)
response.json()
```

To clean up the docker container:

```
make docker-clean
```

### Testing

To run the tests

```
make test
```

note that the tests require the `OPENAI_API_KEY` to be provided and may take ~40s to run, depending on how responsive the OpenAI's API is.

### Deployment

The application can easily be deployed as a docker container after the steps above have been run. The container can be uploaded to a container registry and then deployed in a cloud environment.
