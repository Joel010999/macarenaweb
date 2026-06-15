import re
import os

def refactor_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Nav CSS
    nav_css_old = """.nav-links { display: flex; gap: 3rem; align-items: center; }"""
    nav_css_new = """.mobile-menu-btn { display: block; background: none; border: none; cursor: pointer; color: var(--pink1); }
        .nav-links { display: none; flex-direction: column; width: 100%; position: absolute; top: 100%; left: 0; background: var(--glass-bg); backdrop-filter: blur(20px); padding: 1rem 0; gap: 1rem; box-shadow: var(--glass-shadow); border-bottom: 1px solid var(--glass-border); }
        .nav-links.active { display: flex; }
        @media (min-width: 900px) {
            .mobile-menu-btn { display: none; }
            .nav-links { display: flex; flex-direction: row; position: static; width: auto; background: none; backdrop-filter: none; padding: 0; gap: 3rem; box-shadow: none; border: none; }
        }"""
    content = content.replace(nav_css_old, nav_css_new)
    
    # nav links text align center
    nav_a_old = """.nav-links a { text-decoration: none; color: var(--text); font-size: 0.75rem; letter-spacing: 2px; text-transform: uppercase; font-weight: normal; position: relative; padding-bottom: 5px; }"""
    nav_a_new = """.nav-links a { text-decoration: none; color: var(--text); font-size: 0.75rem; letter-spacing: 2px; text-transform: uppercase; font-weight: normal; position: relative; padding-bottom: 5px; text-align: center; }"""
    content = content.replace(nav_a_old, nav_a_new)

    # 2. About Grid (only index.html)
    about_old = """.about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; }"""
    about_new = """.about-grid { display: grid; grid-template-columns: 1fr; gap: 3rem; align-items: center; }
        @media (min-width: 900px) { .about-grid { grid-template-columns: 1fr 1fr; } }"""
    content = content.replace(about_old, about_new)

    # 3. Footer Grid
    footer_old = """.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }"""
    footer_new = """.footer-grid { display: grid; grid-template-columns: 1fr; gap: 2rem; margin-bottom: 2rem; }
        @media (min-width: 900px) { .footer-grid { grid-template-columns: 2fr 1fr 1fr; } }"""
    content = content.replace(footer_old, footer_new)

    # 4. Remove max-width: 900px blocks
    # index.html
    max_width_index = """        @media (max-width: 900px) {
            .about-grid, .footer-grid { grid-template-columns: 1fr; }
            .nav-links { display: none; }
            .collage { height: 400px; }
        }"""
    content = content.replace(max_width_index, "")
    
    # catalogo.html max-width
    max_width_cat = """@media (max-width: 900px) { .footer-grid { grid-template-columns: 1fr; } .nav-links { display: none; } }"""
    content = content.replace(max_width_cat, "")

    # 5. Masonry Grid (catalogo.html)
    masonry_old = """.masonry-grid { column-count: 4; column-gap: 1.5rem; }
        @media (max-width: 1200px) { .masonry-grid { column-count: 3; } }
        @media (max-width: 900px) { .masonry-grid { column-count: 2; } }
        @media (max-width: 600px) { .masonry-grid { column-count: 1; } }"""
    masonry_new = """.masonry-grid { column-count: 1; column-gap: 1.5rem; }
        @media (min-width: 600px) { .masonry-grid { column-count: 2; } }
        @media (min-width: 900px) { .masonry-grid { column-count: 3; } }
        @media (min-width: 1200px) { .masonry-grid { column-count: 4; } }"""
    content = content.replace(masonry_old, masonry_new)

    # 6. Adjust Navbar HTML
    nav_html_pattern = re.compile(r'<div class="container nav-content">(.*?)</div>\s*</nav>', re.DOTALL)
    
    def repl_nav(match):
        inner = match.group(1)
        # Check if catalogo or index links
        if 'href="catalogo.html"' in inner and 'href="#inicio"' in inner:
            links = """<a href="#inicio">Inicio</a>
                <a href="#nosotros">La Marca</a>
                <a href="#servicios">Servicios</a>
                <a href="catalogo.html">Catálogo Online</a>"""
        else:
            links = """<a href="index.html">Inicio</a>
                <a href="index.html#nosotros">La Marca</a>
                <a href="index.html#servicios">Servicios</a>
                <a href="catalogo.html" style="color: var(--pink1);">Catálogo Online</a>"""
                
        new_nav = f"""
        <div class="container nav-content" style="flex-wrap: wrap; position: relative;">
            <a href="index.html" class="logo">
                <img src="./Logo/PNG transparente/Recurso 24@2x.png" alt="Male Style Logo">
            </a>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <a href="https://wa.me/5493585706305" class="btn btn-primary btn-sm btn-consultar">Consultar Ahora</a>
                <button class="mobile-menu-btn" id="mobile-menu-btn">
                    <i data-lucide="menu"></i>
                </button>
            </div>
            <div class="nav-links" id="nav-links">
                {links}
            </div>
        </div>
    </nav>"""
        return new_nav.strip()

    content = re.sub(r'<div class="container nav-content">(.*?)</nav>', repl_nav, content, flags=re.DOTALL)

    # 7. Add mobile menu JS
    js_addition = """
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const navLinks = document.getElementById('nav-links');
        if(mobileMenuBtn && navLinks) {
            mobileMenuBtn.addEventListener('click', () => {
                navLinks.classList.toggle('active');
            });
            navLinks.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => {
                    navLinks.classList.remove('active');
                });
            });
        }
"""
    # Insert before lucide.createIcons(); if possible, or before </body>
    if 'lucide.createIcons();' in content:
        content = content.replace('lucide.createIcons();', js_addition + '\n        lucide.createIcons();', 1)
    else:
        content = content.replace('</body>', js_addition + '\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Refactored {filepath}")

refactor_html('c:/Renderbyte/Maca/index.html')
refactor_html('c:/Renderbyte/Maca/catalogo.html')
