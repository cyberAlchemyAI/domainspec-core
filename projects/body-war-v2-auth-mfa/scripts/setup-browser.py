#!/usr/bin/env python3
"""Prepare exact local browser tooling; no root install or cache mutation."""
from pathlib import Path
import hashlib,json,os,stat,subprocess,urllib.request,zipfile
root=Path(__file__).resolve().parent.parent
os.chdir(root)
lock=json.loads(Path('provenance/browser.json').read_text())['files']
archive=Path('.tools/chromium-1217.zip');archive.parent.mkdir(exist_ok=True)
if not archive.exists():
 urllib.request.urlretrieve('https://cdn.playwright.dev/builds/cft/147.0.7727.15/linux64/chrome-linux64.zip',archive)
if hashlib.sha256(archive.read_bytes()).hexdigest()!=lock[str(archive)]:raise SystemExit('Browser archive digest mismatch')
target=Path('.tools/chromium-1217');target.mkdir(exist_ok=True)
if not (target/'chrome-linux64/chrome').exists():
 with zipfile.ZipFile(archive) as z:
  for item in z.infolist():
   name=Path(item.filename);mode=item.external_attr>>16
   if name.is_absolute() or '..' in name.parts or stat.S_ISLNK(mode):raise SystemExit('Unsafe archive member')
   z.extract(item,target)
   if mode:os.chmod(target/name,mode&0o777)
packages=Path('.tools/browser-libs');packages.mkdir(exist_ok=True)
for name,version in [('libnspr4','2:4.38.2-1ubuntu1'),('libnss3','2:3.120-1ubuntu2.1'),('libasound2t64','1.2.15.3-1ubuntu1.1')]:
 if not list(packages.glob(name+'_*.deb')):subprocess.run(['apt','download',name+'='+version],cwd=packages,check=True)
for item in packages.glob('*.deb'):
 if str(item) not in lock or hashlib.sha256(item.read_bytes()).hexdigest()!=lock[str(item)]:raise SystemExit('Library package digest mismatch: '+str(item))
 subprocess.run(['dpkg-deb','-x',str(item),str(packages/'root')],check=True)
chrome=target/'chrome-linux64/chrome'
if hashlib.sha256(chrome.read_bytes()).hexdigest()!=lock[str(chrome)]:raise SystemExit('Browser executable digest mismatch')
subprocess.run([str(chrome),'--version'],check=True,env={**os.environ,'LD_LIBRARY_PATH':str((packages/'root/usr/lib/x86_64-linux-gnu').resolve())})
