#!/usr/bin/env bash
# Serves this checkout on a free local port and runs scripts/motion-check.mjs
# against it: does every room's motion actually run (backdrop, hero motif,
# replays, SMIL drawings, tabbed pictures, scroll reveal) with no JavaScript
# error, at 1440 and 390 wide. A tool, not a gate; see the .mjs header.
#
#   scripts/motion-check.sh                       # home, stack and every room
#   scripts/motion-check.sh services/qryx.html    # named pages only
#
# Needs Node 22 or newer, python3, and Chrome (CHROME overrides the path).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="${ROOT:-$(cd "$here/.." && pwd)}"
command -v node >/dev/null || { echo "motion-check: node not found" >&2; exit 64; }
port="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')"
python3 -m http.server "$port" --bind 127.0.0.1 --directory "$root" >/dev/null 2>&1 &
server=$!
trap 'kill "$server" 2>/dev/null || true' EXIT INT TERM
for _ in $(seq 1 100); do
  python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:$port/', timeout=1)" 2>/dev/null && break
  sleep 0.1
done
node "$here/motion-check.mjs" "http://127.0.0.1:$port/" "$@"
