# Daily report GTN (terenkripsi)

`gtn_daily.enc.json` = laporan harian GTN untuk grup Lark, terenkripsi dengan password dashboard.
Field `data_until` (tidak terenkripsi) = tanggal data terakhir.

Isi setelah didekripsi (JSON):
- `data_until`, `period`, `time_gone`
- `messages`: 3 pesan, masing-masing `time_wib` (08:45 / 09:30 / 10:00), `key`, `text` (caption siap kirim), `mentions` (nama untuk di-@), `areas_below_100`

Dekripsi (Python):

```python
import json, base64, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
e = json.load(open("gtn_daily.enc.json"))
d = lambda s: base64.b64decode(s)
key = hashlib.pbkdf2_hmac("sha256", PASSWORD.encode(), d(e["salt"]), e["iter"], 32)
report = json.loads(AESGCM(key).decrypt(d(e["iv"]), d(e["ct"]), None))
```

Jadwal kirim ke grup GTN: 08:45 WIB (All Type & Value), 09:30 WIB (A7 Pro & Reno16), 10:00 WIB (Find X10 PO).
Kirim `text` apa adanya dan @mention nama di `mentions`. Jika `data_until` bukan tanggal kemarin, tambahkan "Catatan: data sampai <data_until>" di awal pesan.
