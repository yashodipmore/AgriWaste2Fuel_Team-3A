const { spawn } = require('child_process');
const path = require('path');

// Change working directory to the correct location
process.chdir(__dirname);

// Start the React development server
const child = spawn('npx', ['react-scripts', 'start'], {
  stdio: 'inherit',
  shell: true,
  cwd: __dirname
});

child.on('error', (error) => {
  console.error('Error starting React app:', error);
});

child.on('close', (code) => {
  console.log(`React app exited with code ${code}`);
});
