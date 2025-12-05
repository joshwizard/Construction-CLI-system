# Quick Start Guide

## Web Interface (Recommended for Beginners)

### Step 1: Start the Web Server
```bash
./start-web.sh
```

### Step 2: What Happens
- The script installs dependencies (first time only)
- Starts a web server on your computer
- **The server keeps running** - this is normal!
- Your browser should open automatically to `http://localhost:3000`

### Step 3: Use the Web Terminal
- Type commands in the browser terminal
- Try: `buildcli --help`
- Try: `buildcli project create "My Project" --budget 50000`

### Step 4: Stop the Server
- Press `Ctrl+C` in the terminal when done
- Or just close the terminal window

## Manual Browser Access
If browser doesn't open automatically:
1. Open any web browser
2. Go to: `http://localhost:3000`
3. Start using the web terminal!

## Troubleshooting

**"npm not found"**
- Install Node.js from https://nodejs.org

**"Port 3000 already in use"**
- Close other applications using port 3000
- Or use: `PORT=3001 npm start` in the web-frontend folder

**Browser doesn't open**
- Manually open `http://localhost:3000`

## Alternative: Direct CLI
If you prefer command line:
```bash
./install.sh
buildcli --help
```