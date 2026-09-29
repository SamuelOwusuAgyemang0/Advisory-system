import { useLocation, useNavigate } from 'react-router-dom';

export default function Results() {
  const { state } = useLocation();
  const navigate  = useNavigate();
  const rec          = state?.rec;
  const previousForm = state?.previousForm;

  if (!rec) return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center space-y-4">
        <p className="text-gray-600">No results found.</p>
        <button onClick={() => navigate('/dashboard')}
          className="bg-green-700 text-white px-6 py-2 rounded-lg hover:bg-green-800 font-semibold">
          Go back
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Sticky Navbar */}
      <nav className="bg-green-800 px-6 py-4 flex justify-between items-center shadow sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <img src="/ubids-logo.jpeg" alt="UBIDS"
            className="w-10 h-10 rounded-full object-cover border-2 border-white" />
          <div>
            <h1 className="text-white font-bold text-base leading-tight">UBIDS Advisory System</h1>
            <p className="text-green-200 text-xs">University of Business and Integrated Development Studies</p>
          </div>
        </div>
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 bg-white text-green-800 px-5 py-2 rounded-full font-semibold text-sm shadow hover:bg-green-50 hover:shadow-md transition-all duration-200 border border-green-200">
          Submit another result
        </button>
      </nav>

      <div className="max-w-xl mx-auto p-8 space-y-6">
        <h2 className="text-xl font-bold text-gray-800">Your Recommendation</h2>

        {/* Eligibility */}
        <div className={`p-6 rounded-xl border shadow-sm ${rec.eligible
          ? 'bg-green-50 border-green-200'
          : 'bg-red-50 border-red-200'}`}>
          <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Eligibility Status</p>
          <p className={`text-2xl font-bold ${rec.eligible ? 'text-green-700' : 'text-red-700'}`}>
            {rec.eligible ? '✓ Eligible for Degree Programme' : '✗ Not Eligible for Degree — Diploma Recommended'}
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Confidence: <span className="font-semibold">{(rec.confidence * 100).toFixed(1)}%</span>
            &nbsp;|&nbsp; Model: {rec.model_version}
          </p>
        </div>

        {/* Recommended Programme — Degree or Diploma */}
        {rec.recommended_programme && (
          <div className={`p-6 rounded-xl border shadow-sm ${
            rec.programme_type === 'Diploma'
              ? 'bg-amber-50 border-amber-200'
              : 'bg-blue-50 border-blue-200'
          }`}>
            <div className="flex items-center justify-between mb-1">
              <p className="text-xs text-gray-500 uppercase tracking-wide">
                Recommended Programme
              </p>
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                rec.programme_type === 'Diploma'
                  ? 'bg-amber-200 text-amber-800'
                  : 'bg-blue-200 text-blue-800'
              }`}>
                {rec.programme_type || 'Degree'}
              </span>
            </div>
            <p className={`text-xl font-bold mt-1 ${
              rec.programme_type === 'Diploma' ? 'text-amber-800' : 'text-blue-800'
            }`}>
              {rec.recommended_programme}
            </p>
            {rec.programme_type === 'Diploma' && (
              <p className="text-sm text-amber-700 mt-2">
                Based on your results, a diploma programme is recommended.
                You may upgrade to{' '}
                <span className="font-semibold">{rec.degree_equivalent}</span>{' '}
                after successfully completing the diploma.
              </p>
            )}
            {rec.programme_type !== 'Diploma' && (
              <p className="text-sm text-blue-600 mt-1">
                Based on your SHS programme and career interest.
              </p>
            )}
          </div>
        )}

        {/* Career paths */}
        {rec.careers?.length > 0 && (
          <div>
            <h3 className="text-base font-bold text-gray-700 mb-3">Possible Career Paths</h3>
            <div className="space-y-3">
              {rec.careers.map((c, i) => (
                <div key={i}
                  className="p-4 rounded-xl border bg-white shadow-sm flex justify-between items-center hover:shadow-md transition">
                  <div>
                    <p className="font-semibold text-gray-800">{c.title}</p>
                    <p className="text-sm text-gray-500">{c.industry}</p>
                  </div>
                  <span className="text-xs bg-green-100 text-green-800 px-3 py-1 rounded-full font-medium">
                    {c.industry}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Bottom back button */}
        <button
          onClick={() => navigate('/dashboard', { state: { previousForm } })}
          className="w-full flex items-center justify-center gap-2 border-2 border-green-700 text-green-700 py-3 rounded-xl font-bold text-sm hover:bg-green-700 hover:text-white transition-all duration-200 shadow hover:shadow-lg">
          ← Go back and make changes
        </button>
      </div>
    </div>
  );
}