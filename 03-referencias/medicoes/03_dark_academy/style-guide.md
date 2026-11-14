# Measured style guide: referencia_03_dark_academy.mp4

Generated at 14/11/2026 00:10 by measure_reference.py from editonny-engine
Use this to edit another video with similar visual direction. Do not copy speech, promises,
brands, logos, music, people, or result figures from the reference.

How to read this guide:
- **MEASURED**: calculated from the recording, within the stated precision.
- **ESTIMATED**: inferred from measurements; verify against frames and crops.
- **UNKNOWN**: listed at the end. Do not invent these details.

## Overview

- Pacing: 79 cuts in 308.0 s, 15.4 per minute, one new shot every 3.9 seconds on average. **MEASURED**
- Another 18 tentative cuts to inspect; including them would yield 18.9 per minute. **ESTIMATED**
- Face visible in 39% of sampled seconds; typical size: medium shot. **ESTIMATED**
- Captions with ? words per line, centered at 90% of frame height, ? uppercase. **MEASURED**
- Audio: -18.4 LUFS; uncertain (speech has too few pauses for a reliable background measurement; listen to the reference or use the user's description). **ESTIMATED**
- Probable sound effects: 6 (1.2 per minute). **ESTIMATED**

## 1. Technical measurements

| Item | Value |
| --- | --- |
| File | `referencia_03_dark_academy.mp4` |
| Duration | 308.00 s |
| Resolution | 640 x 360 (16:9) |
| Frames per second | 24.00 |
| Audio | aac 2 channels 44100 Hz |
| SHA-256 fingerprint | `2d018e4d76261fee...` |

## 2. Pacing and cuts

Frame-by-frame FFmpeg scene detector. Cut = scene score at least 0.20. Tentative cut: a weak peak at least 8 times its neighborhood level.

| Measurement | Value | Status |
| --- | --- | --- |
| Hard cuts | 79 | MEASURED |
| Cuts per minute | 15.4 | MEASURED |
| Average shot duration | 3.85 s (median 2.42 s) | MEASURED |
| Average time between cuts | 3.82 s | MEASURED |
| Shortest / longest shot | 0.25 s / 33.00 s | MEASURED |
| Longest interval without a cut | 00:06.21 to 00:39.21 | MEASURED |
| Shots shorter than 1.5 seconds | 38% | MEASURED |
| Cuts in the first three seconds | 0 | MEASURED |
| Tentative weak cuts | 18 | ESTIMATED, verify in `review-cuts.jpg` |

Cuts per 10 seconds: 0-10s: 2, 10-20s: 0, 20-30s: 0, 30-40s: 1, 40-50s: 1, 50-60s: 0, 60-70s: 3, 70-80s: 3, 80-90s: 1, 90-100s: 3, 100-110s: 1, 110-120s: 4, 120-130s: 1, 130-140s: 2, 140-150s: 3, 150-160s: 2, 160-170s: 2, 170-180s: 2, 180-190s: 7, 190-200s: 1, 200-210s: 3, 210-220s: 5, 220-230s: 10, 230-240s: 2, 240-250s: 1, 250-260s: 4, 260-270s: 2, 270-280s: 10, 280-290s: 1, 290-300s: 1, 300-310s: 1.

List: 00:03.25, 00:06.21, 00:39.21, 00:40.00, 00:59.29 (probable), 01:02.00, 01:04.38, 01:07.33, 01:14.00, 01:14.62, 01:15.88, 01:25.71, 01:31.50, 01:36.21, 01:39.33, 01:47.38, 01:52.33, 01:54.00, 01:55.08, 01:58.08, 02:05.58, 02:10.58, 02:14.46, 02:20.38, 02:25.00, 02:26.00, 02:33.25, 02:35.67, 02:40.25, 02:49.38, 02:53.75, 02:57.58, 02:59.29 (probable), 03:01.58, 03:02.58, 03:03.58, 03:04.17, 03:04.71, 03:06.00, 03:09.71, 03:14.71, 03:20.96, 03:24.71, 03:25.54, 03:30.71, 03:32.00 (probable), 03:36.67, 03:38.17 (multiple frames), 03:39.21 (multiple frames), 03:39.75, 03:40.00, 03:40.46, 03:40.71, 03:41.00, 03:41.33, 03:41.67 (multiple frames), 03:44.00, 03:45.25, 03:47.25, 03:48.83, 03:49.71 (probable), 03:50.75 (probable), 03:51.58 (probable), 03:52.50 (probable), 03:52.88, 03:55.33, 04:03.38, 04:06.79 (probable), 04:11.88, 04:13.88, 04:15.71, 04:18.12, 04:26.00, 04:27.00, 04:27.25 (probable), 04:27.79 (probable), 04:28.17 (probable), 04:28.71 (probable), 04:29.08 (probable), 04:29.62 (probable), 04:32.17 (probable), 04:33.38, 04:34.00, 04:35.04, 04:35.96, 04:36.42 (probable), 04:36.96, 04:37.50, 04:38.04, 04:38.54, 04:39.08, 04:39.62, 04:40.12 (probable), 04:40.67 (probable), 04:41.12, 04:50.42, 05:00.96.

## 3. Framing and zoom (ESTIMATED, face detection)

| Measurement | Value |
| --- | --- |
| Seconds with a face | 39% |
| Face height | 16% of frame height (medium shot) |
| Eye height | 34% from the top |
| Face position | center |
| Shots without a face: supporting image, screen, or product | 73 of 98 |
| Face-size changes at cuts | median 36% in 2 cuts within the same scene with faces on both sides; 2 changed by at least 6% |
| Zoom at cuts | unlikely |

## 4. Captions and on-screen text

Recognized using text-shaped regions without word recognition, 2 samples per second. Sizes in source pixels and converted to the standard canvas 1920x1080.

| Measurement | Value | Status |
| --- | --- | --- |
| Time with captions | 54% of samples | MEASURED |
| Do captions transcribe speech? | not checked: no transcript | ESTIMATED |
| Main text position: line center | 89.6% of frame height, y = 322 pixels (standard canvas: 967), 23% of captioned time | MEASURED |
| Another position | 36.8% of frame height (standard canvas: 397), 4% of captioned time, between 00:00.00 and 00:07.00 | MEASURED |
| Another position | 49.1% of frame height (standard canvas: 530), 9% of captioned time, between 00:14.50 and 00:30.00 | MEASURED |
| Another position | 56.3% of frame height (standard canvas: 608), 18% of captioned time, between 00:32.00 and 01:05.00 | MEASURED |
| Recognized line height | 12 pixels (standard canvas: 35) | MEASURED |
| Words per line at the main position | median ?, maximum None | MEASURED |
| Simultaneous lines | 1 lines in 63%, 2 lines in 28%, 3 lines in 8%, 4 lines in 1% | MEASURED |
| Uppercase | ? of letters | MEASURED |
| Text changes per minute | 51 (sampled; changes faster than 0.5 seconds are not detected) | MEASURED |
| Font size | approximately 37 pixels on the standard canvas | ESTIMATED |
| Letter shape | not measured | ESTIMATED |
| Text color at the main position | #F9F6EE | ESTIMATED |
| Accent color (spoken word) | #9E090E, in 68% of lines | ESTIMATED |
| Dark outline or shadow | unlikely | ESTIMATED |
| Solid background behind text: box or banner | unlikely | ESTIMATED |
| Closest editonny style | `impact` (mixed case; verify in the extracted frames) | ESTIMATED |
| Similar open fonts (Google Fonts) | Montserrat, Inter, Anton | ESTIMATED |

Text in the first three seconds: yes, in zone middle, up to 41 pixels high, larger than captions: hook title. **MEASURED**

## 5. Colors

Pixel measurements at one frame per second are **MEASURED**. Color roles are **ESTIMATED**: skin, wall,
and clothing contribute to the measurement. Text accents are described in section 4.

| Color | Image fraction | Appearance |
| --- | --- | --- |
| `#060304` | 55% | black |
| `#4B1415` | 9% | red dark |
| `#8C8F7F` | 7% | gray |
| `#CCD7D1` | 7% | white |
| `#3C443B` | 6% | dark gray |
| `#A31F13` | 6% | red |
| `#B76F58` | 3% | red |

Strong visible colors, potential accents: `#621313` red dark, `#B2211B` red, `#C2695C` red, `#D0BB6B` yellow light.

Overall appearance: mean brightness 27%, mean saturation 51%, 61% dark frames, 0% bright frames, temperature warm.

## 6. Audio

All audio findings come from signal measurements; subjective listening was not performed.

| Measurement | Value | Status |
| --- | --- | --- |
| Perceived loudness (integrated) | -18.4 LUFS | MEASURED |
| True peak | 1.4 dBTP | MEASURED |
| Volume variation | 5.7 LU | MEASURED |
| Stereo | yes (left/right correlation 0.933) | MEASURED |
| Voice and background levels | -20.0 / -45.8 dBFS (difference 25.8 dB; speech inferred from the loudest audio intervals, background from the quietest intervals) | ESTIMATED |
| Music | uncertain: speech has too few pauses for a reliable background measurement; listen to the reference or use the user's description | ESTIMATED |
| Probable sound effects | 6 (1.2 per minute), confidence low | ESTIMATED |
| Cuts accompanied by sound within 0.2 seconds | 0% | ESTIMATED |
| Audio attacks per minute, including speech syllables | 126 | MEASURED |

Probable effects: timing and spectral family: 00:10.97 bass:; 00:46.63 bass:; 00:51.70 bass:; 02:46.70 bass:; 02:49.64 bass:; 04:07.32 bass:.

Effect detection method: bass jumps unexplained by speech and sounds within pauses; less reliable without a clean side channel. Musical beats and audible breathing may also be detected.

## 7. Speech

No transcription: disabled or failed. Speech pacing was not measured.

## 8. Visual review (complete after inspecting the contact sheets)

Inspect the contact sheets and review crops. Describe what is visible without copying reference text.

- Video type: speaker, screen, product, tutorial, or mixed:
- Do the detected cuts match the contact sheet? Are any tentative detections real cuts?
- Elements beyond captions: hook title, arrows, screenshots, emoji, progress bar, frame:
- Transitions: hard cut, zoom, whip, flash, or slide:
- Supporting images (B-roll): start times and durations:
- Opening direction in the first three seconds and closing call to action:
- What suits the user's video and what does not:

## 9. What measurement cannot establish

- Exact font name; only apparent width and weight are measured.
- Exact animation curves. Generate a 10 or 30 fps filmstrip for closer inspection.
- Dissolves, soft transitions, and slow digital zooms; the detector identifies abrupt changes.
- Whether a sound is a whoosh, pop, or snap; only timing and frequency range were measured, not listened to.
- Music name, author, or license. Never reuse reference music without rights.
- Editing application, AI model, or whether an object is genuinely 3D.
- Sales or audience results of the reference.
- Without Apple Vision, detection finds text-shaped regions only; words per line and capitalization were not measured.
- Without transcription, between-phrase levels were estimated from the quietest intervals.

## 10. Measurement files

- `style-guide.md`: this guide
- `reference-rules.json`: machine-readable measurements with suggested edit_data.json and HyperFrames settings
- `measured-intervals.csv`: one second per row: shot, cut, visible content, on-screen text, and sound
- `contact-sheets/`: 5 contact sheets, one frame per second, marked cuts and effects
- `review-cuts*.jpg`: frames before and after each detected cut
- `measurements/`: raw frame scene scores, cuts, audio, recognized text, and transcription
