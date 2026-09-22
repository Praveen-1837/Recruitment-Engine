import os
import io
import pytest
from fastapi.testclient import TestClient
from main import app
from models.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_db()

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data

def test_complete_flow_endpoints():
    # 1. Create a Job
    job_payload = {
        "title": "Senior Python Developer",
        "description": "We are seeking a Senior Python Developer with 5+ years of experience in Python, FastAPI, PostgreSQL, and Docker. Experience with AWS is nice to have. Requires strong leadership and teamwork."
    }
    create_job_res = client.post("/api/jobs", json=job_payload)
    assert create_job_res.status_code == 201
    job_data = create_job_res.json()["data"]
    job_id = job_data["id"]
    assert job_data["title"] == "Senior Python Developer"
    assert "Python" in job_data["required_skills"]

    # 2. Upload Resumes
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test_data/resumes"))
    pdf_path = os.path.join(base_dir, "alex_senior_python.pdf")
    txt_path = os.path.join(base_dir, "jordan_junior_python.txt")

    with open(pdf_path, "rb") as f1, open(txt_path, "rb") as f2:
        files = [
            ("files", ("alex_senior_python.pdf", f1, "application/pdf")),
            ("files", ("jordan_junior_python.txt", f2, "text/plain"))
        ]
        upload_res = client.post(
            "/api/upload",
            data={"job_id": job_id},
            files=files
        )
    assert upload_res.status_code == 201
    upload_data = upload_res.json()["data"]
    assert upload_data["total_uploaded"] == 2
    candidate_ids = [c["candidate_id"] for c in upload_data["uploaded_files"]]

    # 3. Analyze Candidates
    analyze_res = client.post(f"/api/analyze/{job_id}")
    assert analyze_res.status_code == 200
    analyze_data = analyze_res.json()["data"]
    assert len(analyze_data["candidates_ranked"]) == 2
    # Alex (Senior) should rank #1 with higher match score
    top = analyze_data["candidates_ranked"][0]
    assert "alex" in top["filename"].lower()
    assert top["rank"] == 1
    assert top["match_score"] > 70

    # 4. Get Results
    results_res = client.get(f"/api/results/{job_id}")
    assert results_res.status_code == 200
    results_data = results_res.json()["data"]
    assert results_data["total_candidates"] == 2

    # 5. Compare Candidates
    compare_res = client.post("/api/compare", json={
        "job_id": job_id,
        "candidate_ids": candidate_ids
    })
    assert compare_res.status_code == 200
    comp_data = compare_res.json()["data"]
    assert len(comp_data["candidates"]) == 2
    assert "recommendation" in comp_data

    # 6. Export Results CSV
    export_res = client.get(f"/api/export/{job_id}?format=csv")
    assert export_res.status_code == 200
    assert "text/csv" in export_res.headers["content-type"]
    assert "alex_senior_python.pdf" in export_res.text
    assert "Rank" in export_res.text
