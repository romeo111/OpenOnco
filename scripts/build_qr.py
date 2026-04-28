"""Generate a QR PNG that encodes a patient profile for CSD Lab reports.

Usage:
    py scripts/build_qr.py examples/patient_csd_1_demo_braf_mcrc.json out/qr.png

Output: PNG with embedded URL https://openonco.info/try.html#p=<base64-gzip-json>

The patient profile lives entirely in the URL hash — no server-side state,
no database. The QR is decoded by the user's phone camera, which opens
/try.html; that page reads ``window.location.hash`` and runs the engine in
the browser. CHARTER §9.3 compliance: PHI never reaches a server.

For the canonical CSD-1 demo (BRAF V600E mCRC) the encoded URL is well
under the 1500-char QR-25 cap, so a single standard-density QR suffices.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow ``py scripts/build_qr.py …`` from the repo root without installing
# the package — _token_helpers lives next to this script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts._token_helpers import encode as encode_patient_token  # noqa: E402

try:
    import qrcode
except ImportError:
    print("Install: pip install qrcode[pil]", file=sys.stderr)
    sys.exit(1)


def build_url(patient_dict: dict, base: str = "https://openonco.info") -> str:
    """Patient dict → openonco.info/try.html#p=<token> URL."""
    token = encode_patient_token(patient_dict)
    return f"{base}/try.html#p={token}"


def build_qr_png(url: str, output_path: Path, box_size: int = 10) -> None:
    """Write a black-on-white PNG QR encoding ``url`` to ``output_path``.

    ``error_correction=M`` (~15% recovery) is the QR sweet spot for
    printed lab reports — survives smudging without ballooning the symbol
    size. ``version=None`` lets qrcode auto-pick the smallest version
    that fits the URL.
    """
    qr = qrcode.QRCode(
        version=None,  # auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: build_qr.py <patient.json> <out.png>", file=sys.stderr)
        return 2
    patient = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    url = build_url(patient)
    print(f"URL: {url}")
    print(f"URL length: {len(url)} chars")
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    build_qr_png(url, out)
    print(f"QR written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
