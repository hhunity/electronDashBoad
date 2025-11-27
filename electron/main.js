const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const http = require("http");
const fs = require("fs");

let pyProcess = null;
let mainWindow = null;
let serverReady = false;

function resolvePythonExe() {
  const candidates = [
    path.join(__dirname, "..", "python", "venv", "bin", "python3"),
    path.join(__dirname, "..", "python", "venv", "bin", "python"),
    "python3",
    "python",
  ];
  return candidates.find((p) => {
    try {
      return fs.existsSync(p);
    } catch {
      return false;
    }
  });
}

function startPythonServer() {
  const pythonExe = resolvePythonExe();
  if (!pythonExe) {
    throw new Error("Python executable not found (tried venv and system python).");
  }

  const scriptPath = path.join(__dirname, "..", "python", "app", "app.py");
  pyProcess = spawn(pythonExe, [scriptPath], {
    cwd: path.join(__dirname, "..", "python", "app"),
    stdio: "inherit",
    env: {
      ...process.env,
      PYTHONUNBUFFERED: "1",
      DASH_DEBUG_MODE: "0", // reloader を無効化
      FLASK_ENV: "production",
    },
  });

  pyProcess.on("error", (err) => {
    console.error("Failed to start python:", err);
  });

  pyProcess.on("exit", (code, signal) => {
    console.log("Python exited:", code, signal);
    if (!serverReady && mainWindow) {
      mainWindow.loadURL(
        `data:text/html,<h3>Python app exited before startup.</h3><p>code: ${code}, signal: ${signal}</p>`
      );
    }
  });
}

function waitForServer(url, timeoutMs = 20000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const check = () => {
      const req = http.get(url, (res) => {
        res.destroy();
        resolve();
      });
      req.on("error", () => {
        if (Date.now() - start > timeoutMs) {
          reject(new Error("Server did not start in time."));
        } else {
          setTimeout(check, 500);
        }
      });
    };
    check();
  });
}

async function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
  });
  // 起動時に最大化して全画面サイズで表示
  mainWindow.maximize();

  // Electron だとデフォルトズームが効いて文字が大きく見える場合があるので固定する
  mainWindow.webContents.setZoomFactor(1);
  // mainWindow.webContents.setVisualZoomLevelLimits(1, 1);
  // setLayoutZoomLevelLimits は環境によって真っ白になることがあるので使用しない
  mainWindow.webContents.on("did-finish-load", () => {
    mainWindow.webContents.setZoomFactor(1);
  });

  const url = "http://127.0.0.1:8050/";
  // 起動中に真っ白になるのを避けるため簡易の待機画面を表示
  mainWindow.loadURL("data:text/html,<p>Starting Dash server...</p>");

  // Dash 起動後に読み込む
  try {
    await waitForServer(url);
    serverReady = true;
    console.log("Dash ready → Loading in Electron");
    mainWindow.loadURL(url);
  } catch (err) {
    console.error("Dash server did not become ready:", err);
    mainWindow.loadURL(`data:text/html,Dash server failed to start: ${err.message}`);
  }
}

app.whenReady().then(() => {
  startPythonServer();
  createWindow();
});

app.on("before-quit", () => {
  if (pyProcess) {
    pyProcess.kill();
  }
});
