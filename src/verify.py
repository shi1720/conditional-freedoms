"""Verify the pinned source files before rebuilding any derived manifest."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]

def verify():
    manifest=json.loads((ROOT/'data'/'manifest.json').read_text())
    for source in manifest:
        b=(ROOT/'data'/source['file']).read_bytes()
        if hashlib.sha256(b).hexdigest()!=source['sha256'] or len(b)!=source['bytes']:
            raise ValueError('Source mismatch: '+source['file'])
    print(f'{len(manifest)} pinned source files verified')

if __name__=='__main__':verify()
