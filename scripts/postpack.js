const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const readmePath = path.join(rootDir, 'README.md');
const backupPath = path.join(rootDir, '.readme.bak');

if (fs.existsSync(backupPath)) {
    fs.copyFileSync(backupPath, readmePath);
    fs.unlinkSync(backupPath);
    console.log('Restored original README.md');
}
