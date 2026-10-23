# Frank Lab Website Maintenance & Editing Guide

This guide explains how to update the Frank Lab website ([https://franklab-cornell.github.io/](https://franklab-cornell.github.io/)), add new lab members, edit page content, and manage GitHub organization collaborators.

---

## Quick Reference: 3-Step Workflow

All source content lives in the `content/` folder and `images/` folder. **Never edit `.html` files directly in `docs/`**, because they are automatically generated.

Whenever you make any changes:

```bash
# 1. Rebuild the QMD pages and compile the static site into docs/
python3 tools/build_qmd.py && ~/.local/bin/quarto render

# 2. (Optional) Preview locally in your browser
~/.local/bin/quarto preview

# 3. Commit and push to GitHub (goes live automatically in ~30 seconds)
git add .
git commit -m "Describe what you updated"
git push origin main
```

---

## 1. Adding and Managing Lab Members

### A. Adding a New Lab Member
1. **Save their photo:**
   - Place a square or portrait headshot in `images/people/` (e.g. `images/people/first-last.jpg`).
   - JPG format is recommended. Keep file size under 1MB.

2. **Add their entry in `content/people.yml`:**
   Open `content/people.yml` and add a new block at the desired position:
   ```yaml
   - name: "Jane Doe"
     role: "Ph.D. Student"
     group: current          # Use "current" for current members, or "alumni" for former members
     photo: "images/people/jane-doe.jpg"
     bio:
       - "Jane joined the Frank Lab in Fall 2026. She graduated from ... where she studied ..."
       - "Outside of the lab, Jane enjoys trail running and hiking in the Finger Lakes."
   ```

3. **(Optional) Adjust photo vertical crop:**
   If the person's face is positioned high or low in their photo:
   - Open `tools/build_qmd.py`.
   - In `PHOTO_POSITIONS`, add their name and crop percentage (e.g. `'Jane Doe': 'center 25%'` to show higher up, or `'center 60%'` to show lower down).

4. **Rebuild & Publish:**
   ```bash
   python3 tools/build_qmd.py && ~/.local/bin/quarto render
   git commit -am "Add Jane Doe to lab members"
   git push origin main
   ```

### B. Moving a Member to Alumni
When a student or postdoc graduates or moves on:
1. Open `content/people.yml`.
2. Change `group: current` to `group: alumni`.
3. Optionally update their role (e.g. `role: "Former Ph.D. Student • Now Postdoc at Stanford"`).
4. Rebuild and push. They will automatically move into the **Alumni** section!

---

## 2. Adding Website Editors & Collaborators

There are two levels where you can add editors:
- **Level A: Organization-Wide** (Inviting members to the `FrankLab-Cornell` organization)
- **Level B: Repository-Specific** (Granting direct write/admin permissions to `franklab-cornell.github.io`)

---

### Method A: Add an Editor to the GitHub Organization

Best for adding Dr. Margaret Frank, permanent staff, postdocs, and students to the lab's GitHub team.

1. Open your Organization People settings:  
   👉 **[https://github.com/orgs/FrankLab-Cornell/people](https://github.com/orgs/FrankLab-Cornell/people)**
2. Click the green **Invite member** button in the top right.
3. Type the person's **GitHub username** or their **email address**.
4. Choose their organization role:
   - **Owner (Admin):** Has complete administrative control over the entire organization, billing, and all repositories.  
     > *Recommendation:* Add **Dr. Margaret Frank** and at least one other permanent/senior member as **Owners** so lab access is never lost when students graduate.
   - **Member:** Can view and contribute to organization repositories without access to organization billing or administrative settings.
5. Click **Send invitation**.  
   *(The invited person will receive an email and an on-screen notification on GitHub to accept the invitation).*

---

### Method B: Add an Editor Specifically to the Website Repository

Best if you want to grant direct push permissions to someone (even outside the organization) specifically for the website repository:

1. Open the Repository Access settings:  
   👉 **[https://github.com/FrankLab-Cornell/franklab-cornell.github.io/settings/access](https://github.com/FrankLab-Cornell/franklab-cornell.github.io/settings/access)**
2. Click the green **Add people** button.
3. Search for their GitHub username or email address.
4. Choose their permission level:
   - **Admin:** Can edit code, configure GitHub Pages, manage custom domains, and add other editors.
   - **Write (Recommended for website editors):** Can push changes, add new photos, edit content, and deploy updates.
   - **Read:** Can view code only.
5. Click **Add [name] to this repository**.

---

### How New Editors Work on the Website

Once invited, an editor can work on the website in two ways:

#### Option 1: On Their Computer (Recommended for full edits and adding photos)
1. Clone the repository:
   ```bash
   git clone https://github.com/FrankLab-Cornell/franklab-cornell.github.io.git
   cd franklab-cornell.github.io
   ```
2. Make edits in `content/` or add photos in `images/`.
3. Rebuild and publish:
   ```bash
   python3 tools/build_qmd.py && quarto render
   git commit -am "Update content"
   git push origin main
   ```
   *(When pushing for the first time, Git will prompt them for their GitHub username and a Personal Access Token created under [https://github.com/settings/tokens](https://github.com/settings/tokens) with the `repo` scope).*

#### Option 2: Quick Edits Directly in the Web Browser
For small typo fixes or text tweaks without installing any software:
1. Open the repository on GitHub: [https://github.com/FrankLab-Cornell/franklab-cornell.github.io](https://github.com/FrankLab-Cornell/franklab-cornell.github.io)
2. Navigate to any file in `content/` (e.g. `content/contact.md`).
3. Click the pencil icon (✏️ **Edit this file**) in the top right.
4. Make your text changes, scroll to the bottom, and click **Commit changes**.
   > *Note:* Edits made directly on GitHub modify the source markdown. To update the live web pages, `build_qmd.py` and `quarto render` should be run and committed to update the `docs/` deployment folder.

---

## 3. Editing Content on Each Page

### 🏠 Home Page (`content/index.md`)
- **Recent News:**
  Scroll down to `## Recent News` and add your newest item at the top of the bullet list:
  ```markdown
  - October 2026 - Frank Lab welcomes our newest graduate student, Jane Doe!
  - September 2026 - Dr. Frank awarded a new grant from NSF for ...
  ```
- **Links in News:**
  Use standard markdown syntax: `[Title of Link](https://example.com)`.

---

### 📖 About Us Page (`content/about.md`)
Contains the lab's mission statement, research philosophy, mentorship approach, and outreach commitments.
- Open `content/about.md` and edit or add markdown sections under headings (`## Section Title`).
- To change the hero photo at the top, replace `images/about/about-lab.jpg`.

---

### 🔬 Research Page (`content/research.md`)
Contains summaries of main research pillars (Graft Incompatibility, Long-distance Communication, Graft-induced Vigor, Mobileomes, Soybean Hybridization).
- Open `content/research.md`.
- To add a new research focus:
  ```markdown
  ## New Research Topic Title
  
  ![Caption for research image](images/research/my-new-figure.jpg)
  
  Brief summary description of this research project and our findings...
  ```
- Place any new figures into `images/research/`.

---

### 📚 Publications Page (`content/publications.md`)
Organized by year in reverse chronological order (`2026`, `2025`, `2024`...).
- Open `content/publications.md`.
- Under the appropriate year heading (or create a new `## 2027` heading), add the paper:
  ```markdown
  **Title of the Paper in Bold.**
  Author list with Frank Lab members (e.g. M.H. Frank).
  *Journal Name in Italics* Volume (Issue) pages (Year). [https://doi.org/...](https://doi.org/...)
  ```

---

### ✉️ Contact Page (`content/contact.md`)
Contains mailing address, office/lab rooms, phone number, email, and prospective student/postdoc hiring info.
- Open `content/contact.md`.
- Edit office or lab room numbers, phone numbers, or hiring blurbs under `## Open Positions`.

---

### 📸 Group Photos Slideshow (`content/slides_meta.json`)
The interactive 15-photo slideshow at the top of the **Lab Members** page is controlled here.
1. Place your new photo in `images/groups/` (e.g. `images/groups/harvest-2026.jpg`).
2. Open `content/slides_meta.json` and add an entry:
   ```json
   [
     "harvest-2026.jpg",
     "harvest-2026",
     "Fall 2026",
     "Field Harvest Celebration",
     "center 50%"
   ]
   ```
   *(The 5 values are: source filename, slug name without extension, eyebrow tag, slide title, and vertical centering position).*
3. Rebuild and publish:
   ```bash
   python3 tools/build_qmd.py && ~/.local/bin/quarto render
   git commit -am "Add new group photo to slideshow"
   git push origin main
   ```

---

## 4. Markdown Formatting Cheatsheet

| Format | Syntax | Result |
| :--- | :--- | :--- |
| **Bold** | `**text**` | **text** |
| *Italics* | `*text*` | *text* |
| **Link** | `[Cornell](https://cornell.edu)` | [Cornell](https://cornell.edu) |
| **Email Link** | `[mhf47@cornell.edu](mailto:mhf47@cornell.edu)` | [mhf47@cornell.edu](mailto:mhf47@cornell.edu) |
| **Image** | `![Alt Text](images/path/to/file.jpg)` | Embedded image |
| **Heading 2** | `## Section Heading` | Major section header |
| **Heading 3** | `### Subsection Heading` | Subsection header |
| **Bullet List** | `- Item 1`<br>`- Item 2` | • Item 1<br>• Item 2 |

---

## 5. Live Website Addresses
- **Production Site:** [https://franklab-cornell.github.io/](https://franklab-cornell.github.io/)
- **GitHub Repository:** [https://github.com/FrankLab-Cornell/franklab-cornell.github.io](https://github.com/FrankLab-Cornell/franklab-cornell.github.io)
- **Organization Members & Access:** [https://github.com/orgs/FrankLab-Cornell/people](https://github.com/orgs/FrankLab-Cornell/people)
