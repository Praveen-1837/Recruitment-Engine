"use client";

import React from "react";
import { CompareCandidateData } from "@/lib/types";
import { Check, X, Sparkles, Award, User, Clock } from "lucide-react";

interface ComparisonTableProps {
  jobTitle: string;
  candidates: CompareCandidateData[];
  requiredSkills: string[];
  recommendation: string;
}

export default function ComparisonTable({
  jobTitle,
  candidates,
  requiredSkills,
  recommendation,
}: ComparisonTableProps) {
  if (!candidates || candidates.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500 bg-white rounded-xl border border-gray-200">
        No candidates selected for comparison.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Executive Recommendation */}
      <div className="bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 rounded-2xl border border-blue-100 p-6 shadow-sm">
        <div className="flex items-start space-x-3">
          <div className="w-9 h-9 rounded-xl bg-[#0066CC] text-white flex items-center justify-center flex-shrink-0 mt-0.5 shadow-sm">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-1">
              AI Comparative Recommendation
            </h3>
            <p className="text-gray-800 text-sm leading-relaxed font-medium">
              {recommendation}
            </p>
          </div>
        </div>
      </div>

      {/* Criteria Comparison Table */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
          <h3 className="text-base font-bold text-gray-900">Key Criteria Breakdown</h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50/80">
                <th className="py-3.5 px-5 text-xs font-semibold text-gray-500 uppercase tracking-wider w-1/4">
                  Evaluation Criteria
                </th>
                {candidates.map((c) => (
                  <th
                    key={c.candidate_id}
                    className="py-3.5 px-5 text-sm font-bold text-gray-900"
                  >
                    <div className="flex items-center space-x-2">
                      <div className="w-6 h-6 rounded-full bg-blue-100 text-[#0066CC] flex items-center justify-center text-xs">
                        <User className="w-3.5 h-3.5" />
                      </div>
                      <span className="truncate">{c.filename}</span>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 text-sm">
              {/* Match Score */}
              <tr className="hover:bg-gray-50/50">
                <td className="py-3.5 px-5 font-semibold text-gray-700">Match Score</td>
                {candidates.map((c) => {
                  const score = Math.round(c.match_score);
                  return (
                    <td key={c.candidate_id} className="py-3.5 px-5">
                      <div className="flex items-center space-x-2">
                        <span
                          className={`text-lg font-black ${
                            score >= 90
                              ? "text-[#00B359]"
                              : score >= 70
                              ? "text-[#FFB900]"
                              : "text-[#D94A45]"
                          }`}
                        >
                          {score}%
                        </span>
                        {c.rank && (
                          <span className="text-xs px-2 py-0.5 rounded font-bold bg-gray-100 text-gray-700">
                            Rank #{c.rank}
                          </span>
                        )}
                      </div>
                    </td>
                  );
                })}
              </tr>

              {/* Experience */}
              <tr className="hover:bg-gray-50/50">
                <td className="py-3.5 px-5 font-semibold text-gray-700">Years Experience</td>
                {candidates.map((c) => (
                  <td key={c.candidate_id} className="py-3.5 px-5 font-medium text-gray-800">
                    {c.years_experience} years
                  </td>
                ))}
              </tr>

              {/* Matched Count */}
              <tr className="hover:bg-gray-50/50">
                <td className="py-3.5 px-5 font-semibold text-gray-700">Matched Skills</td>
                {candidates.map((c) => (
                  <td key={c.candidate_id} className="py-3.5 px-5 font-medium text-[#00B359]">
                    {c.matched_skills.length} skills
                  </td>
                ))}
              </tr>

              {/* Missing Count */}
              <tr className="hover:bg-gray-50/50">
                <td className="py-3.5 px-5 font-semibold text-gray-700">Missing Skills</td>
                {candidates.map((c) => (
                  <td key={c.candidate_id} className="py-3.5 px-5 font-medium text-[#D94A45]">
                    {c.missing_skills.length} skills
                  </td>
                ))}
              </tr>

              {/* Extra Count */}
              <tr className="hover:bg-gray-50/50">
                <td className="py-3.5 px-5 font-semibold text-gray-700">Bonus Skills</td>
                {candidates.map((c) => (
                  <td key={c.candidate_id} className="py-3.5 px-5 font-medium text-gray-600">
                    {c.extra_skills.length} skills
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Detailed Skill Matrix */}
      {requiredSkills && requiredSkills.length > 0 && (
        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
            <h3 className="text-base font-bold text-gray-900">Detailed Skill Matrix</h3>
            <p className="text-xs text-gray-500 mt-0.5">
              Comparison across required competencies for {jobTitle}
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50/80">
                  <th className="py-3 px-5 text-xs font-semibold text-gray-500 uppercase tracking-wider w-1/4">
                    Required Skill
                  </th>
                  {candidates.map((c) => (
                    <th
                      key={c.candidate_id}
                      className="py-3 px-5 text-xs font-bold text-gray-700"
                    >
                      {c.filename}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 text-sm">
                {requiredSkills.map((skill, idx) => (
                  <tr key={idx} className="hover:bg-gray-50/50">
                    <td className="py-3 px-5 font-medium text-gray-800">{skill}</td>
                    {candidates.map((c) => {
                      const hasSkill = c.matched_skills.some(
                        (s) => s.toLowerCase() === skill.toLowerCase()
                      );
                      return (
                        <td key={c.candidate_id} className="py-3 px-5">
                          {hasSkill ? (
                            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-[#E8F5E9] text-[#00B359]">
                              <Check className="w-3.5 h-3.5 mr-1 stroke-[2.5]" />
                              Has Skill
                            </span>
                          ) : (
                            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-[#FFEBEE] text-[#D94A45]">
                              <X className="w-3.5 h-3.5 mr-1 stroke-[2.5]" />
                              Missing
                            </span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
