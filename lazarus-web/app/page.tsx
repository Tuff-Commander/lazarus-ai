"use client";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Skull, Zap, Shield, FileCode, Terminal, 
  Activity, Download, ChevronRight, XCircle, CheckCircle, Ghost 
} from "lucide-react";

// --- API CONFIGURATION ---
const API_URL = "https://lazarus-ai.onrender.com"; 

export default function LazarusDashboard() {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState("IDLE");
  const [report, setReport] = useState<any>(null);
  const [results, setResults] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState("MODERNIZATION");
  
  const logEndRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const addLog = (msg: string) => setLogs((prev) => [...prev, `> ${msg}`]);

  const scanRepo = async () => {
    if (!url) return;
    setStatus("SCANNING");
    setLogs(["> SUMMONING DAEMON...", "> LOCATING TARGET..."]);
    try {
      const res = await axios.post(`${API_URL}/scan`, { url });
      setReport(res.data);
      addLog(`> SOUL CAPTURED: ${res.data.project_name}`);
      addLog(`> DECAY LEVEL: ${100 - res.data.resurrection_score}%`);
      setStatus("READY");
    } catch (err) {
      addLog(`> ERROR: THE TARGET IS ELUSIVE.`);
      setStatus("IDLE");
    }
  };

  const resurrectRepo = async () => {
    setStatus("RESURRECTING");
    addLog("> BREAKING ANCIENT SEALS (Lockfiles)...");
    addLog("> INJECTING DARK MATTER (Dependencies)...");
    addLog("> PURGING CURSES (Security)...");
    
    try {
      const res = await axios.post(`${API_URL}/resurrect`, {
        local_path: report.local_path,
        details: report.dependency_health.details
      });
      setResults(res.data.results);
      addLog("> RITUAL COMPLETE.");
      setStatus("COMPLETE");
    } catch (err) {
      addLog("> RITUAL FAILED. THE DEAD REFUSE TO RISE.");
      setStatus("READY");
    }
  };

  const downloadZip = async () => {
    try {
      // Request the file as a 'blob' (binary data)
      const res = await axios.get(
        `${API_URL}/download/${report.project_name}?local_path=${report.local_path}`, 
        { responseType: 'blob' }
      );
      
      // Create a URL for the blob
      const url = window.URL.createObjectURL(new Blob([res.data]));
      
      // Create an invisible link and click it
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `lazarus_${report.project_name}.zip`);
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      link.remove();
      addLog("> CORPSE EXHUMED SUCCESSFULLY.");
    } catch (e) {
      addLog("> EXHUMATION FAILED: NETWORK ERROR");
      alert("EXHUMATION FAILED. Check backend logs.");
    }
  };

  // --- HORROR ANIMATIONS ---
  const flicker = {
    hidden: { opacity: 0.8 },
    visible: { opacity: 1, transition: { duration: 0.1, repeat: Infinity, repeatType: "reverse" as const } }
  };

  return (
    <main className="min-h-screen bg-black text-red-600 font-mono p-4 selection:bg-red-900 selection:text-white overflow-y-auto relative">
      
      {/* --- INJECT HORROR FONTS & STYLES --- */}
      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Creepster&family=Nosifer&family=Share+Tech+Mono&display=swap');
        
        .font-creep { font-family: 'Creepster', cursive; }
        .font-drip { font-family: 'Nosifer', cursive; }
        .font-tech { font-family: 'Share Tech Mono', monospace; }
        
        @keyframes blood-pulse {
          0% { box-shadow: inset 0 0 0 0 rgba(100, 0, 0, 0); }
          50% { box-shadow: inset 0 0 100px 20px rgba(200, 0, 0, 0.2); }
          100% { box-shadow: inset 0 0 0 0 rgba(100, 0, 0, 0); }
        }
        .animate-blood { animation: blood-pulse 3s infinite; }
        
        .crt-line {
          background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
          background-size: 100% 2px, 3px 100%;
          pointer-events: none;
        }
      `}</style>

      {/* ATMOSPHERE OVERLAYS */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_center,_#220000_0%,_#000000_90%)] -z-10" />
      <div className="fixed inset-0 crt-line z-50 pointer-events-none opacity-20" />
      <div className={`fixed inset-0 pointer-events-none transition-opacity duration-1000 ${status === 'COMPLETE' ? 'animate-blood opacity-100' : 'opacity-0'}`} />

      <div className="max-w-6xl mx-auto relative z-10 pb-20">
        
        {/* HEADER */}
        <header className="flex flex-col md:flex-row items-center justify-between mb-12 border-b-2 border-red-900/50 pb-6 pt-8">
          <div className="flex items-center gap-6">
            <motion.div 
              animate={{ scale: [1, 1.1, 1], opacity: [0.8, 1, 0.8] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              <Skull size={64} className="text-red-600 drop-shadow-[0_0_10px_rgba(255,0,0,0.8)]" />
            </motion.div>
            <div>
              <h1 className="text-5xl md:text-6xl font-drip text-red-600 drop-shadow-[0_0_15px_rgba(255,0,0,0.5)]">LAZARUS AI</h1>
              <p className="text-lg text-orange-700 font-creep tracking-widest mt-2">THE RESURRECTION ENGINE</p>
            </div>
          </div>
          <div className="mt-4 md:mt-0 flex gap-4 text-xs font-tech text-red-900/80 uppercase">
            <div className="flex items-center gap-2 border border-red-900/30 px-3 py-1 bg-black"><Activity size={12} className="animate-pulse" /> DEMONIC PRESENCE: DETECTED</div>
          </div>
        </header>

        {/* INPUT SECTION */}
        <AnimatePresence mode="wait">
          {status === "IDLE" && (
            <motion.div 
              initial={{ opacity: 0, y: 50 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.9 }}
              className="max-w-3xl mx-auto mt-20"
            >
              <div className="bg-black/80 border-2 border-red-900/50 p-1 shadow-[0_0_50px_rgba(255,0,0,0.1)]">
                <div className="flex flex-col md:flex-row gap-2">
                  <input 
                    type="text" 
                    placeholder="ENTER DEAD GITHUB URL..." 
                    className="flex-1 bg-black text-red-500 p-6 outline-none font-tech text-xl placeholder-red-900/50"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                  />
                  <button 
                    onClick={scanRepo}
                    className="px-10 py-4 bg-red-950 hover:bg-red-700 text-red-500 hover:text-black font-creep text-2xl transition-all border-l-2 border-red-900"
                  >
                    HUNT
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* DASHBOARD */}
        {(status !== "IDLE") && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
            
            {/* LEFT PANEL: STATUS */}
            <motion.div initial={{ x: -50, opacity: 0 }} animate={{ x: 0, opacity: 1 }} className="space-y-6">
              
              {/* TARGET CARD */}
              <div className="p-6 border-2 border-red-900 bg-black shadow-[0_0_20px_rgba(255,0,0,0.1)]">
                <h3 className="text-sm font-tech text-red-800 mb-2 uppercase tracking-widest">Target Subject</h3>
                <div className="text-2xl font-tech text-white truncate">{report?.project_name || "ACQUIRING..."}</div>
              </div>

              {/* STATS GRID */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border border-red-900/50 bg-red-950/10">
                  <h3 className="text-xs font-tech text-red-700 mb-1">DECAY</h3>
                  <div className="text-4xl font-creep text-red-500 drop-shadow-[0_0_5px_red]">
                    {report ? 100 - report.resurrection_score : 0}%
                  </div>
                </div>
                <div className="p-4 border border-red-900/50 bg-red-950/10">
                  <h3 className="text-xs font-tech text-red-700 mb-1">BROKEN LINKS</h3>
                  <div className="text-4xl font-creep text-orange-600">
                    {report?.dependency_health.total || 0}
                  </div>
                </div>
              </div>

              {/* ACTION: RESURRECT */}
              {status === "READY" && (
                 <button 
                  onClick={resurrectRepo}
                  className="w-full py-6 bg-black border-2 border-red-600 text-red-500 hover:bg-red-600 hover:text-black transition-all text-3xl font-creep tracking-widest animate-pulse shadow-[0_0_30px_rgba(255,0,0,0.2)]"
                >
                  🩸 INITIATE RITUAL
                </button>
              )}

              {/* STATUS BAR */}
              {status === "RESURRECTING" && (
                <div className="w-full bg-red-950/20 border border-red-900 p-4">
                  <div className="text-red-500 font-tech animate-pulse mb-2 text-center">PERFORMING NECROMANCY...</div>
                  <motion.div 
                    className="h-2 bg-red-600 shadow-[0_0_10px_red]"
                    initial={{ width: "0%" }}
                    animate={{ width: "100%" }}
                    transition={{ duration: 10, ease: "linear" }}
                  />
                </div>
              )}

              {/* ACTION: EXHUME */}
              {status === "COMPLETE" && (
                 <button 
                  onClick={downloadZip}
                  className="w-full py-6 bg-green-950/30 border-2 border-green-700 text-green-500 hover:bg-green-700 hover:text-black transition-all text-2xl font-creep tracking-widest shadow-[0_0_30px_rgba(0,255,0,0.2)]"
                >
                  <Ghost className="inline mr-2 mb-1" /> EXHUME BODY
                </button>
              )}
            </motion.div>

            {/* RIGHT PANEL: TERMINAL & REPORT */}
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="lg:col-span-2">
              
              {/* TERMINAL LOGS */}
              <div className="h-[250px] border border-red-900/30 bg-black/90 p-6 overflow-y-auto font-tech text-xs relative mb-6 shadow-inner">
                <div className="absolute top-2 right-4 text-xs text-red-800 flex items-center gap-2 animate-pulse">
                  <Terminal size={12} /> SEANCE LOG
                </div>
                {logs.map((log, i) => (
                  <div key={i} className="mb-1 text-red-400/80 border-l-2 border-red-900/0 hover:border-red-500 pl-2 transition-all">
                    <span className="opacity-30 mr-2">[{new Date().toLocaleTimeString()}]</span>
                    {log}
                  </div>
                ))}
                <div ref={logEndRef} />
              </div>

              {/* THE REPORT CARD */}
              {status === "COMPLETE" && results && (
                <motion.div 
                  initial={{ y: 50, opacity: 0 }} 
                  animate={{ y: 0, opacity: 1 }} 
                  className="border-2 border-green-900 bg-green-950/5 relative overflow-hidden"
                >
                  <div className="absolute top-0 left-0 w-full h-1 bg-green-600 shadow-[0_0_20px_green]" />
                  
                  {/* REPORT TABS */}
                  <div className="flex border-b border-green-900/50">
                    <button onClick={() => setActiveTab("MODERNIZATION")} className={`flex-1 py-4 font-tech font-bold text-sm tracking-wider ${activeTab === "MODERNIZATION" ? "bg-green-900/20 text-green-400" : "text-green-800 hover:text-green-600"}`}>DNA MUTATIONS</button>
                    <button onClick={() => setActiveTab("DEPS")} className={`flex-1 py-4 font-tech font-bold text-sm tracking-wider ${activeTab === "DEPS" ? "bg-green-900/20 text-green-400" : "text-green-800 hover:text-green-600"}`}>DEPENDENCIES</button>
                    <button onClick={() => setActiveTab("SECURITY")} className={`flex-1 py-4 font-tech font-bold text-sm tracking-wider ${activeTab === "SECURITY" ? "bg-green-900/20 text-green-400" : "text-green-800 hover:text-green-600"}`}>SECURITY</button>
                  </div>

                  <div className="p-6 h-[350px] overflow-y-auto scrollbar-thin scrollbar-thumb-green-900 scrollbar-track-black">
                    
                    {/* 1. CODE MODERNIZATION */}
                    {activeTab === "MODERNIZATION" && (
                      <div className="space-y-4">
                        <div className="flex justify-between items-end border-b border-green-900/30 pb-2">
                          <h4 className="text-2xl font-creep text-green-500">FILES MUTATED</h4>
                          <span className="text-4xl font-tech text-white">{results.modernization.files_changed}</span>
                        </div>
                        <div className="grid grid-cols-1 gap-1">
                          {results.modernization.file_names && results.modernization.file_names.length > 0 ? (
                            results.modernization.file_names.map((file: string, i: number) => (
                              <div key={i} className="flex items-center gap-3 text-xs text-green-300/70 p-2 border-b border-green-900/10 hover:bg-green-900/10 transition-colors font-tech">
                                <FileCode size={12} className="text-green-600" />
                                {file}
                              </div>
                            ))
                          ) : (
                            <div className="text-green-900 italic font-tech p-4">NO DNA ALTERATIONS REQUIRED.</div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* 2. DEPENDENCIES */}
                    {activeTab === "DEPS" && (
                      <div className="space-y-6">
                        <div>
                          <h4 className="text-sm font-bold text-green-500 mb-3 flex items-center gap-2 font-tech"><Zap size={14}/> FORCED RESURRECTIONS ({results.dependencies.success.length})</h4>
                          <div className="grid grid-cols-2 gap-2">
                            {results.dependencies.success.map((pkg: string, i: number) => (
                              <div key={i} className="text-xs font-tech bg-green-900/20 text-green-200 p-2 border-l-2 border-green-500">
                                {pkg}
                              </div>
                            ))}
                          </div>
                        </div>
                        {results.dependencies.failed.length > 0 && (
                          <div>
                            <h4 className="text-sm font-bold text-red-500 mb-3 flex items-center gap-2 font-tech mt-6"><XCircle size={14}/> DIED ON TABLE ({results.dependencies.failed.length})</h4>
                            <div className="grid grid-cols-2 gap-2">
                              {results.dependencies.failed.map((pkg: string, i: number) => (
                                <div key={i} className="text-xs font-tech bg-red-900/10 text-red-400 p-2 border-l-2 border-red-500 opacity-70">
                                  {pkg}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* 3. SECURITY */}
                    {activeTab === "SECURITY" && (
                      <div className="flex flex-col items-center justify-center h-full text-center">
                        <div className="relative">
                          <div className="absolute inset-0 bg-green-500 blur-xl opacity-20 animate-pulse" />
                          <Shield size={80} className="relative text-green-500 mb-4" />
                        </div>
                        <h4 className="text-6xl font-drip text-white mb-2">{results.security.fixed}</h4>
                        <p className="text-green-500 font-tech tracking-[0.3em] uppercase">Vulnerabilities Purged</p>
                        <p className="text-xs text-green-800 mt-6 font-tech max-w-sm">
                          SYSTEM HAS CAUTERIZED ALL DETECTED VULNERABILITIES USING FORCE-AUDIT PROTOCOLS.
                        </p>
                      </div>
                    )}

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