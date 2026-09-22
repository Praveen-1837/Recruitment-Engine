"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { createJob } from "@/lib/api";
import { Briefcase, FileText, Sparkles, Loader2, ArrowRight } from "lucide-react";

const SAMPLE_JOB_TITLE = "Senior Python Backend Engineer";
const SAMPLE_JOB_DESC = `We are seeking an exceptional Senior Python Backend Engineer to lead development of our distributed cloud microservices.

Key Responsibilities:
- Design, build, and maintain scalable REST APIs and backend services in Python.
- Architect high-performance database models with PostgreSQL and SQLAlchemy.
- Containerize and orchestrate services using Docker and Kubernetes on AWS.
- Collaborate with frontend engineers, product managers, and lead agile sprints.

Required Technical Skills:
- 5+ years of software engineering experience with Python.
- Deep expertise with modern web frameworks such as FastAPI or Django.
- Strong relational database experience with PostgreSQL, indexing, and optimization.
- Hands-on experience with Docker, CI/CD pipelines, and Git.

Required Soft Skills:
- Engineering leadership, clear communication, problem solving, and agile teamwork.

Nice to Have:
- Experience with AWS (EC2, S3, RDS, Lambda).
- Familiarity with Redis, Kafka, and Kubernetes.
`;

export default function CreateJobPage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFillSample = () => {
    setTitle(SAMPLE_JOB_TITLE);
    setDescription(SAMPLE_JOB_DESC);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError("Please provide a job title.");
      return;
    }
    if (description.trim().length < 20) {
      setError("Job description should be at least 20 characters.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const created = await createJob(title.trim(), description.trim());
      router.push(`/jobs/${created.id || created.job_id}/upload`);
    } catch (err: any) {
      setError(err.message || "Failed to create job posting. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      {/* Step Navigation Header */}
      <div className="flex items-center space-x-2 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
        <span className="text-[#0066CC]">Step 1: Create Job</span>
        <span>•</span>
        <span>Step 2: Upload Resumes</span>
        <span>•</span>
        <span>Step 3: AI Ranking</span>
      </div>

      <div className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm">
        <div className="flex items-center justify-between pb-6 border-b border-gray-100">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Define Job Requirements</h1>
            <p className="text-xs text-gray-500 mt-1">
              Enter the job specifications. Our AI will automatically extract required skills and criteria.
            </p>
          </div>
          <button
            type="button"
            onClick={handleFillSample}
            className="inline-flex items-center text-xs font-semibold text-[#0066CC] hover:text-[#0052A3] bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200 transition-colors"
          >
            <Sparkles className="w-3.5 h-3.5 mr-1" />
            Fill Sample Job
          </button>
        </div>

        {error && (
          <div className="mt-6 p-4 rounded-xl bg-red-50 border border-red-200 text-xs font-medium text-[#D94A45]">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-6">
          {/* Job Title */}
          <div>
            <label htmlFor="title" className="block text-xs font-bold text-gray-700 uppercase tracking-wider mb-2">
              Job Title <span className="text-red-500">*</span>
            </label>
            <div className="relative rounded-xl shadow-sm">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <Briefcase className="w-4 h-4" />
              </div>
              <input
                id="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Senior Python Developer"
                required
                className="block w-full pl-10 pr-4 py-2.5 text-sm rounded-xl border border-gray-300 focus:ring-2 focus:ring-[#0066CC] focus:border-[#0066CC] transition-colors"
              />
            </div>
          </div>

          {/* Job Description */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label htmlFor="desc" className="block text-xs font-bold text-gray-700 uppercase tracking-wider">
                Full Job Description <span className="text-red-500">*</span>
              </label>
              <span className="text-xs text-gray-400">
                {description.length.toLocaleString()} characters
              </span>
            </div>
            <textarea
              id="desc"
              rows={12}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Paste the full job description here, including required skills, years of experience, and responsibilities..."
              required
              className="block w-full p-4 text-sm rounded-xl border border-gray-300 focus:ring-2 focus:ring-[#0066CC] focus:border-[#0066CC] font-mono transition-colors"
            />
          </div>

          {/* Actions */}
          <div className="pt-4 flex items-center justify-end space-x-3 border-t border-gray-100">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center px-6 py-3 text-sm font-bold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-xl shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Extracting Requirements with AI...
                </>
              ) : (
                <>
                  Continue to Resume Upload
                  <ArrowRight className="w-4 h-4 ml-2" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
