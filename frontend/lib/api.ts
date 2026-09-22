import axios from "axios";
import {
  JobPosting,
  CandidateUploaded,
  CandidateDetail,
  JobResultsData,
  CompareResponseData
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 2 minutes for large AI analysis
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorData = error.response?.data;
    const message =
      errorData?.message ||
      errorData?.detail?.message ||
      error.message ||
      "An unexpected server error occurred.";
    return Promise.reject(new Error(message));
  }
);

export async function createJob(title: string, description: string): Promise<JobPosting> {
  const res = await client.post("/api/jobs", { title, description });
  return res.data.data;
}

export async function getJobs(): Promise<JobPosting[]> {
  const res = await client.get("/api/jobs");
  return res.data.data;
}

export async function getJob(jobId: string): Promise<JobPosting> {
  const res = await client.get(`/api/jobs/${jobId}`);
  return res.data.data;
}

export async function uploadResumes(jobId: string, files: File[]): Promise<any> {
  const formData = new FormData();
  formData.append("job_id", jobId);
  files.forEach((file) => {
    formData.append("files", file);
  });

  const res = await client.post("/api/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return res.data.data;
}

export async function getJobCandidates(jobId: string): Promise<CandidateUploaded[]> {
  const res = await client.get(`/api/candidates/${jobId}`);
  return res.data.data;
}

export async function getCandidateDetail(candidateId: string): Promise<CandidateDetail> {
  const res = await client.get(`/api/candidates/detail/${candidateId}`);
  return res.data.data;
}

export async function analyzeJob(jobId: string): Promise<any> {
  const res = await client.post(`/api/analyze/${jobId}`);
  return res.data.data;
}

export async function getJobResults(jobId: string): Promise<JobResultsData> {
  const res = await client.get(`/api/results/${jobId}`);
  return res.data.data;
}

export async function compareCandidates(
  jobId: string,
  candidateIds: string[]
): Promise<CompareResponseData> {
  const res = await client.post("/api/compare", {
    job_id: jobId,
    candidate_ids: candidateIds,
  });
  return res.data.data;
}

export function getExportUrl(jobId: string, format: string = "csv"): string {
  return `${API_BASE}/api/export/${jobId}?format=${format}`;
}
