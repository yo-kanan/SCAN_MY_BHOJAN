const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 1280,
        height: 720,
        show: false, // Don't show until ready to prevent white flash
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false, // Allows using require() in HTML for simple setups
            // preload: path.join(__dirname, 'preload.js') // Best practice for later
        }
    });

    // Load the initial loading screen.
    mainWindow.loadFile('loading.html');

    // Maximize the window (Maximized Windowed Mode)
    mainWindow.maximize();

    // Show window when ready
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
    createWindow();

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit();
});