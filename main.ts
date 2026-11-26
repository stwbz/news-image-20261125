// main.ts — entrypoint for the news-image-20261125 entry.
//
// The front page is drawn by draw.py (Python + Pillow) into entry.png in
// this directory. This entrypoint only places that image where the make.fun
// grader looks for it: $MAKEFUN_OUTPUT_DIR/entry.png.
//
// The image is a newspaper front page for Wednesday 25 November 2026:
// 35 stories, three data-rich heroes (Dow comeback, Hormuz, UCL), a UTC
// strip, a numbers strip, a world map and a DATE CHECK box. The program
// itself never draws anything — it copies the pre-rendered PNG.
//
// Build the image first (from this directory):
//   python3 draw.py
// which writes entry.png (819x1024 portrait, deterministic, under 1 MiB).
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR;
if (!out) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}

mkdirSync(out, { recursive: true });

const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png not found next to main.ts — run python3 draw.py first");
}
copyFileSync(src, join(out, "entry.png"));
console.log("entry.png copied to " + out);
