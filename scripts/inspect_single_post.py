from bs4 import BeautifulSoup
import re

def inspect_post_structure():
    with open('dist/alternativas-gratuitas-asana/index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check title
    title = soup.title.string if soup.title else ""
    print(f"Title: {title}")
    
    # Check H1
    h1 = soup.find('h1')
    print(f"H1: {h1.text.strip() if h1 else 'None'}")
    
    # Check main article or content
    article = soup.find('article')
    print(f"Article tag found: {article is not None}")
    if article:
        print(f"Article class: {article.get('class')}")
        entry_content = article.find('div', class_='entry-content')
        if entry_content:
            print(f"entry-content found, text length: {len(entry_content.text.strip())}")
            # print headings in entry-content
            headings = [h.text.strip() for h in entry_content.find_all(['h2', 'h3', 'h4'])]
            print("Headings:", headings[:8])
            
    # Check meta tags
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    print(f"Meta Description: {meta_desc['content'] if meta_desc else 'None'}")
    
    # Check canonical
    canon = soup.find('link', rel='canonical')
    print(f"Canonical: {canon['href'] if canon else 'None'}")
    
    # Check header & navigation
    header = soup.find('header')
    print(f"Header tag found: {header is not None}")
    
    # Check footer
    footer = soup.find('footer')
    print(f"Footer tag found: {footer is not None}")

if __name__ == '__main__':
    inspect_post_structure()
