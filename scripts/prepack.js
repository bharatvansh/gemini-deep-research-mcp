const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const readmePath = path.join(rootDir, 'README.md');
const npmReadmePath = path.join(rootDir, 'README.npm.md');
const backupPath = path.join(rootDir, '.readme.bak');

if (fs.existsSync(npmReadmePath)) {
    if (!fs.existsSync(backupPath)) {
        fs.copyFileSync(readmePath, backupPath);
    }
    fs.copyFileSync(npmReadmePath, readmePath);
    console.log('Swapped README.md with README.npm.md for npm package');
}
