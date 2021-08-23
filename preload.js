// Preload (Isolated World)
const { contextBridge, ipcRenderer } = require('electron');


const python = require('child_process');
//const proc;


contextBridge.exposeInMainWorld(
  'electron',
  {
    runPython: (c1,c2,c3,c4) => ({return: python.spawn('python3', ['./4GruppeHP.py',c1,c2,c3,c4]).pid}),
    killPython: (pid) => (process.kill(pid)),
    killPythonHard: () => ({return: python.spawn('python3', ['./killPython.py']).pid})
  
  

  }
)