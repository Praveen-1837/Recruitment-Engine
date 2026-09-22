"use client";

import React, { useEffect, useState } from "react";
import { CandidateMatch, CandidateDetail } from "@/lib/types";
import { getCandidateDetail } from "@/lib/api";
import SkillBadge from "./SkillBadge";
import { X, User, FileText, CheckCircle2, AlertTriangle, Briefcase, Award, Globe, Wrench } from "lucide-react";

interface CandidateModalProps {
  candidate: CandidateMatch | null;
  onClose: () => void;
  onToggleCompare?: () => void;
  isSelectedForCompare?: boolean;
}

export default function CandidateModal({
  candidate,
  onClose,
  onToggleCompare,
  isSelectedForCompare = false,
}: CandidateModalProps) {
  const [detail, setDetail] = useState<CandidateDetail | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (candidate) {
      setLoading(true);
      getCandidateDetail(candidate.candidate_id)
        .then((data) => setDetail(data))
        .catch((err) => console.error("Failed to load candidate details", err))
        .finally(() => setLoading(false));
    } else {
      setDetail(null);
    }
  }, [candidate]);

  if (!candidate) return null;

  const score = Math.round(candidate.match_score);
  const displayName = candidate.filename
    .replace(/\.[^/.]+$/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (l) => l.toUpperCase());

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-900/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div
        className="bg-white rounded-2xl shadow-xl border border-gray-200 w-full max-w-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/70">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-blue-100 text-[#0066CC] flex items-center justify-center font-bold">
              <User className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="px-2 py-0.5 rounded text-xs font-bold bg-gray-200 text-gray-800">
                  Rank #{candidate.rank}
                </span>
                <h3 className="text-lg font-bold text-gray-900 leading-tight">
                  {displayName}
                </h3>
              </div>
              <p className="text-xs text-gray-500 flex items-center mt-0.5">
                <FileText className="w-3.5 h-3.5 mr-1" />
                {candidate.filename}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="p-6 max-h-[75vh] overflow-y-auto space-y-5">
          {/* Match Score Bar */}
          <div className="p-4 bg-blue-50/50 rounded-xl border border-blue-100 flex items-center justify-between">
            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Overall Match Score
              </span>
              <div className="flex items-baseline space-x-2 mt-0.5">
                <span className="text-2xl font-black text-[#0066CC]">{score}%</span>
                <span className="text-xs font-medium text-gray-600">
                  {score >= 90 ? "Excellent Fit" : score >= 75 ? "Strong Candidate" : "Moderate Alignment"}
                </span>
              </div>
            </div>
            <div className="w-48">
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className={`h-3 rounded-full ${
                    score >= 90 ? "bg-[#00B359]" : score >= 75 ? "bg-[#FFB900]" : "bg-[#D94A45]"
                  }`}
                  style={{ width: `${Math.min(100, Math.max(5, score))}%` }}
                />
              </div>
            </div>
          </div>

          {/* AI Assessment */}
          <div>
            <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5">
              AI Evaluation Assessment
            </h4>
            <p className="text-sm text-gray-700 bg-gray-50 p-3.5 rounded-xl border border-gray-100 leading-relaxed">
              {candidate.assessment}
            </p>
          </div>

          {/* Matched Skills */}
          <div>
            <h4 className="text-xs font-bold text-[#00B359] uppercase tracking-wider mb-2 flex items-center">
              <CheckCircle2 className="w-4 h-4 mr-1.5" />
              Matched Required Skills ({candidate.matched_skills.length})
            </h4>
            <div className="flex flex-wrap gap-1.5">
              {candidate.matched_skills.length > 0 ? (
                candidate.matched_skills.map((s, i) => (
                  <SkillBadge key={i} skill={s} type="matched" />
                ))
              ) : (
                <span className="text-xs text-gray-400 italic">No matching skills identified</span>
              )}
            </div>
          </div>

          {/* Missing Skills */}
          {candidate.missing_skills.length > 0 && (
            <div>
              <h4 className="text-xs font-bold text-[#D94A45] uppercase tracking-wider mb-2 flex items-center">
                <AlertTriangle className="w-4 h-4 mr-1.5" />
                Missing Critical Requirements ({candidate.missing_skills.length})
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {candidate.missing_skills.map((s, i) => (
                  <SkillBadge key={i} skill={s} type="missing" />
                ))}
              </div>
            </div>
          )}

          {/* Extra / Bonus Skills */}
          {candidate.extra_skills.length > 0 && (
            <div>
              <h4 className="text-xs font-bold text-gray-600 uppercase tracking-wider mb-2">
                Additional Bonus Skills ({candidate.extra_skills.length})
              </h4>
              <div className="flex flex-wrap gap-1.5">
                {candidate.extra_skills.map((s, i) => (
                  <SkillBadge key={i} skill={s} type="extra" />
                ))}
              </div>
            </div>
          )}

          {/* Extracted Details Breakdown */}
          {detail && detail.extracted_skills && (
            <div className="pt-4 border-t border-gray-100 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              {detail.extracted_skills.certifications && detail.extracted_skills.certifications.length > 0 && (
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="font-bold text-gray-700 flex items-center mb-1">
                    <Award className="w-3.5 h-3.5 mr-1 text-amber-500" />
                    Certifications
                  </span>
                  <ul className="list-disc list-inside text-gray-600 space-y-0.5">
                    {detail.extracted_skills.certifications.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                </div>
              )}

              {detail.extracted_skills.languages && detail.extracted_skills.languages.length > 0 && (
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="font-bold text-gray-700 flex items-center mb-1">
                    <Globe className="w-3.5 h-3.5 mr-1 text-blue-500" />
                    Languages
                  </span>
                  <p className="text-gray-600">{detail.extracted_skills.languages.join(", ")}</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-100 flex items-center justify-between">
          {onToggleCompare ? (
            <button
              onClick={onToggleCompare}
              className={`px-4 py-2 text-xs font-semibold rounded-lg border transition-colors ${
                isSelectedForCompare
                  ? "bg-red-50 text-red-600 border-red-200 hover:bg-red-100"
                  : "bg-white text-gray-700 border-gray-300 hover:bg-gray-100"
              }`}
            >
              {isSelectedForCompare ? "Remove from Comparison" : "Add to Comparison"}
            </button>
          ) : <div />}

          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
