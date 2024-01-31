import requests

URL = "http://0.0.0.0:8000/api/summarise"


def test_invalid_file_type():
    files = {"file": open("data/monocle.md", "rb")}
    response = requests.post(URL, files=files)
    result = response.json()
    assert response.status_code == 400
    assert result["detail"] == "Invalid file type. Endpoint only supports .txt files"


def test_stuff_chain():
    files = {"file": open("data/black_hole.txt", "rb")}
    response = requests.post(URL, files=files)
    result = response.json()
    assert response.status_code == 200
    assert "black hole" in result["summary"].lower()


def test_map_reduce_chain():
    files = {"file": open("data/tiny_shakespeare.txt", "rb")}
    response = requests.post(URL, files=files)
    result = response.json()
    assert response.status_code == 200
    assert "Coriolanus" in result["summary"]
