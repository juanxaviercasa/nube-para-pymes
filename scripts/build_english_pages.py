"""
Script to build:
1. en/tools/index.html (Tools Portal in English)
2. en/index.html (English Homepage matching main site design)
3. en/about-us/index.html (English About Us page)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def build_english_tools_portal():
    print("Building en/tools/index.html...")
    src_portal = ROOT / "dist" / "herramientas" / "index.html"
    dest_dir = ROOT / "en" / "tools"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "index.html"

    if not src_portal.exists():
        src_portal = ROOT / "index.html"

    if src_portal.exists():
        txt = src_portal.read_text(encoding="utf-8")
        txt = txt.replace('href="../assets/', 'href="/assets/')
        txt = txt.replace('src="../assets/', 'src="/assets/')
        txt = txt.replace('src="../js/', 'src="/herramientas/js/')
        txt = txt.replace('href="../css/', 'href="/css/')
        txt = txt.replace('href="../index.html"', 'href="/herramientas/"')
        txt = txt.replace('href="/"', 'href="/en/"')
        txt = re.sub(r'<script[^>]*geo-lang-detect[^>]*></script>', '', txt)
        dest_file.write_text(txt, encoding="utf-8")
        print("en/tools/index.html built.")

def build_english_about_us():
    print("Building en/about-us/index.html...")
    src_about = ROOT / "dist" / "sobre-nosotros" / "index.html"
    dest_dir = ROOT / "en" / "about-us"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "index.html"

    if not src_about.exists():
        print("Warning: dist/sobre-nosotros/index.html not found.")
        return

    txt = src_about.read_text(encoding="utf-8")
    
    # Update lang and canonical
    txt = txt.replace('<html lang="es"', '<html lang="en"')
    txt = re.sub(r'<title>.*?</title>', '<title>About Us: Digital Infrastructure Experts | SMB Cloud</title>', txt)
    txt = re.sub(r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>', '<meta name="description" content="Meet SMB Cloud (Nube para Pymes). We help small businesses make informed software decisions through objective reviews, benchmarks, and free web tools." />', txt)
    txt = re.sub(r'<link\s+rel=["\']canonical["\']\s+href=["\'].*?["\']\s*/?>', '<link rel="canonical" href="https://nubeparapymes.online/en/about-us/" />', txt)

    # Translations of headings and content
    txt = txt.replace('No somos un blog de consejos. Somos tu Motor de Infraestructura Digital.', 'We are not just a tips blog. We are your Digital Infrastructure Engine.')
    txt = txt.replace('NubeParaPymes nació para resolver un problema crítico en el sector B2B: la falta de datos empíricos en la elección de software. Nuestra misión es proporcionar a las empresas la arquitectura tecnológica necesaria para automatizar sus flujos de trabajo y maximizar la eficiencia operativa.', 'SMB Cloud was born to solve a critical problem in the business sector: the lack of empirical data when choosing software. Our mission is to provide companies with the technical architecture needed to automate workflows and maximize operational efficiency.')
    txt = txt.replace('NubeParaPymes naci&oacute; para resolver un problema cr&iacute;tico en el sector B2B: la falta de datos emp&iacute;ricos en la elecci&oacute;n de software. Nuestra misi&oacute;n es proporcionar a las empresas la arquitectura tecnol&oacute;gica necesaria para automatizar sus flujos de trabajo y maximizar la eficiencia operativa.', 'SMB Cloud was born to solve a critical problem in the business sector: the lack of empirical data when choosing software. Our mission is to provide companies with the technical architecture needed to automate workflows and maximize operational efficiency.')
    txt = txt.replace('Decisiones basadas en Arquitectura, no en Opiniones', 'Decisions Based on Architecture, Not Opinions')
    txt = txt.replace('Analizamos el software desde una perspectiva de ingeniería y negocio. Evaluamos la capacidad de integración, la escalabilidad y la robustez de cada herramienta. Ayudamos a los dueños de Pymes y directores de operaciones a elegir el stack tecnológico exacto para escalar sin fricciones técnicas.', 'We evaluate software from an engineering and business perspective. We assess integration capabilities, scalability, and robustness for every tool. We help SMB owners and operations leaders choose the exact tech stack to scale without technical friction.')
    txt = txt.replace('Analizamos el software desde una perspectiva de ingenier&iacute;a y negocio. Evaluamos la capacidad de integraci&oacute;n, la escalabilidad y la robustez de cada herramienta. Ayudamos a los due&ntilde;os de Pymes y directores de operaciones a elegir el stack tecnol&oacute;gico exacto para escalar sin fricciones t&eacute;cnicas.', 'We evaluate software from an engineering and business perspective. We assess integration capabilities, scalability, and robustness for every tool. We help SMB owners and operations leaders choose the exact tech stack to scale without technical friction.')
    txt = txt.replace('Política de Transparencia Radical', 'Radical Transparency Policy')
    txt = txt.replace('Pol&iacute;tica de Transparencia Radical', 'Radical Transparency Policy')
    txt = txt.replace('Nuestro modelo de monetización es simple y ético. Nunca cobramos a los proveedores de software por posicionamiento ni reseñas favorables.', 'Our monetization model is simple and ethical. We never charge software vendors for rankings or favorable reviews.')
    txt = txt.replace('Nuestro modelo de monetizaci&oacute;n es simple y &eacute;tico. Nunca cobramos a los proveedores de software por posicionamiento ni rese&ntilde;as favorables.', 'Our monetization model is simple and ethical. We never charge software vendors for rankings or favorable reviews.')
    txt = txt.replace('El Equipo Fundador', 'The Founder')
    txt = txt.replace('Juan Xavier Cabello Salirrosas', 'Juan Xavier Cabello')
    txt = txt.replace('Fundador & Director de Tecnología', 'Founder & Chief Technology Officer')
    txt = txt.replace('Fundador & Director de Tecnolog&iacute;a', 'Founder & Chief Technology Officer')
    txt = txt.replace('Sobre Nosotros', 'About Us')

    # Nav
    txt = txt.replace('>Herramientas Gratis<', '>Free Tools<')
    txt = txt.replace('>Sobre Nosotros<', '>About Us<')
    txt = txt.replace('>Categorías<', '>Categories<')
    txt = txt.replace('>Categor&iacute;as<', '>Categories<')
    txt = txt.replace('href="/herramientas/"', 'href="/en/tools/"')
    txt = txt.replace('href="/sobre-nosotros/"', 'href="/en/about-us/"')
    txt = txt.replace('href="/"', 'href="/en/"')

    dest_file.write_text(txt, encoding="utf-8")
    print("en/about-us/index.html built.")

def build_english_homepage():
    try:
        from build_english_homepage_flawless import build_perfect_english_homepage
        build_perfect_english_homepage()
    except Exception as e:
        print(f"Error building English homepage: {e}")

if __name__ == "__main__":
    build_english_tools_portal()
    build_english_about_us()
    build_english_homepage()
