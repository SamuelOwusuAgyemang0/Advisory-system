import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [focused, setFocused] = useState(false);
  const navigate = useNavigate();

  const handle = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  };

  const submit = async () => {
    try {
      const { data } = await api.post('/auth/login', form);
      localStorage.setItem('token', data.access_token);
      navigate('/dashboard');
    } catch {
      setError('Invalid email or password. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">

      {/* Full background watermark */}
      <div
        style={{
          position: 'fixed',
          inset: 0,
          zIndex: 0,
          transition: 'filter 0.4s ease, opacity 0.4s ease',
          filter: focused ? 'blur(12px)' : 'blur(2px)',
          opacity: focused ? 0.12 : 0.22,
          backgroundImage: 'url(/ubids-logo.jpeg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          pointerEvents: 'none',
        }}
      />

      {/* Green overlay tint */}
      <div style={{
        position: 'fixed', inset: 0, zIndex: 0,
        background: 'linear-gradient(135deg, rgba(20,83,45,0.55) 0%, rgba(21,128,61,0.35) 100%)',
        pointerEvents: 'none',
      }} />

      {/* Login card */}
      <div
        onClick={() => setFocused(true)}
        onBlur={e => { if (!e.currentTarget.contains(e.relatedTarget)) setFocused(false); }}
        tabIndex={-1}
        style={{ position: 'relative', zIndex: 1, outline: 'none' }}
        className="bg-white bg-opacity-95 p-8 rounded-2xl shadow-2xl border border-green-100 w-96 space-y-4"
      >
        {/* Header */}
        <div className="flex flex-col items-center mb-2 space-y-2">
          <img src="/ubids-logo.jpeg" alt="UBIDS Logo"
            className="w-24 h-24 rounded-full object-cover shadow-lg border-4 border-green-700" />
          <div className="text-center">
            <h1 className="text-lg font-bold text-green-800">UBIDS Advisory System</h1>
            <p className="text-xs text-gray-500">University of Business and Integrated Development Studies</p>
          </div>
        </div>

        <h2 className="text-base font-semibold text-gray-700 text-center border-t pt-4">Student Login</h2>

        {error && (
          <p className="text-red-600 text-sm bg-red-50 border border-red-200 p-3 rounded-lg">{error}</p>
        )}

        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">Email</label>
          <input name="email" type="email" value={form.email} onChange={handle}
            placeholder="Enter your email"
            className={`w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 ${error ? 'border-red-400' : 'border-gray-300'}`} />
        </div>

        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">Password</label>
          <input name="password" type="password" value={form.password} onChange={handle}
            placeholder="Enter your password"
            className={`w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 ${error ? 'border-red-400' : 'border-gray-300'}`} />
        </div>

        <button onClick={submit}
          className="w-full bg-green-700 text-white py-2.5 rounded-lg hover:bg-green-800 font-semibold text-sm tracking-wide shadow transition-all duration-200 hover:shadow-lg">
          Login
        </button>

        <p className="text-sm text-center text-gray-600">
          No account?{' '}
          <Link to="/register" className="text-green-700 hover:underline font-semibold">Register here</Link>
        </p>
      </div>
    </div>
  );
}