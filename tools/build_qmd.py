import yaml, os, shutil, re, html, json

PAGES = {
    'index': 'Welcome to the Frank Lab',
    'about': 'About Us',
    'research': 'Research: Plant Grafting',
    'publications': 'Publications',
    'contact': 'Contact Us',
}

for page, title in PAGES.items():
    src = f'content/{page}.md'
    dst = f'{page}.qmd'
    with open(src, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Strip existing frontmatter if present
    fm_match = re.match(r'^---\n(.*?)\n---\n*(.*)', text, re.DOTALL)
    if fm_match:
        body = fm_match.group(2).strip()
    else:
        body = text.strip()
    
    # Remove leading `# Title` or `# Page Name` from body so Quarto doesn't duplicate <h1>
    body = re.sub(r'^#\s+[^\n]+\n*', '', body).strip()
    
    extra_fm = 'title-block-style: none\n' if page == 'index' else ''
    new_content = f'---\ntitle: "{title}"\n{extra_fm}---\n\n' + body + '\n'
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Prepared {dst} (title: '{title}')")

people = yaml.safe_load(open('content/people.yml'))

out = ['---', 'title: "Lab Members"', '---', '']
slides_data = json.load(open('content/slides_meta.json'))
slides_html = []
dots_html = []
for idx, (file, slug, eyebrow, title, pos) in enumerate(slides_data):
    active_cls = ' active' if idx == 0 else ''
    escaped_title = html.escape(title)
    escaped_eyebrow = html.escape(eyebrow)
    slides_html.append(f'''    <!-- Slide {idx+1} -->
    <div class="lab-slide{active_cls}" data-index="{idx}">
      <img src="images/groups/{slug}.jpg" class="lab-slide-img" style="object-position: {pos};" alt="{escaped_title}" />
      <div class="lab-slide-overlay">
        <div class="lab-slide-caption">
          <span class="lab-slide-subtitle">{escaped_eyebrow}</span>
          <span class="lab-slide-title">{escaped_title}</span>
        </div>
      </div>
    </div>''')
    dots_html.append(f'    <button class="lab-dot{active_cls}" data-index="{idx}" aria-label="Go to slide {idx+1}"></button>')

slides_joined = '\n'.join(slides_html)
dots_joined = '\n'.join(dots_html)
total_slides = len(slides_data)

SLIDESHOW_TEMPLATE = '''```{=html}
<div class="lab-slideshow-container" id="labSlideshow" aria-label="Frank Lab Group Photos Slideshow" role="region">
  <div class="lab-slide-badge" id="slideBadge">1 / __TOTAL__</div>

  <div class="lab-slideshow-track">
__SLIDES__
  </div>

  <!-- Navigation Arrows -->
  <button class="lab-slide-nav lab-slide-prev" id="prevSlide" aria-label="Previous slide">&#8249;</button>
  <button class="lab-slide-nav lab-slide-next" id="nextSlide" aria-label="Next slide">&#8250;</button>

  <!-- Pagination Dots -->
  <div class="lab-slide-dots" id="slideDots">
__DOTS__
  </div>
</div>

<script>
(function() {
  function initSlideshow() {
    const container = document.getElementById('labSlideshow');
    if (!container) return;

    const slides = container.querySelectorAll('.lab-slide');
    const dots = container.querySelectorAll('.lab-dot');
    const badge = document.getElementById('slideBadge');
    const prevBtn = document.getElementById('prevSlide');
    const nextBtn = document.getElementById('nextSlide');
    let current = 0;
    const total = slides.length;
    let timer = null;

    function goToSlide(n) {
      slides[current].classList.remove('active');
      dots[current].classList.remove('active');
      current = (n + total) % total;
      slides[current].classList.add('active');
      dots[current].classList.add('active');
      if (badge) badge.textContent = (current + 1) + ' / ' + total;
    }

    function nextSlide() { goToSlide(current + 1); }
    function prevSlide() { goToSlide(current - 1); }

    function startTimer() {
      stopTimer();
      timer = setInterval(nextSlide, 5000);
    }
    function stopTimer() {
      if (timer) clearInterval(timer);
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function(e) {
        e.preventDefault();
        prevSlide();
        startTimer();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function(e) {
        e.preventDefault();
        nextSlide();
        startTimer();
      });
    }

    dots.forEach(function(dot, idx) {
      dot.addEventListener('click', function(e) {
        e.preventDefault();
        goToSlide(idx);
        startTimer();
      });
    });

    container.addEventListener('mouseenter', stopTimer);
    container.addEventListener('mouseleave', startTimer);

    container.setAttribute('tabindex', '0');
    container.addEventListener('keydown', function(e) {
      if (e.key === 'ArrowLeft') {
        prevSlide();
        startTimer();
      } else if (e.key === 'ArrowRight') {
        nextSlide();
        startTimer();
      }
    });

    let touchStartX = 0;
    let touchEndX = 0;
    container.addEventListener('touchstart', function(e) {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    container.addEventListener('touchend', function(e) {
      touchEndX = e.changedTouches[0].screenX;
      if (touchStartX - touchEndX > 50) {
        nextSlide();
        startTimer();
      } else if (touchEndX - touchStartX > 50) {
        prevSlide();
        startTimer();
      }
    }, { passive: true });

    startTimer();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSlideshow);
  } else {
    initSlideshow();
  }
})();
</script>
```\n'''

out.append(SLIDESHOW_TEMPLATE.replace('__TOTAL__', str(total_slides)).replace('__SLIDES__', slides_joined).replace('__DOTS__', dots_joined))

PHOTO_POSITIONS = {
    'Dr. Margaret Frank': 'center 65%',
    'Michelle Heeney': 'center 25%',
    'Zachary Joseph Ruwitch': 'center 55%',
    'Weiwei Chen': '80% 70%',
    'Dr. Hannah Rae Thomas': 'center 35%',
    'Antone Jung': 'center 35%',
    'Xing Ma': 'center 35%',
    'Allie Hermanson': 'center 40%',
    'Emma Nam': 'center 40%',
    'Lucia Gore': 'center 45%',
    'Diego Hernandez': 'center 18%',
    'Juliane Scholtz': 'center 15%',
    'Jules Hart': 'center 35%',
}

def render_group(title, group_name):
    group_members = [p for p in people if p.get('group') == group_name]
    if not group_members:
        return
    out.append(f'## {title}\n')
    out.append('<div class="people-grid">\n')
    for p in group_members:
        photo = p.get('photo')
        if photo and os.path.exists(photo):
            pos = PHOTO_POSITIONS.get(p['name'])
            pos_style = f' style="object-position: {pos};"' if pos else ''
            img_html = f'<img src="{photo}" alt="{html.escape(p["name"])}" class="person-photo"{pos_style} />'
        else:
            initials = ''.join([part[0] for part in p["name"].split() if part[0].isalpha()][:2])
            img_html = f'<div class="person-photo-placeholder">{initials}</div>'
        
        bio_html = ""
        if p.get('bio'):
            bio_paras = []
            for b in p['bio']:
                b_html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', b)
                bio_paras.append(f'<p>{b_html}</p>')
            bio_html = f'<div class="person-bio">{"".join(bio_paras)}</div>'
        
        role_html = f'<p class="person-role">{html.escape(p.get("role", ""))}</p>' if p.get("role") else ''
        card = (
            f'<div class="person-card">\n'
            f'<div class="person-photo-wrapper">{img_html}</div>\n'
            f'<div class="person-details">\n'
            f'<h3 class="person-name">{html.escape(p["name"])}</h3>\n'
            f'{role_html}\n'
            f'{bio_html}\n'
            f'</div>\n'
            f'</div>\n'
        )
        out.append(card)
    out.append('</div>\n')

render_group("Current Lab Members", "current")
render_group("Alumni", "alumni")

with open('people.qmd', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')
print("Generated people.qmd successfully")
