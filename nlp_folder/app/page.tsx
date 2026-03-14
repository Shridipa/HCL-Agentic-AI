'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      router.push('/dashboard');
    }
  }, [router]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Clear previous errors
    setError('');
    
    // Validate both fields
    if (!username.trim()) {
      setError('Username is required');
      return;
    }
    
    if (!email.trim()) {
      setError('Email is required');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      setError('Please enter a valid email address');
      return;
    }
    
    if (!password.trim()) {
      setError('Password is required');
      return;
    }
    
    // Both fields filled - store and redirect
    localStorage.setItem('user', JSON.stringify({ 
      username: username.trim(),
      email: email.trim()
    }));
    router.push('/dashboard');
  };

  return (
    <div className="min-h-screen bg-[#090a1a] flex items-center justify-center p-8 relative overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/20 blur-[120px] rounded-full"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/20 blur-[120px] rounded-full"></div>
      
      <Card className="w-[440px] max-w-full glass-card border-white/10 shadow-2xl relative z-10 animate-slide-up">
        <CardHeader className="space-y-4 pb-8">
          <div className="flex justify-center mb-2">
            <div className="w-16 h-16 bg-gradient-to-tr from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-500/20">
              <span className="font-bold text-2xl text-white">H</span>
            </div>
          </div>
          <div className="text-center space-y-2">
            <CardTitle className="text-3xl font-bold tracking-tight text-white flex items-center justify-center gap-2">
              HCL<span className="text-blue-500">.</span>Tech
            </CardTitle>
            <CardDescription className="text-slate-400 font-medium">
              Intelligent Assistant Protocol v2.0
            </CardDescription>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="username" className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Identity</Label>
              <Input
                id="username"
                type="text"
                placeholder="Operational Alias"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="h-12 bg-white/5 border-white/10 focus:border-blue-500/50 focus:ring-0 text-white placeholder:text-slate-600 rounded-xl transition-all"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email" className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Secure Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@hcltech.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-12 bg-white/5 border-white/10 focus:border-blue-500/50 focus:ring-0 text-white placeholder:text-slate-600 rounded-xl transition-all"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Access Key</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="h-12 bg-white/5 border-white/10 focus:border-blue-500/50 focus:ring-0 text-white placeholder:text-slate-600 rounded-xl transition-all"
              />
            </div>

            {error && (
              <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-medium text-center animate-pulse">
                {error}
              </div>
            )}

            <Button type="submit" className="w-full h-14 btn-premium rounded-xl font-bold text-sm tracking-widest shadow-lg shadow-blue-600/20 group">
              INITIALIZE SESSION
              <span className="ml-2 transition-transform group-hover:translate-x-1">→</span>
            </Button>
            
            <p className="text-center text-[10px] text-slate-500 font-medium tracking-wide">
              AUTHENTICATED ACCESS ONLY • ENCRYPTED VIA HCL-SHIELD
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
