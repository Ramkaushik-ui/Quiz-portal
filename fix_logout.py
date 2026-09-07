import os
import re

TEMPLATES_DIR = 'templates'

for filename in os.listdir(TEMPLATES_DIR):
    if filename.endswith('.html'):
        filepath = os.path.join(TEMPLATES_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Replace logout links pointing to login with logout
        if 'class="logout-link"' in content and "url_for('login')" in content:
            # We specifically target the logout links
            content = re.sub(r'href="\{\{ url_for\(\'login\'\) \}\}" class="logout-link"', r'href="{{ url_for(\'logout\') }}" class="logout-link"', content)
            
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Fixed logout link in {filename}")
