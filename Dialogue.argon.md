Because Wix relies on proprietary server-side code, you cannot directly export a Wix website into a static zip file to upload to GitHub Pages. Instead, the migration involves two stages: extracting your text and media from Wix while you still have Co-Owner access, and dropping them into a Markdown-based static site generator that publishes directly to GitHub Pages.

Here is the step-by-step workflow using **Quarto**, which is the cleanest, fastest tool for building Markdown websites on macOS (or you can use the **Greene Lab Website Template** if you want automated DOI citation lists—see the note at the bottom).

---

### Phase 1: Extract Your Content from Wix (Before It Expires)

Do not copy and paste directly from the live website into an editor if you want to save time— grab the raw assets from the Wix Media Manager first.

1. **Download All Lab Images at Once:**
* Log into Wix as a Co-Owner and open the **Wix Editor** (or go to your Dashboard $\rightarrow$ **Content Management / Media**).
* Open the **Media Manager** (the **Media** icon on the left sidebar of the editor).
* Select your uploaded lab photos, headshots, and research figures, click the **three dots (...)**, and select **Download**. Save these into a local folder on your computer (e.g., `~/Desktop/wix_backup/images/`).


2. **Copy Your Text Content into Markdown:**
* Open your live Wix site in a browser.
* Create a few temporary `.md` files (in Obsidian or VS Code) corresponding to your main navigation tabs: `index.md` (Home), `research.md`, `people.md`, `publications.md`, and `contact.md`.
* Copy the text from each Wix page and paste it as plain text (`Cmd + Shift + V`) into those files so you don't lose anything if the Wix subscription lapses.



---

### Phase 2: Set Up a Shared Lab GitHub Organization

To guarantee the lab is never locked out of its website again when someone leaves:

1. Go to [GitHub.com](https://github.com), click the **+** icon in the top-right corner, and select **New organization**.
2. Choose the **Free** plan. Name the organization after your lab (e.g., `frank-lab-cornell`).
3. Once created, go to the Organization's **People** tab $\rightarrow$ **Invite member**, and add your PI and another senior lab member as **Owners** (not just Members).
4. Inside this Organization, click **New Repository**:
* **Repository name:** `frank-lab-cornell.github.io` *(Naming the repository `<org-name>.github.io` gives you a clean root URL: `[https://frank-lab-cornell.github.io](https://frank-lab-cornell.github.io)`)*.
* **Visibility:** **Public** (required for free GitHub Pages hosting).
* Check **Add a README file** and click **Create repository**.



---

### Phase 3: Build the Local Site with Quarto

If you already work with Markdown or R/Python, Quarto lets you build a responsive website in minutes without touching HTML or CSS.

1. **Install Quarto (if not already installed):**
Open your macOS Terminal and install it via Homebrew or Conda/Mamba (or download the macOS `.pkg` installer from [quarto.org](https://quarto.org)):
```bash
brew install --cask quarto

```


2. **Clone Your Lab Repository & Scaffold the Website:**
Run the following in your Terminal (replace `frank-lab-cornell` with your actual GitHub Organization name):
```bash
cd ~/Documents
git clone https://github.com/frank-lab-cornell/frank-lab-cornell.github.io.git
cd frank-lab-cornell.github.io
quarto create project website .

```


3. **Create Your Pages & Move Your Images:**
* Create an `images/` folder inside the directory and move all the photos you downloaded from Wix into it.
* Create `.qmd` (Quarto Markdown) files for each of your pages:
```bash
touch research.qmd people.qmd publications.qmd contact.qmd

```




4. **Configure the Navigation Bar (`_quarto.yml`):**
Open the `_quarto.yml` file in your text editor and replace its contents with a clean lab layout:
```yaml
project:
  type: website
  output-dir: docs

website:
  title: "Frank Lab"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: research.qmd
        text: Research
      - href: people.qmd
        text: People
      - href: publications.qmd
        text: Publications
      - href: contact.qmd
        text: Contact

format:
  html:
    theme: cosmo
    css: styles.css
    toc: false

```


*(Note: Setting `output-dir: docs` tells Quarto to compile the finished HTML website directly into a `/docs` folder, which is the simplest way for GitHub Pages to serve it.)*
5. **Paste Your Wix Content & Preview:**
* Open `index.qmd`, `people.qmd`, etc., and paste in the text you saved from Wix.
* To embed images you downloaded from Wix, use standard Markdown syntax: `![](images/headshot.jpg){width=200px}`.
* To see a live preview in your browser that updates every time you save a file, run:
```bash
quarto preview

```





---

### Phase 4: Publish to GitHub Pages

1. **Render the Final HTML:**
In your terminal, stop the preview (`Ctrl + C`) and build the static site into the `docs/` folder:
```bash
quarto render

```


2. **Push to GitHub:**
```bash
git add .
git commit -m "Initial lab website migration from Wix"
git push origin main

```


3. **Turn On GitHub Pages:**
* Go to your repository on GitHub.com and click **Settings** (top tab) $\rightarrow$ **Pages** (left sidebar).
* Under **Build and deployment** $\rightarrow$ **Source**, keep **Deploy from a branch** selected.
* Under **Branch**, select **`main`**, change the folder dropdown next to it from `/ (root)` to **`/docs`**, and click **Save**.
* Wait about 60 seconds and refresh the page. Your live lab website URL will appear at the top of the settings page.



---

### Alternative Option: Automated Citations (Greene Lab Template)

If you don't want to format team member grids or publication lists manually in Quarto, check out the **[Greene Lab Website Template](https://github.com/greenelab/lab-website-template)** before you build:

* Instead of running `quarto create`, you simply click the green **"Use this template"** button directly on their GitHub repository page and copy it into your Lab GitHub Organization.
* It runs entirely in the cloud via GitHub Actions (no local installation required), provides pre-styled circular headshots for your `People` page via simple YAML files, and **automatically builds your `Publications` page just by typing a list of DOIs or PubMed IDs** into a text file.