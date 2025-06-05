import pytest
import importlib
from unittest.mock import MagicMock, patch


@pytest.fixture(scope="session")
def flask_app():
    import os, sys
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if root not in sys.path:
        sys.path.insert(0, root)
    with patch("sentence_transformers.SentenceTransformer") as MockModel:
        MockModel.return_value = MagicMock()
        module = importlib.import_module("app")
    return module.app

@pytest.fixture
def client(flask_app):
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client
