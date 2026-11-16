# Encrypted copy of the build kit inside the GitHub repo, so any new session can restore the whole pipeline from GitHub alone.
# The repo is public: everything is AES-256-GCM encrypted with the dashboard password (same one that opens the standalone page).
#   python3 build/kit.py pack && python3 build/ghkit.py pack REPO_DIR [PASSWORD]   -> REPO_DIR/kit/{kit,cur,hist}.enc + manifest.json
#   python3 kit/restore.py PASSWORD [WORK_DIR]   (run from the repo)             -> WORK_DIR/build, data, chk
import sys, os, json, gzip, hashlib, re
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
ITER = 250000
def key(pw, salt): return hashlib.pbkdf2_hmac('sha256', pw.encode(), salt, ITER, 32)
def pack(repo, pw):
    out = os.path.join(repo, 'kit'); os.makedirs(out, exist_ok=True)
    mp = os.path.join(out, 'manifest.json'); man = json.load(open(mp)) if os.path.exists(mp) else {}
    for n in ('kit', 'cur', 'hist'):
        raw = open('kit_out/%s.json' % n, 'rb').read(); h = hashlib.sha256(raw).hexdigest()
        if man.get(n, {}).get('sha256') == h and os.path.exists(os.path.join(out, n + '.enc')): print(n, 'tidak berubah'); continue
        salt, iv = os.urandom(16), os.urandom(12)
        ct = AESGCM(key(pw, salt)).encrypt(iv, gzip.compress(raw, 9, mtime=0), None)
        open(os.path.join(out, n + '.enc'), 'wb').write(b'NKA2' + salt + iv + ct)
        man[n] = {'sha256': h, 'bytes': len(raw)}; print(n, len(raw), '->', len(ct))
    json.dump(man, open(mp, 'w'), indent=1)
def restore(src, pw, work):
    os.makedirs(os.path.join(work, 'kitin'), exist_ok=True)
    for n in ('kit', 'cur', 'hist'):
        b = open(os.path.join(src, n + '.enc'), 'rb').read(); assert b[:4] == b'NKA2'
        raw = gzip.decompress(AESGCM(key(pw, b[4:20])).decrypt(b[20:32], b[32:], None))
        open(os.path.join(work, 'kitin', n + '.json'), 'wb').write(raw)
    k = json.load(open(os.path.join(work, 'kitin', 'kit.json')))
    os.makedirs(os.path.join(work, 'build'), exist_ok=True); open(os.path.join(work, 'build', 'kit.py'), 'w').write(k['build/kit.py'])
    print('kit didekripsi ke %s/kitin. Lanjut:  cd %s && python3 build/kit.py unpack kitin' % (work, work))
if __name__ == '__main__':
    if sys.argv[1] == 'pack':
        pw = sys.argv[3] if len(sys.argv) > 3 else re.search(r"PW = '([^']+)'", open('build/standalone.py').read()).group(1)
        pack(sys.argv[2], pw)
    else: restore(os.path.dirname(os.path.abspath(__file__)), sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '.')
