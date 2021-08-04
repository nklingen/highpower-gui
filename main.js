const { app, BrowserWindow } = require('electron')
const {PythonShell} = require('python-shell');
const path = require('path')



function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
  })

  win.loadFile('index.html')

  var python = require('child_process').spawn('python', ['./script.py']);
  python.stdout.on('data',function(data){
      console.log("data: ",data.toString('utf8'));
  });

}

// Quit the app when all windows are closed (Windows & Linux)
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})


// Open a window if none are open (macOS)
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
  
})

