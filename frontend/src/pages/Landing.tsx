import { Link } from 'react-router-dom'

function Landing() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Hero Section */}
      <div className="max-w-4xl mx-auto px-4 pt-20 pb-16 text-center">
        <h1 className="text-5xl font-bold text-white mb-6 leading-tight">
          Understand any codebase's <br /> history before you touch it
        </h1>
        <p className="text-gray-400 text-lg mb-10 max-w-2xl mx-auto">
          OnboardGit mines a repository's entire git history to surface what
          matters — risky files, hidden knowledge gaps, and dependencies
          nobody documented. Built for developers joining a new codebase.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/signup"
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-8 py-3 rounded-lg transition-colors"
          >
            Get Started Free
          </Link>
          <Link
            to="/login"
            className="border border-gray-700 hover:border-gray-500 text-gray-300 font-medium px-8 py-3 rounded-lg transition-colors"
          >
            Log In
          </Link>
        </div>
      </div>

      {/* The Problem */}
      <div className="border-t border-gray-800 py-16">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-2xl font-semibold text-white mb-4">The problem</h2>
          <p className="text-gray-400 leading-relaxed">
            Joining a new codebase usually means guessing. Which files are
            fragile? Who actually understands the payment module? Are these
            two unrelated-looking files secretly dependent on each other?
            Normally you find out the hard way — after breaking something.
          </p>
        </div>
      </div>

      {/* Features — one per function */}
      <div className="border-t border-gray-800 py-16">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-2xl font-semibold text-white mb-10 text-center">
            What OnboardGit actually does
          </h2>

          <div className="space-y-10">
            {/* Feature 1 */}
            <div className="flex gap-5">
              <div className="text-3xl">🔥</div>
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  Hotspot Detection
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  Scans the full commit history to find which files change
                  most often. These are usually the files with the most
                  logic, the most bugs, and the highest risk when modified —
                  exactly what a new developer should read first.
                </p>
              </div>
            </div>

            {/* Feature 2 */}
            <div className="flex gap-5">
              <div className="text-3xl">👤</div>
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  File Ownership
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  For every file, OnboardGit identifies who has made the most
                  changes — so instead of guessing who to ask, you know
                  exactly who owns which part of the codebase.
                </p>
              </div>
            </div>

            {/* Feature 3 */}
            <div className="flex gap-5">
              <div className="text-3xl">⚠️</div>
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  Bus Factor Risk
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  Flags files where a single contributor owns 70%+ of all
                  changes. If that person leaves, that knowledge leaves with
                  them — this surfaces that risk before it becomes a
                  problem.
                </p>
              </div>
            </div>

            {/* Feature 4 */}
            <div className="flex gap-5">
              <div className="text-3xl">🔗</div>
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  Temporal Coupling
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  Detects files that consistently change together across
                  commits — even when there's no visible import or reference
                  between them. This reveals hidden dependencies no one
                  documented.
                </p>
              </div>
            </div>

            {/* Feature 5 */}
            <div className="flex gap-5">
              <div className="text-3xl">📋</div>
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  Saved Analysis History
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  Every analysis is saved to your account. Come back anytime
                  and revisit a past report instantly, without re-running
                  the analysis.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* How it works */}
      <div className="border-t border-gray-800 py-16">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-2xl font-semibold text-white mb-8 text-center">
            How it works
          </h2>
          <div className="space-y-4">
            {[
              'Paste any public GitHub repository URL',
              'OnboardGit clones it and reads the full commit history',
              'Hotspots, ownership, risks, and coupling are calculated',
              'Results are saved to your account and shown instantly',
            ].map((step, index) => (
              <div key={index} className="flex items-center gap-4">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-semibold shrink-0">
                  {index + 1}
                </div>
                <p className="text-gray-300">{step}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="border-t border-gray-800 py-16">
        <div className="max-w-2xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-semibold text-white mb-4">
            Stop guessing. Start understanding.
          </h2>
          <Link
            to="/signup"
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-medium px-8 py-3 rounded-lg transition-colors mt-4"
          >
            Create Free Account
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Landing