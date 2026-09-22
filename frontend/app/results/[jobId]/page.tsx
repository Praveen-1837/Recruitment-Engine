"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { getJobResults, getExportUrl } from "@/lib/api";
import { JobResultsData, CandidateMatch } from "@/lib/types";
import CandidateCard from "@/components/CandidateCard";
import CandidateModal from "@/components/CandidateModal";
import {
  Download,
  UploadCloud,
  Columns,
  Sparkles,
  Trophy,
  Users,
  Briefcase,
  AlertCircle,
  RotateCcw
} from "lucide-react";

export default function ResultsPage() {
  const params = useParams();
  const router = useRouter();
  const jobId = params.jobId as string;

  const [data, setData] = useState<JobResultsData | null>(null);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [activeModalCandidate, setActiveModalCandidate] = useState<CandidateMatch | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (jobId) {
      loadResults();
    }
  }, [jobId]);

  const loadResults = async () => {
    try {
      setLoading(true);
      setError(null);
      const results = await getJobResults(jobId);
      setData(results);
    } catch (err: any) {
      setError(err.message || "Failed to load analysis results.");
    } finally {
      setLoading(false);
    }
  };

  const toggleSelect = (candidateId: string) => {
    setSelectedIds((prev) => {
      if (prev.includes(candidateId)) {
        return prev.filter((id) => id !== candidateId);
      } else {
        if (prev.length >= 5) return prev; // limit to 5
        return [...prev, candidateId];
      }
    });
  };

  const handleCompare = () => {
    if (selectedIds.length < 2) return;
    const query = new URLSearchParams();
    query.set("job_id", jobId);
    query.set("candidates", selectedIds.join(","));
    router.push(`/compare?${query.toString()}`);
  };

  if (loading) {
    return (
      <div className="py-20 text-center">
        <div className="w-12 h-12 border-4 border-[#0066CC] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <h3 className="text-base font-bold text-gray-900">Loading Ranked Results</h3>
        <p className="text-xs text-gray-500 mt-1">Retrieving candidate evaluations and match breakdowns...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto py-12 text-center bg-white rounded-2xl border border-gray-200 p-8">
        <AlertCircle className="w-10 h-10 text-red-500 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-gray-900 mb-1">Results Unavailable</h2>
        <p className="text-xs text-gray-600 mb-6">{error}</p>
        <Link
          href={`/jobs/${jobId}/upload`}
          className="inline-flex items-center px-4 py-2 text-xs font-bold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-lg"
        >
          <UploadCloud className="w-4 h-4 mr-1.5" />
          Go to Upload & Analyze
        </Link>
      </div>
    );
  }

  const candidates = data?.candidates || [];
  const bestMatch = data?.best_match;

  return (
    <div className="space-y-6 pb-20">
      {/* Top Banner & Stats */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 sm:p-8 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 pb-6 border-b border-gray-100">
          <div>
            <div className="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-emerald-50 text-[#00B359] text-xs font-semibold mb-2">
              <Sparkles className="w-3.5 h-3.5" />
              <span>AI Analysis Complete</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-gray-900 tracking-tight">
              {data?.job_title || "Job Candidates"}
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-1">
              Ranked candidates based on technical skill alignment, experience, and role qualifications.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <Link
              href={`/jobs/${jobId}/upload`}
              className="inline-flex items-center px-3.5 py-2 text-xs font-semibold text-gray-700 bg-white hover:bg-gray-50 border border-gray-300 rounded-xl transition-colors shadow-sm"
            >
              <UploadCloud className="w-4 h-4 mr-1.5 text-gray-500" />
              Upload More
            </Link>

            <a
              href={getExportUrl(jobId, "csv")}
              download
              className="inline-flex items-center px-4 py-2 text-xs font-bold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-xl shadow-sm hover:shadow transition-all"
            >
              <Download className="w-4 h-4 mr-1.5" />
              Export CSV
            </a>
          </div>
        </div>

        {/* Highlight Cards */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 bg-gray-50 rounded-xl border border-gray-100 flex items-center space-x-3.5">
            <div className="w-10 h-10 rounded-lg bg-blue-100 text-[#0066CC] flex items-center justify-center font-bold">
              <Users className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs text-gray-500 font-medium block">Total Evaluated</span>
              <span className="text-xl font-bold text-gray-900">{candidates.length} candidates</span>
            </div>
          </div>

          {bestMatch && (
            <div className="p-4 bg-emerald-50/60 rounded-xl border border-emerald-100 flex items-center space-x-3.5 sm:col-span-2">
              <div className="w-10 h-10 rounded-lg bg-[#E8F5E9] text-[#00B359] flex items-center justify-center font-bold">
                <Trophy className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-emerald-800 font-bold uppercase tracking-wider">
                    Top Recommended Candidate
                  </span>
                  <span className="text-sm font-black text-[#00B359]">
                    {Math.round(bestMatch.match_score)}% Match
                  </span>
                </div>
                <p className="text-sm font-bold text-gray-900 truncate mt-0.5">
                  {bestMatch.filename}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Comparison Floating Action Bar */}
      {selectedIds.length > 0 && (
        <div className="sticky top-20 z-30 bg-gray-900 text-white rounded-2xl p-4 shadow-xl flex items-center justify-between animate-in fade-in slide-in-from-top-3">
          <div className="flex items-center space-x-3">
            <Columns className="w-5 h-5 text-blue-400" />
            <span className="text-sm font-semibold">
              {selectedIds.length} candidate{selectedIds.length > 1 ? "s" : ""} selected for comparison
            </span>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setSelectedIds([])}
              className="px-3 py-1 text-xs text-gray-300 hover:text-white transition-colors"
            >
              Clear
            </button>
            <button
              onClick={handleCompare}
              disabled={selectedIds.length < 2}
              className="px-4 py-1.5 text-xs font-bold bg-[#0066CC] hover:bg-[#0052A3] rounded-lg transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Compare Side-by-Side
            </button>
          </div>
        </div>
      )}

      {/* Candidate List */}
      <div className="space-y-4">
        {candidates.map((cand) => (
          <CandidateCard
            key={cand.candidate_id}
            candidate={cand}
            isSelected={selectedIds.includes(cand.candidate_id)}
            onToggleSelect={() => toggleSelect(cand.candidate_id)}
            onOpenDetail={() => setActiveModalCandidate(cand)}
          />
        ))}
      </div>

      {/* Detail Modal */}
      <CandidateModal
        candidate={activeModalCandidate}
        onClose={() => setActiveModalCandidate(null)}
        isSelectedForCompare={
          activeModalCandidate ? selectedIds.includes(activeModalCandidate.candidate_id) : false
        }
        onToggleCompare={() => {
          if (activeModalCandidate) {
            toggleSelect(activeModalCandidate.candidate_id);
          }
        }}
      />
    </div>
  );
}
