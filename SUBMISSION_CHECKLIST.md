# SUBMISSION CHECKLIST — Garrafeira Bali

## ⏰ DEADLINE — READ FIRST

Official timeline (from the competition Overview → Timeline page):
**Submissions due July 6, 2026 at 11:59 PM PT.**
In Bali time (WITA, UTC+8) that is **Tuesday July 7, 2:59 PM**.
Draft (unsubmitted) writeups are NOT judged — you must click **Submit**.

## Official requirements (verified against the competition pages)

- One submission per team; team size up to 5 (you're solo — fine).
- Kaggle Writeup ≤ 2,500 words, with a selected **Track**.
- Media Gallery: **cover image (required)** + **video (required)**.
- Video: ≤ 5 minutes, published on **YouTube**.
- Public Project Link: live demo OR public GitHub repo **with setup
  instructions** (we use GitHub — the README covers this).
- Demonstrate ≥ 3 course key concepts (we demonstrate 4:
  ADK multi-agent, Security features, Agent skills, Antigravity).
- 🚨 No API keys or passwords in the code (checked: only .env.example
  with a placeholder; .env is git-ignored).

## Steps, in order

1. **GitHub — push the repo (15 min)**
   - Create a public repo `garrafeira-bali` on github.com.
   - From the project folder:
     ```
     git init
     git add .
     git commit -m "Garrafeira Bali - AI Agents capstone"
     git branch -M main
     git remote add origin https://github.com/<you>/garrafeira-bali.git
     git push -u origin main
     ```
   - Confirm on github.com that `.env` is NOT there and the mermaid
     diagram renders in the README.
   - Replace `<your-username>` in README.md and KAGGLE_WRITEUP.md with
     your real GitHub username.

2. **Smoke-test once with your API key (15 min)**
   - `cp .env.example .env`, paste your AI Studio key, `pip install -r
     requirements.txt`, `adk web`, run the 4 demo conversations from
     the README. Reset `garrafeira/data/inventory.json` to 24/18/12 and
     delete `garrafeira/data/orders.json` afterwards.

3. **Record the video (45–60 min incl. one dry run)**
   - Follow `VIDEO_SCRIPT.md`. Keep it under 5:00.
   - Upload to YouTube as Public or Unlisted. Test the link in an
     incognito window.

4. **Create the Kaggle Writeup (20 min)**
   - Go to the competition → click **New Writeup**.
   - Paste Title, Subtitle and body from `KAGGLE_WRITEUP.md`
     (insert your real GitHub + YouTube URLs in the Links section).
   - Select Track: **Agents for Business**.
   - Media Gallery: upload `cover.png` + attach the YouTube video.
   - Attach the GitHub URL as the Project Link.

5. **SUBMIT (2 min — do not skip)**
   - Click **Submit** (top-right). Verify the writeup shows as
     *submitted*, not draft.

## Final sanity checks

- [ ] Writeup submitted (not draft) before July 7, 2:59 PM Bali time
- [ ] Track = Agents for Business selected
- [ ] Cover image visible in Media Gallery
- [ ] YouTube video ≤ 5 min, opens without login
- [ ] GitHub repo public, README setup steps work, no secrets
- [ ] Real URLs (not placeholders) in the writeup Links section
