# Dashboard NKA2 — OPPO sell-out (MC-ERABLUE & MC-GTN)

- `index.html` — halaman dashboard standalone (terenkripsi, dibuka dengan password dashboard). Disajikan lewat GitHub Pages.
- `kit/` — build kit terenkripsi (AES-256-GCM, password yang sama): skrip update, template halaman, file mapping, dan data penjualan. Tidak ada data yang terbaca tanpa password.

## Melanjutkan update di sesi baru (Claude / Opus)

```bash
git clone https://github.com/suryanderson/Surya.git repo
pip install cryptography --break-system-packages
python3 repo/kit/restore.py '<password dashboard>' W      # dekripsi kit ke W/kitin
cd W && python3 build/kit.py unpack kitin                  # membangun ulang build/ dan data/
mkdir -p d3pkg && (cd d3pkg && npm i d3@7.9.0)
cat build/README.md                                        # runbook lengkap
python3 build/run.py --psi <file PSI>.xlsx                 # update + render + tes + daftar yang perlu dipublish
```

Setelah publish: `python3 build/run.py --mark && python3 build/kit.py pack && python3 build/ghkit.py pack ../repo`, salin `build/Dashboard_NKA2.html` ke `repo/index.html`, lalu commit dan push.

Password tidak disimpan di repo ini.
