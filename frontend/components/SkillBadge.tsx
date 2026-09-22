"use client";

import React from "react";
import { Check, X, Plus } from "lucide-react";

interface SkillBadgeProps {
  skill: string;
  type: "matched" | "missing" | "extra";
  size?: "sm" | "md";
}

export default function SkillBadge({ skill, type, size = "md" }: SkillBadgeProps) {
  let bgClass = "bg-[#F3F3F3] text-[#666666] border-gray-300";
  let icon = <Plus className="w-3.5 h-3.5 mr-1 text-gray-500" />;

  if (type === "matched") {
    bgClass = "bg-[#E8F5E9] text-[#00B359] border-[#A5D6A7]";
    icon = <Check className="w-3.5 h-3.5 mr-1 text-[#00B359] stroke-[2.5]" />;
  } else if (type === "missing") {
    bgClass = "bg-[#FFEBEE] text-[#D94A45] border-[#EF9A9A]";
    icon = <X className="w-3.5 h-3.5 mr-1 text-[#D94A45] stroke-[2.5]" />;
  }

  const paddingClass = size === "sm" ? "px-2 py-0.5 text-xs" : "px-2.5 py-1 text-xs font-medium";

  return (
    <span
      className={`inline-flex items-center rounded-full border ${bgClass} ${paddingClass} tracking-wide transition-colors`}
    >
      {icon}
      <span>{skill}</span>
    </span>
  );
}
