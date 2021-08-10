// Preload (Isolated World)
const { contextBridge, ipcRenderer } = require('electron');


const python = require('child_process');
//const proc;

function helper() {
  const ls = python.spawn('python', ['./receiveData.py'])
  
  ls.stdout.on('data',function(data){
    console.log("data: ",data.toString('utf8'));
    return data.toString('utf8');
  });

    return "hello2"

    
}

contextBridge.exposeInMainWorld(
  'electron',
  {
    runPython: (i) => ({return: python.spawn('python', ['./script.py',i]).pid}),
    killPython: (pid) => (process.kill(pid)),
    getInformation: (i) => ({return:helper()})
  
  

  }
)