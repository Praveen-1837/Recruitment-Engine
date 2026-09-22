"use client";

import React, { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { getJob, uploadResumes, getJobCandidates, analyzeJob } from "@/lib/api";
import { JobPosting, CandidateUploaded } from "@/lib/types";
import ProgressBar from "@/components/ProgressBar";
import {
  UploadCloud,
  FileText,
  Trash2,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Sparkles,
  ArrowRight,
  Briefcase,
  Layers
} from "lucide-react";

export default function UploadPage() {
  const params = useParams();
  const router = useRouter();
  const jobId = params.jobId as string;

  const [job, setJob] = useState<JobPosting | null>(null);
  const [candidates, setCandidates] = useState<CandidateUploaded[]>([]);
  const [stagedFiles, setStagedFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (jobId) {
      loadData();
    }
  }, [jobId]);

  const loadData = async () => {
    try {
      const [jobData, candidateData] = await Promise.all([
        getJob(jobId),
        getJobCandidates(jobId),
      ]);
      setJob(jobData);
      setCandidates(candidateData || []);
    } catch (err: any) {
      setError("Failed to load job data: " + err.message);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      addFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      addFiles(Array.from(e.target.files));
    }
  };

  const addFiles = (newFiles: File[]) => {
    setError(null);
    const valid = newFiles.filter((f) => {
      const ext = f.name.split(".").pop()?.toLowerCase();
      return ext === "pdf" || ext === "docx" || ext === "txt";
    });

    if (valid.length < newFiles.length) {
      setError("Only PDF, DOCX, and TXT files are supported. Some files were skipped.");
    }

    setStagedFiles((prev) => [...prev, ...valid]);
  };

  const removeStagedFile = (idx: number) => {
    setStagedFiles((prev) => prev.filter((_, i) => i !== idx));
  };

  const handleUploadFiles = async () => {
    if (stagedFiles.length === 0) return;
    try {
      setUploading(true);
      setError(null);
      await uploadResumes(jobId, stagedFiles);
      setStagedFiles([]);
      await loadData();
    } catch (err: any) {
      setError(err.message || "Upload failed. Please check files and try again.");
    } finally {
      setUploading(false);
    }
  };

  const handleRunAnalysis = async () => {
    try {
      setAnalyzing(true);
      setError(null);

      // Multi-step progress animation
      setAnalysisStep(1);
      const step1Timer = setTimeout(() => setAnalysisStep(2), 1200);
      const step2Timer = setTimeout(() => setAnalysisStep(3), 2800);

      await analyzeJob(jobId);

      clearTimeout(step1Timer);
      clearTimeout(step2Timer);
      router.push(`/results/${jobId}`);
    } catch (err: any) {
      setAnalyzing(false);
      setError(err.message || "Analysis failed. Please try again.");
    }
  };

  if (analyzing) {
    return (
      <div className="py-12">
        <ProgressBar currentStep={analysisStep} candidateCount={candidates.length + stagedFiles.length} />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Navigation Header */}
      <div className="flex items-center space-x-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
        <span className="text-gray-400">Step 1: Job Created ✓</span>
        <span>•</span>
        <span className="text-[#0066CC]">Step 2: Upload Resumes</span>
        <span>•</span>
        <span>Step 3: AI Ranking</span>
      </div>

      {/* Job Banner */}
      {job && (
        <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm flex items-center justify-between">
          <div className="flex items-center space-x-3.5">
            <div className="w-10 h-10 rounded-xl bg-blue-50 text-[#0066CC] flex items-center justify-center font-bold">
              <Briefcase className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs font-bold text-[#0066CC] uppercase tracking-wider block">
                Target Role
              </span>
              <h2 className="text-lg font-bold text-gray-900 leading-tight">{job.title}</h2>
            </div>
          </div>

          <div className="text-right">
            <span className="text-xs text-gray-500 block">Uploaded Resumes</span>
            <span className="text-lg font-black text-gray-900">{candidates.length}</span>
          </div>
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-xs font-medium text-[#D94A45] flex items-center">
          <AlertCircle className="w-4 h-4 mr-2 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Upload Box */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200 ${
          isDragging
            ? "border-[#0066CC] bg-blue-50/60 scale-[1.005]"
            : "border-gray-300 hover:border-[#0066CC] bg-white hover:bg-gray-50/50 shadow-sm"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.docx,.txt"
          onChange={handleFileSelect}
          className="hidden"
        />

        <div className="w-14 h-14 rounded-2xl bg-blue-50 text-[#0066CC] flex items-center justify-center mx-auto mb-3 shadow-inner">
          <UploadCloud className="w-7 h-7" />
        </div>

        <h3 className="text-base font-bold text-gray-900 mb-1">
          Drag & drop candidate resumes here
        </h3>
        <p className="text-xs text-gray-500 mb-4">
          Supports PDF, DOCX, and TXT files up to 10MB each (up to 50 resumes)
        </p>

        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            fileInputRef.current?.click();
          }}
          className="inline-flex items-center px-4 py-2 text-xs font-bold text-[#0066CC] bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
        >
          Browse Files from Computer
        </button>
      </div>

      {/* Staged Files for Upload */}
      {stagedFiles.length > 0 && (
        <div className="bg-white rounded-2xl border border-blue-200 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-gray-900">
              Ready to Upload ({stagedFiles.length} files)
            </h3>
            <button
              onClick={handleUploadFiles}
              disabled={uploading}
              className="inline-flex items-center px-4 py-2 text-xs font-bold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-lg shadow-sm transition-all disabled:opacity-50"
            >
              {uploading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 mr-1.5 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>Upload Selected Files</>
              )}
            </button>
          </div>

          <div className="divide-y divide-gray-100 max-h-56 overflow-y-auto">
            {stagedFiles.map((file, idx) => (
              <div key={idx} className="py-2.5 flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2.5">
                  <FileText className="w-4 h-4 text-gray-400" />
                  <span className="font-medium text-gray-800">{file.name}</span>
                  <span className="text-gray-400">
                    ({(file.size / 1024).toFixed(1)} KB)
                  </span>
                </div>
                <button
                  onClick={() => removeStagedFile(idx)}
                  className="text-gray-400 hover:text-red-500 transition-colors p-1"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Uploaded Candidates List */}
      {candidates.length > 0 && (
        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-gray-900 flex items-center">
              <CheckCircle2 className="w-4 h-4 mr-2 text-[#00B359]" />
              Uploaded Resumes in Database ({candidates.length})
            </h3>

            <button
              onClick={handleRunAnalysis}
              className="inline-flex items-center px-5 py-2.5 text-xs font-bold text-white bg-[#00B359] hover:bg-emerald-600 rounded-xl shadow-md transition-all"
            >
              <Sparkles className="w-3.5 h-3.5 mr-1.5" />
              Analyze & Rank Candidates
              <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-h-64 overflow-y-auto">
            {candidates.map((c) => (
              <div
                key={c.id}
                className="p-3 bg-gray-50 rounded-xl border border-gray-100 flex items-center space-x-2.5 text-xs text-gray-700"
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-[#00B359] flex-shrink-0" />
                <span className="font-medium truncate">{c.filename}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
