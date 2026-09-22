"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Sparkles, Briefcase, PlusCircle, ArrowLeft } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Link href="/" className="flex items-center space-x-2.5">
            <div className="w-10 h-10 rounded-lg bg-[#0066CC] flex items-center justify-center text-white font-bold shadow-sm">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-lg text-gray-900 tracking-tight block">
                Recruitment Intelligence Engine
              </span>
              <span className="text-xs text-gray-500 font-medium -mt-1 block">
                AI-Powered Screening & Ranking
              </span>
            </div>
          </Link>
        </div>

        <nav className="flex items-center space-x-3">
          {pathname !== "/" && (
            <Link
              href="/"
              className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900 px-3 py-1.5 rounded-md hover:bg-gray-100 transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-1.5" />
              All Jobs
            </Link>
          )}

          <Link
            href="/jobs/new"
            className="inline-flex items-center justify-center px-4 py-2 text-sm font-semibold text-white bg-[#0066CC] hover:bg-[#0052A3] rounded-lg shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-[#0066CC] focus:ring-offset-2"
          >
            <PlusCircle className="w-4 h-4 mr-2" />
            New Job Analysis
          </Link>
        </nav>
      </div>
    </header>
  );
}
