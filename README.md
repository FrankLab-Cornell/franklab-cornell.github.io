# Frank Lab Website • Cornell University

Official website for the **Frank Lab** in the School of Integrative Plant Science (SIPS) at Cornell University, investigating the molecular mechanisms of plant grafting, mobile signaling, and graft junction formation.

🌐 **Live Website:** [https://franklab-cornell.github.io/](https://franklab-cornell.github.io/)

---

## Website Editing & Maintenance

For complete instructions on editing pages, adding new lab members, updating publications, and managing GitHub collaborators, please see:

📖 **[INSTRUCTIONS.md](INSTRUCTIONS.md)**

### Quick Commands

```bash
# 1. Rebuild pages and compile the website into docs/
python3 tools/build_qmd.py && quarto render

# 2. Preview locally in your browser
quarto preview

# 3. Deploy changes live to GitHub Pages
git add .
git commit -m "Update website content"
git push origin main
```
