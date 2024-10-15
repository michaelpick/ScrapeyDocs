import requests
from bs4 import BeautifulSoup
import html2text
import os
from urllib.parse import urljoin, urlparse
from datetime import datetime

def prompt_for_url():
    """Prompt the user to enter a URL to scrape."""
    url = input("Enter the URL of the documentation to scrape: ").strip()
    if not url.startswith("http"):
        url = "https://" + url
    return url

def scrape_page(url):
    """Scrape the content of a single page and convert it to markdown."""
    try:
        print(f"Scraping {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('article') or soup.find('main')  # Adjust as needed
        if not main_content:
            print(f"Warning: No main content found for {url}")
            return None
        h = html2text.HTML2Text()
        h.ignore_links = False
        markdown_content = h.handle(str(main_content))
        return markdown_content
    except requests.RequestException as e:
        print(f"Network error scraping {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error scraping {url}: {e}")
        return None

def save_as_markdown(content, filepath, metadata=None):
    """Save the content as a markdown file, creating directories as needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        if metadata:
            f.write(f"<!--\n{metadata}\n-->\n\n")
        f.write(content)
    print(f"Saved: {filepath}")

def should_scrape_link(url, base_url):
    """Filter out links that are not relevant, such as anchors or external links."""
    parsed_url = urlparse(url)
    if parsed_url.fragment or parsed_url.netloc != urlparse(base_url).netloc:
        return False
    if any(part in url.lower() for part in ['/version', '/0.', '/beta', 'history']):
        return False
    return True

def discover_links(base_url):
    """Discover all the internal links on the documentation site."""
    to_visit = {base_url}
    visited = set()
    while to_visit:
        url = to_visit.pop()
        visited.add(url)
        print(f"Discovering links on {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(base_url, link['href'])
                if full_url.startswith(base_url) and full_url not in visited:
                    if should_scrape_link(full_url, base_url):
                        to_visit.add(full_url)
        except requests.RequestException as e:
            print(f"Network error while discovering links on {url}: {e}")
        except Exception as e:
            print(f"Unexpected error while discovering links on {url}: {e}")
    return visited

def generate_toc(markdown_text):
    """Generate a Table of Contents based on the markdown headings."""
    lines = markdown_text.split('\n')
    toc = []
    for line in lines:
        if line.startswith('#'):
            level = line.count('#')
            title = line.lstrip('#').strip()
            anchor = title.lower().replace(' ', '-').replace('.', '')
            toc.append(f"{'  ' * (level - 1)}- [{title}](#{anchor})")
    return "\n".join(toc)

def combine_markdown_files(root_dir, output_dir, base_filename):
    """Combine all markdown files into a single file with a ToC."""
    combined_path = os.path.join(output_dir, f"{base_filename}.md")
    with open(combined_path, 'w', encoding='utf-8') as outfile:
        all_content = []
        for dirpath, _, filenames in os.walk(root_dir):
            filenames = sorted(filenames)
            for filename in filenames:
                if filename.endswith('.md'):
                    file_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(file_path, root_dir)
                    header = f"# {relative_path.replace('.md', '').replace(os.sep, ' > ')}\n\n"
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        all_content.append(header + infile.read() + "\n\n")
        combined_content = "\n".join(all_content)
        toc = generate_toc(combined_content)
        outfile.write("# Table of Contents\n\n" + toc + "\n\n" + combined_content)
    print(f"Combined markdown saved as {combined_path}")
    
    # Save a plain text version
    txt_output_path = os.path.join(output_dir, f"{base_filename}.txt")
    with open(txt_output_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(combined_content)
    print(f"Combined text saved as {txt_output_path}")

def main():
    base_url = prompt_for_url()
    parsed_url = urlparse(base_url)
    domain_name = parsed_url.netloc.replace('.', '_')
    output_dir = os.path.join(os.getcwd(), 'Outputs', domain_name)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Starting to process documentation from {base_url}")
    pages = discover_links(base_url)
    print(f"Found {len(pages)} pages to scrape.")
    
    for url in pages:
        content = scrape_page(url)
        if content:
            relative_path = url.replace(base_url, '').strip('/')
            filename = os.path.join(output_dir, relative_path + '.md')
            metadata = f"Original URL: {url}\nScraped on: {datetime.now().isoformat()}"
            save_as_markdown(content, filename, metadata)

    # Combine markdown files
    base_filename = domain_name + "_documentation"
    combine_markdown_files(output_dir, output_dir, base_filename)

if __name__ == '__main__':
    main()
