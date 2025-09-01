import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.routers import editHandler


@pytest.fixture()
def client(monkeypatch):
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    class DummyS3:
        def __init__(self):
            self.objects = []

        def upload_object(self, name: str, content: bytes) -> None:
            self.objects.append((name, content))

    dummy_s3 = DummyS3()
    monkeypatch.setattr(editHandler, "s3", dummy_s3)

    return TestClient(app)


def _image_bytes(color: str = "blue") -> bytes:
    img = Image.new("RGB", (10, 10), color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


def test_add_white_bg(client):
    image_content = _image_bytes()
    response = client.post(
        "/edit/add-white-bg/",
        files={"file": ("test.png", image_content, "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "test.png"
    assert body["url"]


def test_add_frame(client):
    image_content = _image_bytes("red")
    response = client.post(
        "/edit/add-frame/",
        files={"file": ("test.png", image_content, "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "test.png"
    assert body["url"]
