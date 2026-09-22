"use client";

import React, { useEffect, useState } from "react";
import { CheckCircle2, Loader2, Sparkles, BrainCircuit } from "lucide-react";

interface ProgressBarProps {
  currentStep: number; // 1: Text extraction, 2: Claude AI extraction, 3: Matching & Ranking
  candidateCount?: number;
}

export default function ProgressBar({ currentStep, candidateCount = 5 }: ProgressBarProps) {
  const steps = [
    { id: 1, label: "Extracting Text", desc: "Parsing PDF, DOCX, and TXT resumes" },
    { id: 2, label: "AI Skill Extraction", desc: "Claude AI identifying tech & soft competencies" },
    { id: 3, label: "Matching & Ranking", desc: "Evaluating requirement overlap and ranking fit" },
  ];

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm max-w-xl mx-auto text-center">
      <div className="w-14 h-14 bg-blue-50 text-[#0066CC] rounded-2xl flex items-center justify-center mx-auto mb-4 border border-blue-100">
        <BrainCircuit className="w-7 h-7 animate-pulse" />
      </div>

      <h3 className="text-xl font-bold text-gray-900 mb-1">Analyzing Candidates</h3>
      <p className="text-sm text-gray-500 mb-6">
        Processing {candidateCount} resumes against job criteria...
      </p>

      {/* Steps List */}
      <div className="space-y-4 text-left mb-6">
        {steps.map((step) => {
          const isDone = currentStep > step.id;
          const isCurrent = currentStep === step.id;

          return (
            <div
              key={step.id}
              className={`p-3.5 rounded-xl border flex items-center justify-between transition-all ${
                isDone
                  ? "bg-emerald-50/60 border-emerald-200 text-emerald-900"
                  : isCurrent
                  ? "bg-blue-50/60 border-[#0066CC]/30 text-gray-900 ring-1 ring-[#0066CC]/20"
                  : "bg-gray-50 border-gray-100 text-gray-400"
              }`}
            >
              <div className="flex items-center space-x-3">
                {isDone ? (
                  <CheckCircle2 className="w-5 h-5 text-[#00B359]" />
                ) : isCurrent ? (
                  <Loader2 className="w-5 h-5 text-[#0066CC] animate-spin" />
                ) : (
                  <div className="w-5 h-5 rounded-full border border-gray-300 flex items-center justify-center text-xs font-semibold text-gray-400">
                    {step.id}
                  </div>
                )}
                <div>
                  <span className="font-semibold text-sm block leading-tight">
                    {step.label}
                  </span>
                  <span className="text-xs opacity-75">{step.desc}</span>
                </div>
              </div>

              <span className="text-xs font-bold">
                {isDone ? "100%" : isCurrent ? "Processing..." : "Pending"}
              </span>
            </div>
          );
        })}
      </div>

      <p className="text-xs text-gray-400">
        AI semantic extraction in progress with Claude Opus 4.1
      </p>
    </div>
  );
}
