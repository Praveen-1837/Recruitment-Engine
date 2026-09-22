"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { compareCandidates, getExportUrl } from "@/lib/api";
import { CompareResponseData } from "@/lib/types";
import ComparisonTable from "@/components/ComparisonTable";
import { ArrowLeft, Download, Printer, AlertCircle, Sparkles } from "lucide-react";

function CompareContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const jobId = searchParams.get("job_id");
  const candidatesParam = searchParams.get("candidates");

  const [data, setData] = useState<CompareResponseData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId || !candidatesParam) {
      setError("Missing job_id or candidates parameter for comparison.");
      setLoading(false);
      return;
    }

    const candidateIds = candidatesParam.split(",").map((s) => s.trim()).filter(Boolean);
    if (candidateIds.length === 0) {
      setError("No candidates specified.");
      setLoading(false);
      return;
    }

    setLoading(true);
    compareCandidates(jobId, candidateIds)
      .then((res) => setData(res))
      .catch((err) => setError(err.message || "Failed to compare candidates."))
      .finally(() => setLoading(false));
  }, [jobId, candidatesParam]);

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="py-20 text-center">
        <div className="w-12 h-12 border-4 border-[#0066CC] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <h3 className="text-base font-bold text-gray-900">Comparing Candidates</h3>
        <p className="text-xs text-gray-500 mt-1">
          Evaluating side-by-side skill matrix and strengths...
        </p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="max-w-xl mx-auto py-12 text-center bg-white rounded-2xl border border-gray-200 p-8">
        <AlertCircle className="w-10 h-10 text-red-500 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-gray-900 mb-1">Comparison Unavailable</h2>
        <p className="text-xs text-gray-600 mb-6">{error || "Unable to load comparison data."}</p>
        <button
          onClick={() => router.back()}
          className="inline-flex items-center px-4 py-2 text-xs font-bold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-lg"
        >
          <ArrowLeft className="w-4 h-4 mr-1.5" />
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-16">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <Link
            href={`/results/${jobId}`}
            className="p-2 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 text-gray-600 transition-colors"
            title="Back to ranked results"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <div className="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 text-[#0066CC] text-xs font-semibold mb-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Side-by-Side Comparison</span>
            </div>
            <h1 className="text-2xl font-black text-gray-900 leading-tight">
              {data.job_title}
            </h1>
          </div>
        </div>

        <div className="flex items-center space-x-2.5 print:hidden">
          <button
            onClick={handlePrint}
            className="inline-flex items-center px-3.5 py-2 text-xs font-semibold text-gray-700 bg-white hover:bg-gray-50 border border-gray-300 rounded-xl transition-colors shadow-sm"
          >
            <Printer className="w-4 h-4 mr-1.5 text-gray-500" />
            Print / Save PDF
          </button>

          {jobId && (
            <a
              href={getExportUrl(jobId, "csv")}
              download
              className="inline-flex items-center px-4 py-2 text-xs font-bold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-xl shadow-sm hover:shadow transition-all"
            >
              <Download className="w-4 h-4 mr-1.5" />
              Export Full CSV
            </a>
          )}
        </div>
      </div>

      {/* Comparison Table Component */}
      <ComparisonTable
        jobTitle={data.job_title}
        candidates={data.candidates}
        requiredSkills={data.required_skills}
        recommendation={data.recommendation}
      />
    </div>
  );
}

export default function ComparePage() {
  return (
    <Suspense
      fallback={
        <div className="py-20 text-center text-xs text-gray-500">
          Loading comparison view...
        </div>
      }
    >
      <CompareContent />
    </Suspense>
  );
}
