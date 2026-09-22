import os
import sys

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_verification():
    print("=== 1. Health Check ===")
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("Health response:", res.json())

    print("\n=== 2. Create Job Posting ===")
    job_payload = {
        "title": "Senior Python Backend Engineer",
        "description": (
            "We are seeking a Senior Python Backend Engineer with 5+ years experience. "
            "Required skills: Python, FastAPI, PostgreSQL, Docker, Git. "
            "Soft skills: Leadership, Agile/Scrum. "
            "Nice to have: AWS, Kubernetes, Redis. "
            "Responsibilities: Build scalable backend microservices and maintain data pipelines."
        )
    }
    res = client.post("/api/jobs", json=job_payload)
    assert res.status_code == 201, f"Job creation failed: {res.text}"
    job_data = res.json()["data"]
    job_id = job_data["id"]
    print(f"Created Job: '{job_data['title']}' (ID: {job_id})")
    print(f"Extracted Requirements: {job_data['required_skills']}")

    print("\n=== 3. Upload 5 Sample Resumes ===")
    resumes_dir = "test_data/resumes"
    filenames = [
        ("alex_senior_python.pdf", "application/pdf"),
        ("sarah_mid_python.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("jordan_junior_python.txt", "text/plain"),
        ("emily_frontend_lead.pdf", "application/pdf"),
        ("michael_devops_cloud.txt", "text/plain"),
    ]

    files_to_send = []
    file_handles = []
    for fname, mime in filenames:
        path = os.path.join(resumes_dir, fname)
        f = open(path, "rb")
        file_handles.append(f)
        files_to_send.append(("files", (fname, f, mime)))

    try:
        upload_res = client.post(
            "/api/upload",
            data={"job_id": job_id},
            files=files_to_send
        )
        assert upload_res.status_code == 201, f"Upload failed: {upload_res.text}"
        upload_data = upload_res.json()["data"]
        print(f"Successfully uploaded {upload_data['total_uploaded']} resumes:")
        candidate_ids = [c["candidate_id"] for c in upload_data["uploaded_files"]]
        for c in upload_data["uploaded_files"]:
            print(f"  - {c['filename']} (Candidate ID: {c['candidate_id']})")
    finally:
        for f in file_handles:
            f.close()

    print("\n=== 4. Analyze & Rank Candidates ===")
    analyze_res = client.post(f"/api/analyze/{job_id}")
    assert analyze_res.status_code == 200, f"Analysis failed: {analyze_res.text}"
    analyze_data = analyze_res.json()["data"]
    print(f"Analysis completed at: {analyze_data['analysis_completed_at']}")
    print(f"Top Match: {analyze_data['top_match']}")

    print("\n=== 5. Verify Ranked Results ===")
    results_res = client.get(f"/api/results/{job_id}")
    assert results_res.status_code == 200, f"Get results failed: {results_res.text}"
    results = results_res.json()["data"]["candidates"]
    
    print(f"Total Ranked Candidates: {len(results)}")
    for cand in results:
        print(
            f"Rank #{cand['rank']}: {cand['filename']:<26} | "
            f"Score: {cand['match_score']:>4.1f}% | "
            f"Matched: {len(cand['matched_skills'])} | "
            f"Missing: {len(cand['missing_skills'])} | "
            f"Exp: {cand['experience_years']} yrs"
        )
        print(f"  Matched Skills: {cand['matched_skills']}")
        print(f"  Missing Skills: {cand['missing_skills']}")
        print(f"  Assessment:     {cand['assessment'][:80]}...")
        print()

    # Alex (Senior Python) should be Rank #1
    assert "alex" in results[0]["filename"].lower(), "Alex Chen should be Rank #1"
    assert results[0]["match_score"] >= 80, f"Alex match score should be >= 80%, got {results[0]['match_score']}"

    print("=== 6. Side-by-Side Comparison (Top 2 Candidates) ===")
    comp_res = client.post("/api/compare", json={
        "job_id": job_id,
        "candidate_ids": [results[0]["candidate_id"], results[1]["candidate_id"]]
    })
    assert comp_res.status_code == 200, f"Comparison failed: {comp_res.text}"
    comp_data = comp_res.json()["data"]
    print("Recommendation:", comp_data["recommendation"])

    print("\n=== 7. CSV Export ===")
    export_res = client.get(f"/api/export/{job_id}?format=csv")
    assert export_res.status_code == 200
    assert "text/csv" in export_res.headers["content-type"]
    assert "Rank" in export_res.text
    print("CSV Header & Sample Line:")
    for line in export_res.text.strip().split("\n")[:3]:
        print("  ", line)

    print("\n✅ All End-to-End Recruitment Engine checks PASSED successfully!")

if __name__ == "__main__":
    run_verification()
