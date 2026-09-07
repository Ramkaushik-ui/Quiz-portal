import os

TEMPLATES_DIR = 'templates'

for filename in os.listdir(TEMPLATES_DIR):
    if filename.endswith('.html'):
        filepath = os.path.join(TEMPLATES_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            
        if "\\'" in content:
            # Replace the literal backslash followed by a single quote
            # with just a single quote.
            new_content = content.replace("\\'", "'")
            
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Fixed {filename}")
