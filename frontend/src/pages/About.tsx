function About() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 px-4 py-12">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">About OnboardGit</h1>
        <p className="text-gray-400 mb-10">
          Understand any codebase's history before you touch it.
        </p>

        {/* What it does */}
        <div className="mb-10">
          <h2 className="text-xl font-semibold text-white mb-3">What it does</h2>
          <p className="text-gray-400 leading-relaxed">
            OnboardGit analyzes a GitHub repository's commit history to surface
            hotspot files, knowledge ownership, bus factor risks, and hidden
            dependencies between files — helping developers understand a
            codebase before making changes.
          </p>
        </div>

        {/* Tech Stack */}
        <div className="mb-10">
          <h2 className="text-xl font-semibold text-white mb-3">Tech Stack</h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              'FastAPI',
              'PostgreSQL',
              'SQLAlchemy',
              'Alembic',
              'React',
              'TypeScript',
              'Tailwind CSS',
              'JWT Auth',
            ].map((tech) => (
              <div
                key={tech}
                className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 text-gray-300 text-sm text-center"
              >
                {tech}
              </div>
            ))}
          </div>
        </div>

        {/* Roadmap */}
        <div>
          <h2 className="text-xl font-semibold text-white mb-3">What's Next</h2>
          <div className="space-y-2">
            {[
              'GitHub username resolution for commit authors',
              'Suggested reading path based on file dependencies',
              'PDF export for analysis reports',
              'Repository comparison over time',
            ].map((item, index) => (
              <div
                key={index}
                className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-3 text-gray-400 text-sm"
              >
                {item}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default About