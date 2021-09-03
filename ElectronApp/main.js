const { app, BrowserWindow } = require('electron')
const {PythonShell} = require('python-shell');

var AutoLaunch = require('auto-launch');
const path = require('path')


function createWindow () {
  win = new BrowserWindow({
    
    width: 800,
    height: 600,
    fullscreen: true
    
  })

  win.loadFile('index.html')



}

// Quit the app when all windows are closed (Windows & Linux)
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})


// Open a window if none are open (macOS)
app.whenReady().then(() => {


  var autoLauncher = new AutoLaunch({
      name: "GUI"
  });
  // Checking if autoLaunch is enabled, if not then enabling it.
  autoLauncher.isEnabled().then(function(isEnabled) {
    if (isEnabled) return;
    autoLauncher.enable();
  }).catch(function (err) {
    throw err;
  });


  
  createWindow()

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
  
})

