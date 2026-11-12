"""Clean single-line progress wrapper for running Remotion renders in Google Colab."""

from __future__ import annotations

from collections import deque
import os
import re
import shutil
import subprocess
import sys
import time
from typing import Sequence

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
RENDERED_RE = re.compile(r"Rendered\s+(\d+)/(\d+)(?:,\s*time remaining:\s*(.+))?$")
ENCODED_RE = re.compile(r"Encoded\s+(\d+)/(\d+)")
BUNDLING_RE = re.compile(r"Bundling\s+(\d+)%")
COPYING_RE = re.compile(r"Copying public dir\s+(.+)")
DOWNLOAD_RE = re.compile(r"(?:Getting|Downloading) Chrome.*?(-\s*.+)?$")


def _has_nvidia_gpu() -> bool:
    if not shutil.which("nvidia-smi"):
        return False
    res = subprocess.run(
        ["nvidia-smi"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return res.returncode == 0


def _get_ipython_clear():
    try:
        from IPython import get_ipython
        from IPython.display import clear_output

        if get_ipython() is not None:
            return clear_output
    except Exception:
        pass
    return None


def _progress_bar(ratio: float, width: int = 20) -> str:
    clamped = max(0.0, min(1.0, ratio))
    filled = int(round(clamped * width))
    return "#" * filled + "-" * (width - filled)


def run_render(
    composition: str,
    out_path: str,
    extra_args: Sequence[str] = (),
    cwd: str | None = None,
    update_interval_sec: float = 1.0,
) -> None:
    """Run `npx remotion render` and display a single in-place updating status line."""
    workdir = cwd or os.getcwd()
    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    npx_bin = shutil.which("npx") or "npx"
    use_gpu = _has_nvidia_gpu()
    mode_label = (
        "GPU T4: headless-shell + NVENC"
        if use_gpu
        else "CPU: headless-shell + libx264 veryfast"
    )

    cmd = [npx_bin, "remotion", "render", composition, out_path, "--chrome-mode=headless-shell"]
    if use_gpu:
        cmd.extend(["--hardware-acceleration=if-possible", "--video-bitrate=8M"])
    else:
        cmd.extend(["--x264-preset=veryfast", "--crf=21"])
    cmd.extend(extra_args)

    clear_fn = _get_ipython_clear()
    last_draw_time = 0.0
    last_drawn_line = ""
    last_encoded: tuple[int, int] | None = None
    rendered_done = False
    log_tail: deque[str] = deque(maxlen=30)

    def draw(text: str, force: bool = False) -> None:
        nonlocal last_draw_time, last_drawn_line
        now = time.monotonic()
        if not force and text == last_drawn_line:
            return
        if not force and (now - last_draw_time) < update_interval_sec:
            return
        last_draw_time = now
        last_drawn_line = text
        if clear_fn is not None:
            clear_fn(wait=True)
            print(text, flush=True)
        else:
            sys.stdout.write(f"\r{text[:100]:<100}")
            sys.stdout.flush()

    draw(f"[{composition}] ({mode_label}) Memulai render...", force=True)

    proc = subprocess.Popen(
        cmd,
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    try:
        assert proc.stdout is not None
        for raw_line in proc.stdout:
            # Handle both \r and \n cleanly without letting DOM output grow
            for part in raw_line.replace("\r", "\n").splitlines():
                line = ANSI_RE.sub("", part).strip()
                if not line:
                    continue
                log_tail.append(line)

                m_render = RENDERED_RE.match(line)
                if m_render:
                    done = int(m_render.group(1))
                    total = max(1, int(m_render.group(2)))
                    eta = (m_render.group(3) or "").strip()
                    pct = (done / total) * 100.0
                    if done >= total:
                        rendered_done = True
                    bar = _progress_bar(done / total)
                    enc_info = (
                        f" | Encoded: {last_encoded[0]}/{last_encoded[1]}"
                        if last_encoded
                        else ""
                    )
                    eta_info = f" | Sisa: {eta}" if eta else ""
                    draw(
                        f"[{composition}] [{bar}] {pct:5.1f}% | {done}/{total} frame{eta_info}{enc_info}",
                        force=(done == 0 or done >= total),
                    )
                    continue

                m_enc = ENCODED_RE.match(line)
                if m_enc:
                    e_done = int(m_enc.group(1))
                    e_total = max(1, int(m_enc.group(2)))
                    last_encoded = (e_done, e_total)
                    if rendered_done:
                        bar = _progress_bar(e_done / e_total)
                        pct = (e_done / e_total) * 100.0
                        draw(
                            f"[{composition}] Encoding MP4 [{bar}] {pct:5.1f}% ({e_done}/{e_total})",
                            force=(e_done >= e_total),
                        )
                    continue

                m_bundle = BUNDLING_RE.match(line)
                if m_bundle:
                    pct = int(m_bundle.group(1))
                    draw(f"[{composition}] Bundling kode... {pct}%", force=(pct >= 100))
                    continue

                m_copy = COPYING_RE.match(line)
                if m_copy:
                    draw(f"[{composition}] Menyalin aset public... {m_copy.group(1)}")
                    continue

                if "Getting composition" in line:
                    draw(f"[{composition}] Memuat komposisi...", force=True)
                    continue

                if "Rendering frames done" in line:
                    rendered_done = True
                    draw(f"[{composition}] Render frame selesai, menuntaskan encoding MP4...", force=True)
                    continue

                if "Stitching done" in line:
                    draw(f"[{composition}] Menggabungkan audio & video...", force=True)
                    continue

                if DOWNLOAD_RE.search(line):
                    draw(f"[{composition}] {line}")

        rc = proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        if clear_fn is None:
            print()
        raise

    if rc != 0:
        if clear_fn is not None:
            clear_fn(wait=True)
        else:
            print()
        print(f"ERROR: Render {composition} gagal (exit code {rc}). Log terakhir:")
        for item in log_tail:
            print(" ", item)
        raise subprocess.CalledProcessError(rc, cmd)

    size_mb = os.path.getsize(out_path) / (1024 * 1024) if os.path.exists(out_path) else 0.0
    final_msg = f"[{composition}] Selesai! ({mode_label}) -> {out_path} ({size_mb:.1f} MB)"
    if clear_fn is not None:
        clear_fn(wait=True)
        print(final_msg, flush=True)
    else:
        print(f"\r{final_msg:<100}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: colab_render.py <composition> <out_path> [extra remotion args...]")
        sys.exit(2)
    run_render(sys.argv[1], sys.argv[2], extra_args=sys.argv[3:])
