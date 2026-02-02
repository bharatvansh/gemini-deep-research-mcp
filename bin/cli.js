#!/usr/bin/env node

const { spawn } = require('child_process');
const { platform } = require('os');

// Try uvx first (recommended), fall back to python -m
function runWithUvx() {
    const proc = spawn('uvx', ['gemini-deep-research-mcp'], {
        stdio: 'inherit',
        shell: platform() === 'win32'
    });

    proc.on('error', (err) => {
        if (err.code === 'ENOENT') {
            console.error('Error: uvx not found. Please install uv first:');
            console.error('');
            if (platform() === 'win32') {
                console.error('  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"');
            } else {
                console.error('  curl -LsSf https://astral.sh/uv/install.sh | sh');
            }
            console.error('');
            console.error('Or install the Python package directly:');
            console.error('  pip install gemini-deep-research-mcp');
            console.error('  gemini-deep-research-mcp');
            process.exit(1);
        }
        throw err;
    });

    proc.on('exit', (code) => {
        process.exit(code || 0);
    });
}

runWithUvx();
