"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { getJobs } from "@/lib/api";
import { JobPosting } from "@/lib/types";
import {
  UploadCloud,
  BrainCircuit,
  BarChart3,
  Clock,
  Sparkles,
  ArrowRight,
  PlusCircle,
  FileCheck,
  ChevronRight,
  Briefcase
} from "lucide-react";

export default function HomePage() {
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getJobs()
      .then((data) => setJobs(data || []))
      .catch((err) => console.error("Error loading jobs:", err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-12 pb-12">
      {/* Hero Section */}
      <section className="text-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-blue-50/70 via-white to-transparent rounded-3xl border border-blue-100/60 shadow-sm">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-100/80 text-[#0066CC] text-xs font-semibold mb-6">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Powered by Claude Opus AI Architecture</span>
        </div>

        <h1 className="text-4xl sm:text-5xl font-black text-gray-900 tracking-tight max-w-3xl mx-auto leading-tight">
          AI Recruitment <br className="hidden sm:inline" />
          <span className="text-[#0066CC]">Intelligence Engine</span>
        </h1>

        <p className="mt-4 text-base sm:text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
          Upload resumes. Automatically extract technical and soft competencies.
          Rank candidates by semantic fit in minutes, not hours.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3.5">
          <Link
            href="/jobs/new"
            className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3.5 text-base font-bold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-xl shadow-md hover:shadow-lg transition-all"
          >
            <PlusCircle className="w-5 h-5 mr-2" />
            Start New Job Analysis
          </Link>
        </div>

        {/* Quick Stats */}
        <div className="mt-12 pt-8 border-t border-gray-200/60 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-center">
          <div>
            <div className="text-2xl font-black text-[#0066CC]">85%+</div>
            <div className="text-xs font-medium text-gray-500 mt-0.5">Matching Precision</div>
          </div>
          <div>
            <div className="text-2xl font-black text-gray-900">&lt; 3 mins</div>
            <div className="text-xs font-medium text-gray-500 mt-0.5">20-Resume Batch</div>
          </div>
          <div>
            <div className="text-2xl font-black text-[#00B359]">5-10 hrs</div>
            <div className="text-xs font-medium text-gray-500 mt-0.5">Saved per Hire</div>
          </div>
          <div>
            <div className="text-2xl font-black text-gray-900">PDF, DOCX</div>
            <div className="text-xs font-medium text-gray-500 mt-0.5">Multi-format Parsing</div>
          </div>
        </div>
      </section>

      {/* Feature Cards */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-[#0066CC] flex items-center justify-center mb-4">
            <UploadCloud className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-gray-900 mb-2">1. Batch Upload</h3>
          <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
            Drag and drop up to 50 resumes in PDF, DOCX, or TXT format. Text is cleaned and extracted asynchronously.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
          <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center mb-4">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-gray-900 mb-2">2. AI Skill Extraction</h3>
          <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
            Claude Opus semantically identifies technical frameworks, soft skills, certifications, and years of experience.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
          <div className="w-12 h-12 rounded-xl bg-emerald-50 text-[#00B359] flex items-center justify-center mb-4">
            <BarChart3 className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-gray-900 mb-2">3. Quantitative Ranking</h3>
          <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
            Candidates are scored 0-100% based on exact requirements alignment, experience fit, and missing skill penalties.
          </p>
        </div>
      </section>

      {/* Active Jobs Section */}
      <section className="bg-white rounded-2xl border border-gray-200 p-6 sm:p-8 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Recent Job Analyses</h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Select an existing job role to view ranked results or upload more candidates
            </p>
          </div>
          <Link
            href="/jobs/new"
            className="text-xs sm:text-sm font-semibold text-[#0066CC] hover:text-[#0052A3] flex items-center"
          >
            <span>Create Job</span>
            <ChevronRight className="w-4 h-4 ml-0.5" />
          </Link>
        </div>

        {loading ? (
          <div className="py-12 text-center text-sm text-gray-500">Loading job postings...</div>
        ) : jobs.length === 0 ? (
          <div className="py-12 text-center border-2 border-dashed border-gray-200 rounded-xl">
            <Briefcase className="w-10 h-10 text-gray-300 mx-auto mb-2" />
            <p className="text-sm font-medium text-gray-700">No job postings created yet.</p>
            <p className="text-xs text-gray-400 mt-1 mb-4">
              Get started by creating your first job posting and uploading candidates.
            </p>
            <Link
              href="/jobs/new"
              className="inline-flex items-center px-4 py-2 text-xs font-semibold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-lg"
            >
              <PlusCircle className="w-4 h-4 mr-1.5" />
              Create First Job
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {jobs.map((job) => (
              <div
                key={job.id}
                className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-gray-50/70 px-2 rounded-xl transition-colors"
              >
                <div>
                  <h4 className="font-bold text-base text-gray-900 leading-tight">{job.title}</h4>
                  <div className="flex items-center space-x-3 mt-1 text-xs text-gray-500">
                    <span>{job.candidate_count || 0} candidates uploaded</span>
                    <span>•</span>
                    <span>{job.seniority_level || "mid-level"}</span>
                    <span>•</span>
                    <span>
                      Created {new Date(job.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-2.5">
                  <Link
                    href={`/jobs/${job.id}/upload`}
                    className="px-3 py-1.5 text-xs font-medium text-gray-700 bg-white hover:bg-gray-100 border border-gray-300 rounded-lg transition-colors"
                  >
                    Upload Resumes
                  </Link>

                  <Link
                    href={`/results/${job.id}`}
                    className="px-3.5 py-1.5 text-xs font-semibold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-lg transition-colors flex items-center"
                  >
                    <span>View Results</span>
                    <ArrowRight className="w-3.5 h-3.5 ml-1" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
