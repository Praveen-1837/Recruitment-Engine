"use client";

import React from "react";
import { CandidateMatch } from "@/lib/types";
import SkillBadge from "./SkillBadge";
import { User, FileText, ChevronRight, Award, Clock } from "lucide-react";

interface CandidateCardProps {
  candidate: CandidateMatch;
  isSelected: boolean;
  onToggleSelect: () => void;
  onOpenDetail: () => void;
}

export default function CandidateCard({
  candidate,
  isSelected,
  onToggleSelect,
  onOpenDetail,
}: CandidateCardProps) {
  const score = Math.round(candidate.match_score);

  // Score color classes
  let scoreColor = "text-[#00B359]";
  let progressBg = "bg-[#00B359]";
  let borderHighlight = "hover:border-emerald-300";

  if (score < 70) {
    scoreColor = "text-[#D94A45]";
    progressBg = "bg-[#D94A45]";
    borderHighlight = "hover:border-rose-300";
  } else if (score < 90) {
    scoreColor = "text-[#FFB900]";
    progressBg = "bg-[#FFB900]";
    borderHighlight = "hover:border-amber-300";
  }

  // Derive human-readable name from filename if possible
  const displayName = candidate.filename
    .replace(/\.[^/.]+$/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (l) => l.toUpperCase());

  return (
    <div
      className={`bg-white rounded-xl border transition-all duration-200 shadow-sm hover:shadow-md p-5 ${
        isSelected ? "border-[#0066CC] ring-2 ring-[#0066CC]/20" : "border-gray-200 " + borderHighlight
      }`}
    >
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        {/* Left: Checkbox + Avatar + Name + Filename */}
        <div className="flex items-start space-x-3.5">
          <input
            type="checkbox"
            checked={isSelected}
            onChange={onToggleSelect}
            className="mt-1.5 h-4 w-4 rounded border-gray-300 text-[#0066CC] focus:ring-[#0066CC] cursor-pointer"
            title="Select for comparison"
          />

          <div className="w-11 h-11 rounded-full bg-blue-50 border border-blue-200 flex items-center justify-center text-[#0066CC] flex-shrink-0">
            <User className="w-5 h-5" />
          </div>

          <div>
            <div className="flex items-center space-x-2">
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-gray-100 text-gray-800">
                #{candidate.rank}
              </span>
              <h3 className="font-semibold text-gray-900 text-base leading-tight">
                {displayName}
              </h3>
            </div>
            <div className="flex items-center space-x-2 mt-1 text-xs text-gray-500">
              <FileText className="w-3.5 h-3.5" />
              <span>{candidate.filename}</span>
              {candidate.experience_years !== undefined && candidate.experience_years > 0 && (
                <>
                  <span>•</span>
                  <span className="flex items-center">
                    <Clock className="w-3.5 h-3.5 mr-1 text-gray-400" />
                    {candidate.experience_years} years exp
                  </span>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Right: Score Progress Bar */}
        <div className="flex items-center space-x-4 lg:w-72">
          <div className="flex-1">
            <div className="flex justify-between items-center mb-1">
              <span className="text-xs font-medium text-gray-500">Match Score</span>
              <span className={`text-base font-bold ${scoreColor}`}>{score}%</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
              <div
                className={`h-2.5 rounded-full transition-all duration-500 ${progressBg}`}
                style={{ width: `${Math.min(100, Math.max(5, score))}%` }}
              />
            </div>
          </div>

          <button
            onClick={onOpenDetail}
            className="inline-flex items-center px-3 py-1.5 text-xs font-semibold text-[#0066CC] hover:bg-blue-50 border border-blue-200 rounded-lg transition-colors whitespace-nowrap"
          >
            Details
            <ChevronRight className="w-3.5 h-3.5 ml-1" />
          </button>
        </div>
      </div>

      {/* Assessment snippet */}
      {candidate.assessment && (
        <div className="mt-3.5 p-2.5 bg-gray-50 rounded-lg border border-gray-100 text-xs text-gray-600 italic">
          "{candidate.assessment}"
        </div>
      )}

      {/* Skills breakdown */}
      <div className="mt-4 pt-3.5 border-t border-gray-100 space-y-2">
        {candidate.matched_skills && candidate.matched_skills.length > 0 && (
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-xs font-semibold text-gray-500 mr-1 min-w-[75px]">
              Matched ({candidate.matched_skills.length}):
            </span>
            {candidate.matched_skills.map((s, i) => (
              <SkillBadge key={i} skill={s} type="matched" size="sm" />
            ))}
          </div>
        )}

        {candidate.missing_skills && candidate.missing_skills.length > 0 && (
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-xs font-semibold text-gray-500 mr-1 min-w-[75px]">
              Missing ({candidate.missing_skills.length}):
            </span>
            {candidate.missing_skills.map((s, i) => (
              <SkillBadge key={i} skill={s} type="missing" size="sm" />
            ))}
          </div>
        )}

        {candidate.extra_skills && candidate.extra_skills.length > 0 && (
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-xs font-semibold text-gray-500 mr-1 min-w-[75px]">
              Bonus ({candidate.extra_skills.length}):
            </span>
            {candidate.extra_skills.slice(0, 5).map((s, i) => (
              <SkillBadge key={i} skill={s} type="extra" size="sm" />
            ))}
            {candidate.extra_skills.length > 5 && (
              <span className="text-xs text-gray-400 self-center">
                +{candidate.extra_skills.length - 5} more
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
