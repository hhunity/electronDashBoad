const { app, BrowserWindow } = require('electron');
const { spawn } = require("child_process");
const py = spawn("python3", ["../dash/app.py"]);

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
    }
  });

  win.loadURL("http://127.0.0.1:8050/");  // Test
}

app.whenReady().then(createWindow);