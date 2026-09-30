const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../dist');
const mime = {'.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.csv': 'text/csv'};
function createServer() {
  const rules = fs.readFileSync(path.join(root, '_redirects'), 'utf8').split(/\r?\n/).filter(x => x && !x.startsWith('#')).map(x => x.trim().split(/\s+/));
  return http.createServer((req, res) => {
    const url = new URL(req.url, 'http://localhost');
    let pathname;
    try {pathname = decodeURIComponent(url.pathname);} catch {res.writeHead(400).end(); return;}
    const rule = rules.find(([source]) => source === pathname || (source.endsWith('*') && pathname.startsWith(source.slice(0, -1))));
    if (rule) {res.writeHead(Number(rule[2]), {Location: rule[1] + url.search}).end(); return;}
    let target = path.resolve(root, '.' + pathname);
    if (!target.startsWith(root + path.sep) && target !== root) {res.writeHead(403).end(); return;}
    if (fs.existsSync(target) && fs.statSync(target).isDirectory()) {
      if (!pathname.endsWith('/')) {res.writeHead(301, {Location: pathname + '/' + url.search}).end(); return;}
      target = path.join(target, 'index.html');
    }
    if (!fs.existsSync(target) && !path.extname(target) && fs.existsSync(target + '.html')) target += '.html';
    if (!fs.existsSync(target) || !fs.statSync(target).isFile()) {res.writeHead(404).end('Not found'); return;}
    res.writeHead(200, {'Content-Type': mime[path.extname(target)] || 'application/octet-stream'});
    fs.createReadStream(target).pipe(res);
  });
}
module.exports = {createServer};
if (require.main === module) createServer().listen(3000, '127.0.0.1', () => console.log('Preview: http://127.0.0.1:3000'));
