"use client";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Skull, Zap, Shield, FileCode, Terminal, 
  Activity, Download 
} from "lucide-react";

// --- API CONFIGURATION ---
const API_URL = "http://127.0.0.1:8000";

export default function LazarusDashboard() {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState("IDLE"); // IDLE, SCANNING, READY, RESURRECTING, COMPLETE
  const [report, setReport] = useState<any>(null);
  const [results, setResults] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);
  
  // Auto-scroll log window
  const logEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const addLog = (msg: string) => setLogs((prev) => [...prev, `> ${msg}`]);

  const scanRepo = async () => {
    if (!url) return;
    setStatus("SCANNING");
    setLogs(["> INITIALIZING LAZARUS PROTOCOL...", "> CONNECTING TO TARGET..."]);
    
    try {
      const res = await axios.post(`${API_URL}/scan`, { url });
      setReport(res.data);
      addLog(`> TARGET ACQUIRED: ${res.data.project_name}`);
      addLog(`> DECAY LEVEL: ${100 - res.data.resurrection_score}%`);
      setStatus("READY");
    } catch (err) {
      addLog(`> ERROR: CONNECTION REFUSED`);
      setStatus("IDLE");
    }
  };

  const resurrectRepo = async () => {
    setStatus("RESURRECTING");
    addLog("> INJECTING ADRENALINE (Dependencies)...");
    addLog("> CAUTERIZING WOUNDS (Security)...");
    addLog("> MUTATING DNA (Code Refactoring)...");
    
    try {
      const res = await axios.post(`${API_URL}/resurrect`, {
        local_path: report.local_path,
        details: report.dependency_health.details
      });
      
      setResults(res.data.results);
      addLog("> PROCESS COMPLETE.");
      setStatus("COMPLETE");
    } catch (err) {
      addLog("> RESURRECTION FAILED.");
      setStatus("READY");
    }
  };

  const downloadZip = async () => {
    try {
      const res = await axios.get(`${API_URL}/download/${report.project_name}?local_path=${report.local_path}`);
      window.open(`file://${res.data.download_url}`, '_blank'); 
      alert(`Saved to: ${res.data.download_url}`);
    } catch (e) {
      alert("Export failed");
    }
  };

  return (
    <main className="min-h-screen bg-black text-green-500 font-mono p-8 selection:bg-green-900 selection:text-white overflow-hidden relative">
      {/* BACKGROUND */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-green-900/10 via-black to-black pointer-events-none" />
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-green-600 to-transparent opacity-50" />

      <div className="max-w-6xl mx-auto relative z-10">
        
        {/* HEADER */}
        <header className="flex items-center justify-between mb-16 border-b border-green-900/50 pb-6">
          <div className="flex items-center gap-4">
            <motion.div 
              animate={{ rotate: status === "RESURRECTING" ? 360 : 0 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <Skull size={48} className="text-purple-500" />
            </motion.div>
            <div>
              <h1 className="text-4xl font-bold tracking-tighter text-white">LAZARUS <span className="text-purple-500">AI</span></h1>
              <p className="text-xs text-green-700 tracking-[0.5em]">RESURRECTION ENGINE v1.0</p>
            </div>
          </div>
          <div className="flex gap-4 text-xs opacity-50">
            <div className="flex items-center gap-2"><div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" /> SYSTEM ONLINE</div>
          </div>
        </header>

        {/* INPUT SECTION */}
        <AnimatePresence mode="wait">
          {status === "IDLE" && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
              className="max-w-2xl mx-auto mt-20"
            >
              <div className="relative flex bg-black rounded-lg border border-green-900 shadow-[0_0_30px_rgba(0,255,0,0.1)]">
                <input 
                  type="text" 
                  placeholder="ENTER GITHUB REPOSITORY URL..." 
                  className="w-full bg-transparent p-4 outline-none text-white placeholder-green-900"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                />
                <button 
                  onClick={scanRepo}
                  className="px-8 bg-green-900/20 hover:bg-green-500 hover:text-black transition-colors font-bold border-l border-green-900"
                >
                  SCAN
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* DASHBOARD */}
        {(status !== "IDLE") && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* LEFT PANEL */}
            <motion.div initial={{ x: -50, opacity: 0 }} animate={{ x: 0, opacity: 1 }} className="space-y-6">
              <div className="p-6 border border-green-900/50 bg-green-950/5 rounded-lg">
                <h3 className="text-xs text-green-700 mb-2">TARGET SUBJECT</h3>
                <div className="text-2xl text-white truncate">{report?.project_name || "LOADING..."}</div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border border-green-900/50 bg-green-950/5 rounded-lg">
                  <h3 className="text-xs text-green-700 mb-1">DECAY LEVEL</h3>
                  <div className="text-3xl font-bold text-red-500">
                    {report ? 100 - report.resurrection_score : 0}%
                  </div>
                </div>
                <div className="p-4 border border-green-900/50 bg-green-950/5 rounded-lg">
                  <h3 className="text-xs text-green-700 mb-1">DEPENDENCIES</h3>
                  <div className="text-3xl font-bold text-white">
                    {report?.dependency_health.total || 0}
                  </div>
                </div>
              </div>

              {status === "READY" && (
                 <button 
                  onClick={resurrectRepo}
                  className="w-full py-4 bg-purple-900/20 border border-purple-500 text-purple-400 hover:bg-purple-500 hover:text-white transition-all rounded text-xl font-bold tracking-widest animate-pulse"
                >
                  ⚡ INITIATE RITUAL
                </button>
              )}

              {status === "RESURRECTING" && (
                <div className="w-full bg-green-900/20 border border-green-900 p-4 rounded text-center">
                  <div className="text-green-500 animate-pulse mb-2">RESURRECTING...</div>
                  <progress className="w-full h-2 bg-black [&::-webkit-progress-bar]:bg-black [&::-webkit-progress-value]:bg-green-500" max="100"></progress>
                </div>
              )}

              {status === "COMPLETE" && (
                 <button 
                  onClick={downloadZip}
                  className="w-full py-4 bg-green-900/20 border border-green-500 text-green-400 hover:bg-green-500 hover:text-black transition-all rounded text-xl font-bold tracking-widest"
                >
                  <Download className="inline mr-2" /> EXHUME CORPSE
                </button>
              )}
            </motion.div>

            {/* RIGHT PANEL (LOGS) */}
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="lg:col-span-2">
              <div className="h-[400px] border border-green-900/50 bg-black rounded-lg p-6 overflow-y-auto font-mono text-sm relative">
                <div className="absolute top-2 right-4 text-xs text-green-800 flex items-center gap-2">
                  <Terminal size={12} /> TERMINAL OUTPUT
                </div>
                {logs.map((log, i) => (
                  <div key={i} className="mb-2 text-green-400">
                    <span className="opacity-50 mr-2">[{new Date().toLocaleTimeString()}]</span>
                    {log}
                  </div>
                ))}
                <div ref={logEndRef} />
              </div>

              {/* RESULTS GRID */}
              {status === "COMPLETE" && results && (
                <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="grid grid-cols-3 gap-4 mt-6">
                  <div className="p-4 border border-green-500/30 bg-green-900/10 rounded text-center">
                    <Zap className="mx-auto mb-2 text-green-500" />
                    <div className="text-2xl font-bold text-white">{results.dependencies.success.length}</div>
                    <div className="text-xs text-green-500">UPDATES FORCED</div>
                  </div>
                  <div className="p-4 border border-purple-500/30 bg-purple-900/10 rounded text-center">
                    <Shield className="mx-auto mb-2 text-purple-500" />
                    <div className="text-2xl font-bold text-white">{results.security.fixed}</div>
                    <div className="text-xs text-purple-500">VULNERABILITIES PATCHED</div>
                  </div>
                  <div className="p-4 border border-blue-500/30 bg-blue-900/10 rounded text-center">
                    <FileCode className="mx-auto mb-2 text-blue-500" />
                    <div className="text-2xl font-bold text-white">{results.modernization.files_changed}</div>
                    <div className="text-xs text-blue-500">FILES MODERNIZED</div>
                  </div>
                </motion.div>
              )}
            </motion.div>

          </div>
        )}
      </div>
    </main>
  );
}