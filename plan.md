In this project, we will help Margaret to copy her lab webpage on wix.com and move it to github.io as a static website.

First, we need to download all the content from the current website. 
go to https://hrt388.wixsite.com/website from the firefox in this computer and browse the pages like a human, and try to download everything on the pages.

---

A running log of everything done is in [LOG.md](LOG.md).

## Steps

Reference: [Dialogue.argon.md](Dialogue.argon.md) (Quarto workflow). The GitHub account, organization and repo are created later by the user, so Steps 2-4 are done locally first.

### Step 1: Download all content from the Wix site (DONE)
- Saved to `original_site/`: raw HTML, text, screenshots, 66 original images, image-to-page map and an inventory in `original_site/README.md`.
- The Wix Media Manager export in Dialogue Phase 1 is not needed. The images were downloaded directly from the public site.
- Optional: do a real interactive browse (scroll and click) with Playwright and Firefox to check nothing is hidden.

### Step 2: Clean up the content for the new site (Dialogue Phase 1, part 2) (DONE)
- Result in `content/` (Markdown plus `people.yml`) and `images/` (10.5 MB). Details and open questions for Margaret are in `LOG.md`.
- Turn `original_site/text/*.md` into clean Markdown with no Wix menu or footer text.
  - Pages: `index` (Home and news), `about`, `research`, `people` (Lab Members), `publications`, `contact`.
- Match Lab Members photos to people using `original_site/html/lab-members.html`.
- Resize and compress images (the originals total about 199 MB) into `images/`, and add alt text.
- Fix links:
  - Replace the Cornell library proxy links (`proxy.library.cornell.edu`) with public DOI or publisher links.
  - Turn plain-text URLs in the news into proper links.

### Step 3: Choose the site generator and set up the project locally (Dialogue Phase 3) (DONE)
- Site generator chosen: **Quarto** (local, Markdown-based, outputs cleanly to `docs/` for GitHub Pages).
- Configured `_quarto.yml` with custom navbar (Home, About Us, Research, Publications, Lab Members, Contact), footer, and `output-dir: docs`.

### Step 4: Build the pages and match the look of the original (Dialogue Phase 3, steps 3-5) (DONE)
- Created `.qmd` pages via `tools/build_qmd.py` from cleaned content in Step 2.
- Responsive layout with Cornell Carnelian palette (`#B31B1B`), custom dark navbar, elegant card layouts, and custom `styles.css`.
- Lab Members page: responsive card grid with confirmed member headshots (Photo A = Jessica Morgan, Photo B = Elise Boisvert), role, and bio.
- Research page: hero images, figure captions, and section anchors.
- Clean build verified: `quarto render` compiles cleanly into `docs/` (11 MB total).
- Visual verification screenshots captured in `_review/local_site/*.png`.

### Step 5: Review with Margaret
- Check content accuracy, because the Wix site's last major update was in 2025.
- Update stale items, and decide whether to keep the old Wix "Wix ad" and "©2020" footer. Use a new footer instead.
- Get approval before publishing.

### Step 6: Publish to GitHub Pages (later, after the user creates the account) (Dialogue Phases 2 and 4)
- The user creates a GitHub Organization (e.g. `frank-lab-cornell`) and adds Margaret and one more senior member as **Owners**.
- Create the public repo `<org>.github.io`, then commit and push this project.
- In Settings -> Pages, choose branch `main` and folder `/docs`, then wait about a minute for the site to go live.
- Optional: custom domain, and keep the Wix site up until the new site is verified.
