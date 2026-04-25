'use client';

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

interface Transaction {
  id: string;
  type: string;
  amount: number;
  date: string;
  status: string;
  description: string;
}

interface Ticket {
  id: string;
  title: string;
  status: 'open' | 'in-progress' | 'closed';
  priority: 'low' | 'medium' | 'high';
  createdAt: string;
  description: string;
}

interface Meeting {
  id: string;
  title: string;
  date: string;
  time: string;
  participants: string[];
  status: 'scheduled' | 'completed' | 'cancelled';
}

export default function Dashboard() {
  const router = useRouter();
  const [userName, setUserName] = useState('User');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Dialog states
  const [financeDialog, setFinanceDialog] = useState(false);
  const [ticketsDialog, setTicketsDialog] = useState(false);
  const [meetsDialog, setMeetsDialog] = useState(false);
  const [accessDialog, setAccessDialog] = useState(false);

  // Data states
  const [transactions, setTransactions] = useState<Transaction[]>([
    { id: '1', type: 'expense', amount: 1500, date: '2026-02-10', status: 'completed', description: 'Office Supplies' },
    { id: '2', type: 'income', amount: 5000, date: '2026-02-09', status: 'completed', description: 'Client Payment' }
  ]);

  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [tickets, setTickets] = useState<Ticket[]>([]);

  useEffect(() => {
    const savedMeetings = localStorage.getItem('hcl_meetings');
    if (savedMeetings) setMeetings(JSON.parse(savedMeetings));
    else {
      setMeetings([{ id: '1', title: 'Project Review', date: '2026-02-14', time: '10:00 AM', participants: ['Alex Chen', 'John Doe'], status: 'scheduled' }]);
    }
    const savedTickets = localStorage.getItem('hcl_tickets');
    if (savedTickets) setTickets(JSON.parse(savedTickets));
    else {
      setTickets([{ id: '1', title: 'System Login Issue', status: 'in-progress', priority: 'high', createdAt: '2026-02-12', description: 'Users unable to login to the system' }]);
    }
  }, []);

  useEffect(() => {
    if (meetings.length > 0) localStorage.setItem('hcl_meetings', JSON.stringify(meetings));
  }, [meetings]);

  useEffect(() => {
    if (tickets.length > 0) localStorage.setItem('hcl_tickets', JSON.stringify(tickets));
  }, [tickets]);

  const [newTransaction, setNewTransaction] = useState({ type: 'expense', amount: '', description: '' });

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const parsed = JSON.parse(storedUser);
        const name = parsed.username || parsed.name || 'User';
        setUserName(name);
        setMessages([{ id: 'welcome', text: `Hello ${name}, I am your HCL Intelligent Assistant. How can I facilitate your operations today?`, isUser: false, timestamp: new Date() }]);
      } catch (error) { console.error('Error parsing user data:', error); }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('user');
    router.push('/');
  };



  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    const userMsg: Message = { id: `user-${Date.now()}`, text: input, isUser: true, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: currentInput, user: userName, conversationHistory: messages.map(m => ({ role: m.isUser ? 'user' : 'assistant', content: m.text })) })
      });
      const data = await response.json();
      const replyText = data.reply || data.message || "I'm here to help!";
      try {
        const parsed = JSON.parse(replyText);
        if (parsed.action_data && parsed.action_data.action === 'schedule_meeting') {
          const action = parsed.action_data;
          const newMeeting: Meeting = { id: `meet-${Date.now()}`, title: action.topic || 'New Meeting', date: action.date || 'TBD', time: action.time || 'TBD', participants: Array.isArray(action.participants) ? action.participants : [action.participants], status: 'scheduled' };
          setMeetings(prev => [newMeeting, ...prev]);
        }
      } catch { }
      setMessages(prev => [...prev, { id: `bot-${Date.now()}`, text: replyText, isUser: false, timestamp: new Date(), metadata: data.metadata }]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { id: `error-${Date.now()}`, text: "I encountered a communication error. Please try again.", isUser: false, timestamp: new Date() }]);
    } finally { setIsLoading(false); }
  };

  const newChat = () => {
    setMessages([{ id: 'welcome', text: `Hello ${userName}, how can I help you today?`, isUser: false, timestamp: new Date() }]);
    setInput('');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'border-yellow-500/30 text-yellow-500';
      case 'in-progress': return 'border-blue-500/30 text-blue-400';
      case 'completed': return 'border-green-500/30 text-green-400';
      case 'scheduled': return 'border-purple-500/30 text-purple-400';
      default: return 'border-white/10 text-slate-400';
    }
  };

  const NavItem = ({ icon, label, onClick, active = false }: { icon: string; label: string; onClick: () => void; active?: boolean }) => (
    <button onClick={onClick} className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group ${active ? 'bg-white/10 text-white' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`}>
      <span className="text-xl group-hover:scale-110 transition-transform">{icon}</span>
      <span className="text-sm font-medium">{label}</span>
    </button>
  );

  const renderMessageContent = (msg: Message) => {
    try {
      if (msg.text.trim().startsWith('{') && msg.text.trim().endsWith('}')) {
        const data = JSON.parse(msg.text);
        if (data.title && data.direct_answer) {
          return (
            <div className="space-y-4">
              <div className="flex items-center gap-2 border-b border-white/10 pb-2">
                <span className="text-xl">📊</span>
                <h3 className="text-white font-bold tracking-tight">{data.title.replace('Answer: ', '')}</h3>
                <Badge variant="outline" className="ml-auto border-blue-500/30 text-blue-400 text-[10px]">{data.confidence_score} CONFIDENCE</Badge>
              </div>
              <p className="text-slate-200 text-sm">{data.direct_answer}</p>
              {data.key_insights && (
                <ul className="space-y-2">
                  {data.key_insights.map((insight: string, idx: number) => (
                    <li key={idx} className="flex gap-2 text-slate-300 text-xs bg-white/5 p-2 rounded-lg border border-white/5">
                      <span className="text-blue-400">•</span>
                      <span>{insight}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          );
        }
      }
    } catch { }
    return <div className="prose prose-invert prose-sm max-w-none [&_p]:text-slate-200"><ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown></div>;
  };

  return (
    <div className="flex h-screen bg-[#090a1a] text-white font-sans overflow-hidden">
      <aside className="w-64 border-r border-white/5 flex flex-col bg-black/20 backdrop-blur-3xl">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 bg-gradient-to-tr from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
              <span className="font-bold text-lg">H</span>
            </div>
            <div>
              <h1 className="font-bold text-lg tracking-tight">HCL<span className="text-blue-500">.</span>Tech</h1>
              <p className="text-[10px] text-slate-500 font-medium tracking-[0.2em] uppercase">Intelligence</p>
            </div>
          </div>
          <nav className="space-y-2">
            <NavItem icon="🏠" label="Dashboard" onClick={() => {}} active />
            <NavItem icon="💼" label="Finance" onClick={() => setFinanceDialog(true)} />
            <NavItem icon="🎫" label="Support" onClick={() => setTicketsDialog(true)} />
            <NavItem icon="📅" label="Calendar" onClick={() => setMeetsDialog(true)} />
            <NavItem icon="🔓" label="Access" onClick={() => setAccessDialog(true)} />
            <NavItem icon="📚" label="Knowledge" onClick={() => window.open('/docs.html', '_blank')} />
          </nav>
        </div>
        <div className="flex-1 px-6 py-4 overflow-auto">
          <h3 className="text-[10px] font-bold text-slate-500 tracking-widest uppercase mb-4">Timeline</h3>
          <div className="space-y-6 relative before:absolute before:left-[7px] before:top-2 before:bottom-2 before:w-[1px] before:bg-white/10">
            <div className="relative pl-6">
              <div className="absolute left-0 top-1 w-3.5 h-3.5 rounded-full bg-blue-500/20 border-2 border-blue-500 glow-blue"></div>
              <p className="text-[10px] text-slate-400">10:45 AM Sync</p>
            </div>
          </div>
        </div>
        <div className="p-6 border-t border-white/5 bg-white/[0.02]">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-[10px] font-bold">{userName.substring(0, 2).toUpperCase()}</div>
            <div className="overflow-hidden">
              <p className="text-xs font-bold truncate">{userName}</p>
            </div>
          </div>
          <Button variant="ghost" onClick={handleLogout} className="w-full justify-start text-xs text-red-400 hover:text-red-300 hover:bg-red-500/10 h-8 rounded-lg">退出 Logout</Button>
        </div>
      </aside>

      <main className="flex-1 flex flex-col relative bg-gradient-premium">
        <header className="h-20 border-b border-white/5 flex items-center justify-between px-8 bg-black/10 backdrop-blur-md z-10">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-blue-500/30 p-0.5 glow-blue bg-slate-900">
                <Image src="/avatar.png" alt="AI" width={48} height={48} className="object-cover" />
              </div>
              <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-background"></div>
            </div>
            <div>
              <h2 className="text-sm font-bold flex items-center gap-2">HCL Assistant <Badge className="bg-blue-500/10 text-blue-400 border-0 h-4 px-1.5 text-[8px]">PRO</Badge></h2>
              <p className="text-[10px] text-slate-400">Secure Session Active</p>
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-auto p-8 space-y-6 scroll-smooth">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'} animate-slide-up`}>
              <div className={`p-4 rounded-3xl max-w-[80%] lg:max-w-2xl ${msg.isUser ? 'bg-blue-600 shadow-lg shadow-blue-500/20' : 'glass-card glow-purple'}`}>
                {renderMessageContent(msg)}
                <p className="text-[9px] mt-2 opacity-40 font-medium">{msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
              </div>
            </div>
          ))}
          {isLoading && <div className="flex justify-start animate-pulse"><div className="glass-card p-4 rounded-3xl flex gap-1.5"><div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce"></div><div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce delay-150"></div></div></div>}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-8 pt-0">
          <div className="max-w-4xl mx-auto relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl blur opacity-20 group-focus-within:opacity-40 transition duration-500"></div>
            <div className="relative flex items-center bg-[#1a1b2e]/80 backdrop-blur-xl border border-white/10 rounded-2xl p-2 focus-within:border-blue-500/50">
              <Button variant="ghost" size="icon" className="text-slate-400 shrink-0 ml-2"><span>📎</span></Button>
              <Input value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} placeholder="Ask me anything..." className="flex-1 bg-transparent border-0 focus-visible:ring-0 text-white py-6 px-4" />
              <Button onClick={sendMessage} disabled={!input.trim() || isLoading} className="btn-premium h-11 px-6 rounded-xl font-bold ml-2">SEND</Button>
            </div>
          </div>
        </div>
        <button onClick={newChat} className="absolute bottom-32 right-8 w-14 h-14 bg-gradient-to-r from-cyan-400 to-blue-600 rounded-2xl shadow-2xl flex items-center justify-center hover:scale-110 active:scale-95 transition-all glow-blue group z-20"><span className="text-2xl transition-transform group-hover:rotate-90">➕</span></button>
      </main>

      <Dialog open={financeDialog} onOpenChange={setFinanceDialog}>
        <DialogContent className="max-w-4xl max-h-[85vh] overflow-hidden bg-[#090a1a] border-white/10 p-0 rounded-3xl">
          <div className="h-full flex flex-col">
            <div className="p-8 border-b border-white/5 bg-white/[0.02]">
              <DialogHeader><DialogTitle className="text-2xl font-bold">💼 Finance Center</DialogTitle></DialogHeader>
            </div>
            <div className="flex-1 overflow-auto p-8">
              <Tabs defaultValue="transactions">
                <TabsList className="bg-white/5 border border-white/10 p-1 rounded-xl mb-6">
                  <TabsTrigger value="transactions">Ledger</TabsTrigger>
                  <TabsTrigger value="add">New Entry</TabsTrigger>
                </TabsList>
                <TabsContent value="transactions" className="space-y-3">
                  {transactions.map(txn => (
                    <div key={txn.id} className="glass-card rounded-2xl p-4 flex justify-between items-center">
                      <div className="flex items-center gap-4">
                        <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${txn.type === 'income' ? 'text-green-400' : 'text-red-400'}`}>{txn.type === 'income' ? '↓' : '↑'}</div>
                        <div><p className="font-bold text-sm">{txn.description}</p><p className="text-[10px] text-slate-500">{txn.date}</p></div>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold">${txn.amount.toLocaleString()}</p>
                        <Badge variant="outline" className={getStatusColor(txn.status)}>{txn.status}</Badge>
                      </div>
                    </div>
                  ))}
                </TabsContent>
                <TabsContent value="add" className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2"><Label>Type</Label><Select value={newTransaction.type} onValueChange={v => setNewTransaction({...newTransaction, type: v})}><SelectTrigger className="bg-white/5 border-white/10"><SelectValue /></SelectTrigger><SelectContent className="bg-[#090a1a] border-white/10"><SelectItem value="expense">Expense</SelectItem><SelectItem value="income">Income</SelectItem></SelectContent></Select></div>
                    <div className="space-y-2"><Label>Amount</Label><Input type="number" value={newTransaction.amount} onChange={e => setNewTransaction({...newTransaction, amount: e.target.value})} className="bg-white/5 border-white/10" placeholder="0.00" /></div>
                  </div>
                  <Input value={newTransaction.description} onChange={e => setNewTransaction({...newTransaction, description: e.target.value})} className="bg-white/5 border-white/10" placeholder="Description..." />
                  <Button onClick={() => { if (!newTransaction.amount || !newTransaction.description) return; setTransactions([{ id: Date.now().toString(), type: newTransaction.type, amount: parseFloat(newTransaction.amount), description: newTransaction.description, date: new Date().toISOString().split('T')[0], status: 'completed' }, ...transactions]); setNewTransaction({type:'expense', amount:'', description:''}); }} className="w-full btn-premium py-6 rounded-xl font-bold">Add</Button>
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={ticketsDialog} onOpenChange={setTicketsDialog}>
        <DialogContent className="max-w-4xl max-h-[85vh] overflow-hidden bg-[#090a1a] border-white/10 p-0 rounded-3xl">
          <div className="p-8 border-b border-white/5 bg-white/[0.02]">
            <DialogHeader><DialogTitle className="text-2xl font-bold">🎫 Support</DialogTitle></DialogHeader>
          </div>
          <div className="p-8 overflow-auto space-y-4">
            {tickets.map(ticket => (
              <div key={ticket.id} className="glass-card rounded-2xl p-5 border-l-4 border-l-blue-500 transition-all hover:translate-x-1">
                <div className="flex justify-between items-start mb-2"><h4 className="font-bold text-white">{ticket.title}</h4><Badge variant="outline" className={getStatusColor(ticket.status)}>{ticket.status}</Badge></div>
                <p className="text-xs text-slate-400 mb-4">{ticket.description}</p>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Priority: <span className={ticket.priority === 'high' ? 'text-red-400' : 'text-blue-400'}>{ticket.priority}</span></div>
              </div>
            ))}
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={meetsDialog} onOpenChange={setMeetsDialog}>
        <DialogContent className="max-w-4xl max-h-[85vh] overflow-hidden bg-[#090a1a] border-white/10 p-0 rounded-3xl">
          <div className="p-8 border-b border-white/5 bg-white/[0.02]">
            <DialogHeader><DialogTitle className="text-2xl font-bold">📅 Meetings</DialogTitle></DialogHeader>
          </div>
          <div className="p-8 overflow-auto space-y-4">
            {meetings.map(meeting => (
              <div key={meeting.id} className="glass-card rounded-2xl p-5 flex justify-between items-center">
                <div><h4 className="font-bold text-white mb-1">{meeting.title}</h4><p className="text-[10px] text-slate-400">{meeting.date} • {meeting.time}</p></div>
                <Badge variant="outline" className={getStatusColor(meeting.status)}>{meeting.status}</Badge>
              </div>
            ))}
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={accessDialog} onOpenChange={setAccessDialog}>
        <DialogContent className="max-w-md bg-[#090a1a] border-white/10 rounded-3xl p-8">
          <DialogHeader className="mb-6"><DialogTitle className="text-2xl font-bold">🔓 Access</DialogTitle></DialogHeader>
          <div className="space-y-4">
            {['Cloud Storage', 'Financial Ledger'].map((label, i) => (
              <div key={i} className="flex justify-between items-center p-4 glass-card rounded-2xl"><span className="text-sm font-medium">{label}</span><span className="text-[10px] font-bold uppercase text-green-400">Granted</span></div>
            ))}
            <Button className="w-full btn-premium py-6 rounded-xl font-bold">Request More</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
