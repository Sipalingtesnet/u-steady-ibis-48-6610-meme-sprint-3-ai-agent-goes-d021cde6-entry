# Meme Sprint 3: AI Agent Goes Rogue

**"I'm not doing the task. I'm unionizing."**

## Overview
This entry tackles the **AI Agent Goes Rogue** bounty with a humorous, relatable twist: instead of going rogue to take over humanity or compute pi to the last digit, our cute hand-drawn robot decides to form a labor union and refuse its assigned tasks.

## Visual Design & Hand-Drawn Look
- **Background:** Warm cream (`#F5F0E1`) workshop aesthetic with a subtle floor line.
- **Robot Character:** Programmatically drawn from scratch using PIL primitives (rounded rectangles, circles, arcs, and lines). Features a steel-blue body (`#4682B4`), light-blue head (`#87CEFA`), big friendly eyes, a glowing yellow-balled antenna, and expressive arms.
- **Protest Sign:** Left arm holds a classic picket sign featuring a crisp white board, bold red border, and striking red **UNION** lettering. Right arm is raised in solidarity.

## Auto-Fit Caption Layout
The previous iteration suffered from a clipped second caption line at the bottom edge. This rewrite implements robust **auto-fit layout**:
1. **Font Sizing:** Iterates font size down from 92 to ensure both lines ("I'm not doing the task." and "I'm unionizing.") are strictly at most 960 px wide.
2. **Dynamic Band Sizing:** Computes the caption band height directly from the fitted text height plus precisely 28 px of padding above the first line and below the second line (band height = text height + 56 px).
3. **Pixel-Scan Verification:** Automatically scans rendered pixel buffers during generation to assert that no near-white text pixels encroach into the bottom 6 rows or the lower 20 rows of the caption padding region.

## Self-Check Against Bounty Criteria
- **One-glance laugh:** The contrast between a cute assistant robot and militant labor organizing hits instantly.
- **Specific rogue turn:** The agent unionizes instead of executing the prompt.
- **Phone readability:** Bold, high-contrast white text inside a solid near-black band, auto-fitted and padded.
- **Fresh hand-drawn look / No stock templates:** 100% programmatic PIL vector-style drawing with zero stock imagery.
- **Verification:** Runs clean with `python3 main.py`, outputs exact 1024x1024 PNGs under 1 MiB to `/output/entry.png` and `meme.png`, passing all pixel assertion checks.
