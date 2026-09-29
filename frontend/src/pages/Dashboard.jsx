import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import api from '../api/axios';

const PROGRAM_ELECTIVES = {
  "General Science":     ["Biology", "Chemistry", "Physics", "Elective Math"],
  "General Arts":        ["Literature", "Geography", "Government", "History", "Economics", "French", "Christian Religious Studies", "Islamic Religious Studies"],
  "Business":            ["Business Management", "Financial Accounting", "Costing", "Economics"],
  "Home Economics":      ["Food and Nutrition", "Clothing and Textiles", "Management in Living", "General Knowledge in Art"],
  "Visual Arts":         ["Graphic Design", "Picture Making", "Sculpture", "Ceramics", "Leatherwork", "Textiles", "Jewellery"],
  "Agricultural Science":["Animal Husbandry", "Crop Husbandry and Horticulture", "Agricultural Economics", "Farm Management"],
};

const PROGRAM_INTERESTS = {
  "General Science": [
    "Engineering & Technology", "Healthcare & Medicine","Data Science & Analytics","Research & Science",
    "Environmental Studies", "Mathematics & Computing", "Education",
    "Finance & Economics", "Management", "Real Estate & Construction"
  ],
  "General Arts": [
    "Law & Legal Studies", "Education & Teaching", "Politics & Governance",
    "Communication & Media", "Social Sciences", "History & Culture",
    "Development Studies", "Finance & Economics", "Management", "Real Estate"
  ],
  "Business": [
    "Accounting & Finance", "Banking & Investment", "Entrepreneurship",
    "Marketing & Management", "Real Estate", "Economics",
    "Law & Legal Studies", "Education", "Communication & Media"
  ],
  "Home Economics": [
    "Healthcare & Public Health", "Education & Teaching", "Nutrition & Dietetics",
    "Social Sciences", "Management", "Entrepreneurship",
    "Communication & Media", "Development Studies"
  ],
  "Visual Arts": [
    "Communication & Media", "Education & Teaching", "Design & Creative Arts",
    "Entrepreneurship", "Development Studies", "Social Sciences",
    "History & Culture", "Management"
  ],
  "Agricultural Science": [
    "Research & Science", "Education & Teaching", "Environmental Studies",
    "Development Studies", "Management", "Finance & Economics",
    "Healthcare & Public Health", "Real Estate & Construction"
  ],
};

const GRADES = ["A1","A2","B2","B3","C4","C5","C6","D7","E8","F9"];

