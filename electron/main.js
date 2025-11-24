const { app, BrowserWindow } = require('electron');
const { spawn } = require("child_process")
const path = require("path")
const http = require("http")

let pyProcess = null

function startPythonServer() {
  const pythonExe = path.join(__dirname, "..", "python", "venv", "bin", "python3")
  const scriptPath = path.join(__dirname, "..", "python", "app", "simple_dash.py")

  pyProcess = spawn(pythonExe, [scriptPath], {
    cwd: path.join(__dirname, "..", "python", "app"),
    stdio: "inherit"
  })

  pyProcess.on("exit", (code) => {
    console.log("Python exited:", code)
  })
}

function waitForServer(url, callback) {
  const check = () => {
    http.get(url, () => {
      callback()    // → サーバ起動した瞬間に呼ばれる
    }).on("error", () => {
      setTimeout(check, 500) // 半秒ごとにリトライ
    })
  }
  check()
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
  });

  const url = "http://127.0.0.1:8050/"

  // Dash 起動後に読み込む
  waitForServer(url, () => {
    console.log("Dash ready → Loading in Electron")
    win.loadURL(url)
  })
}

app.whenReady().then(() => {
  startPythonServer()
  createWindow()
})