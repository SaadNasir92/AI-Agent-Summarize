# tests/test_tasks.py
import os
import tempfile
import pytest
from tasks import process_workflow
from llm import summarize_text


# Override the summarization function to avoid real API calls.
def dummy_summarize_text(text):
    return "dummy summary"


@pytest.fixture(autouse=True)
def override_summarize(monkeypatch):
    monkeypatch.setattr("llm.summarize_text", dummy_summarize_text)


# Create a dummy local connector class for testing.
class DummyLocalConnector:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def read_files(self):
        # Return a list of .txt files in the folder.
        return [
            os.path.join(self.folder_path, f)
            for f in os.listdir(self.folder_path)
            if f.endswith(".txt")
        ]

    def write_file(self, filename, content):
        with open(os.path.join(self.folder_path, filename), "w") as f:
            f.write(content)


@pytest.fixture
def temp_local_connector(tmp_path, monkeypatch):
    # Create a temporary folder and a dummy text file.
    dummy_dir = tmp_path / "data"
    dummy_dir.mkdir()
    file_path = dummy_dir / "test.txt"
    file_path.write_text("This is a test file.")

    # Override LocalConnector in tasks to use our dummy connector.
    monkeypatch.setattr(
        "tasks.LocalConnector", lambda: DummyLocalConnector(str(dummy_dir))
    )
    return dummy_dir


def test_process_workflow_local(temp_local_connector):
    results = process_workflow("local", "local")
    # Verify that the summarization was applied.
    assert len(results) == 1
    result = results[0]
    assert result["summary"] == "dummy summary"
    # Verify that the output file was written.
    output_file = os.path.join(str(temp_local_connector), "summary_test.txt")
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        content = f.read()
    assert content == "dummy summary"