export default function Dashboard() {
  const navigate = useNavigate();
  const location = useLocation();

  const [form, setForm] = useState(
    location.state?.previousForm || {
      shs_program: '',
      elective_1: '', elective_1_grade: '',
      elective_2: '', elective_2_grade: '',
      elective_3: '', elective_3_grade: '',
      interest: '',
      core_math_grade: '', english_grade: '',
      science_grade: '', social_grade: ''
    }
  );

  const [errors, setErrors]   = useState({});
  const [loading, setLoading] = useState(false);

  const handle = e => {
    const { name, value } = e.target;
    setForm(prev => {
      const updated = { ...prev, [name]: value };
      if (name === 'shs_program') {
        updated.elective_1 = ''; updated.elective_1_grade = '';
        updated.elective_2 = ''; updated.elective_2_grade = '';
        updated.elective_3 = ''; updated.elective_3_grade = '';
        updated.interest   = '';
      }
      return updated;
    });
    setErrors(prev => ({ ...prev, [name]: '' }));
  };

  const validate = () => {
    const e = {};
    if (!form.shs_program)      e.shs_program      = 'Please select your SHS programme';
    if (!form.interest)         e.interest         = 'Please select your career interest';
    if (!form.elective_1)       e.elective_1       = 'Please select Elective 1';
    if (!form.elective_1_grade) e.elective_1_grade = 'Please select grade for Elective 1';
    if (!form.elective_2)       e.elective_2       = 'Please select Elective 2';
    if (!form.elective_2_grade) e.elective_2_grade = 'Please select grade for Elective 2';
    if (!form.elective_3)       e.elective_3       = 'Please select Elective 3';
    if (!form.elective_3_grade) e.elective_3_grade = 'Please select grade for Elective 3';
    if (!form.core_math_grade)  e.core_math_grade  = 'Required';
    if (!form.english_grade)    e.english_grade    = 'Required';
    if (!form.science_grade)    e.science_grade    = 'Required';
    if (!form.social_grade)     e.social_grade     = 'Required';

    const chosen = [form.elective_1, form.elective_2, form.elective_3].filter(Boolean);
    if (new Set(chosen).size !== chosen.length) {
      e.elective_2 = 'You cannot choose the same elective twice';
      e.elective_3 = 'You cannot choose the same elective twice';
    }
    return e;
  };

  const submit = async () => {
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }
    setLoading(true);
    try {
      const { data: result } = await api.post('/students/results', form);
      const { data: rec }    = await api.post(`/recommend/${result.result_id}`);
      navigate('/results', { state: { rec, previousForm: form } });
    } catch (err) {
      setErrors({ general: err.response?.data?.detail || 'Submission failed. Try again.' });
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const availableElectives = PROGRAM_ELECTIVES[form.shs_program] || [];
  const availableInterests = PROGRAM_INTERESTS[form.shs_program] || [];

  const getElectiveOptions = (currentField) => {
    const selected = ['elective_1','elective_2','elective_3']
      .filter(f => f !== currentField)
      .map(f => form[f]);
    return availableElectives.filter(e => !selected.includes(e));
  };

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
        <button onClick={logout}
          className="text-sm bg-white text-green-800 px-4 py-1.5 rounded-full font-semibold hover:bg-green-100 transition">
          Logout
        </button>
      </nav>

      <div className="max-w-2xl mx-auto p-8 space-y-6">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Enter your SHS results</h2>
          <p className="text-sm text-gray-500 mt-1">Fill in all fields to get your university programme recommendation</p>
        </div>

        {errors.general && (
          <p className="text-red-500 text-sm bg-red-50 border border-red-200 p-3 rounded-lg">{errors.general}</p>
        )}

        {/* SHS Programme & Interest */}
        <div className="bg-white border rounded-xl p-5 space-y-4 shadow-sm">
          <h3 className="text-sm font-semibold text-green-800 uppercase tracking-wide">Programme & Interest</h3>

          <div>
            <label className="text-sm font-medium text-gray-700 mb-1 block">
              SHS Programme <span className="text-red-500">*</span>
            </label>
            <select name="shs_program" value={form.shs_program} onChange={handle}
              className={`w-full border rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-green-500 ${errors.shs_program ? 'border-red-400' : 'border-gray-300'}`}>
              <option value="">Select your SHS programme</option>
              {Object.keys(PROGRAM_ELECTIVES).map(p => <option key={p}>{p}</option>)}
            </select>
            {errors.shs_program && <p className="text-red-500 text-xs mt-1">{errors.shs_program}</p>}
          </div>

          {form.shs_program && (
            <div>
              <label className="text-sm font-medium text-gray-700 mb-1 block">
                Career Interest <span className="text-red-500">*</span>
              </label>
              <select name="interest" value={form.interest} onChange={handle}
                className={`w-full border rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-green-500 ${errors.interest ? 'border-red-400' : 'border-gray-300'}`}>
                <option value="">Select your career interest</option>
                {availableInterests.map(i => <option key={i}>{i}</option>)}
              </select>
              {errors.interest && <p className="text-red-500 text-xs mt-1">{errors.interest}</p>}
            </div>
          )}
        </div>

        {/* Electives */}
        <div className="bg-white border rounded-xl p-5 space-y-4 shadow-sm">
          <h3 className="text-sm font-semibold text-green-800 uppercase tracking-wide">Elective Subjects & Grades</h3>
          {!form.shs_program ? (
            <p className="text-amber-600 text-sm bg-amber-50 border border-amber-200 p-3 rounded-lg">
              Select your SHS programme first to see available electives.
            </p>
          ) : (
            [1, 2, 3].map(num => {
              const sf = `elective_${num}`;
              const gf = `elective_${num}_grade`;
              return (
                <div key={num} className="border rounded-lg p-4 bg-gray-50">
                  <p className="text-sm font-semibold text-gray-700 mb-3">Elective {num}</p>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <select name={sf} value={form[sf]} onChange={handle}
                        className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 ${errors[sf] ? 'border-red-400' : 'border-gray-300'}`}>
                        <option value="">Select subject</option>
                        {getElectiveOptions(sf).map(e => <option key={e}>{e}</option>)}
                      </select>
                      {errors[sf] && <p className="text-red-500 text-xs mt-1">{errors[sf]}</p>}
                    </div>
                    <div>
                      <select name={gf} value={form[gf]} onChange={handle}
                        className={`w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 ${errors[gf] ? 'border-red-400' : 'border-gray-300'}`}>
                        <option value="">Select grade</option>
                        {GRADES.map(g => <option key={g}>{g}</option>)}
                      </select>
                      {errors[gf] && <p className="text-red-500 text-xs mt-1">{errors[gf]}</p>}
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Core Grades */}
        <div className="bg-white border rounded-xl p-5 space-y-3 shadow-sm">
          <h3 className="text-sm font-semibold text-green-800 uppercase tracking-wide">Core Subject Grades</h3>
          {[
            ["core_math_grade", "Core Mathematics"],
            ["english_grade",   "English Language"],
            ["science_grade",   "Integrated Science"],
            ["social_grade",    "Social Studies"],
          ].map(([field, label]) => (
            <div key={field} className="flex items-center justify-between border rounded-lg px-4 py-3 bg-gray-50">
              <span className="text-sm font-medium text-gray-700">
                {label} <span className="text-red-500">*</span>
              </span>
              <div className="text-right">
                <select name={field} value={form[field]} onChange={handle}
                  className={`border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 ${errors[field] ? 'border-red-400' : 'border-gray-300'}`}>
                  <option value="">Grade</option>
                  {GRADES.map(g => <option key={g}>{g}</option>)}
                </select>
                {errors[field] && <p className="text-red-500 text-xs mt-1">{errors[field]}</p>}
              </div>
            </div>
          ))}
        </div>

        <button onClick={submit} disabled={loading}
          className="w-full bg-green-700 text-white py-3 rounded-xl hover:bg-green-800 font-bold text-sm tracking-wide shadow-lg transition-all duration-200 hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed">
          {loading ? 'Analysing your results...' : 'Get University Recommendation →'}
        </button>
      </div>
    </div>
  );
}