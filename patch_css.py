import re

with open('static/css/style.css', 'r') as f:
    content = f.read()

# 1. Update root variables
root_vars = """:root {
  --navy: #f3faff;
  --navy-deep: #e6f6ff;
  --navy-panel: #ffffff;
  --blue: #1976d2;
  --blue-bright: #005dac;
  --cyan: #005dac;
  --cyan-soft: #414752;
  --cyan-wash: #021f29;
  --ink: #021f29;
  --muted: #717783;
  --danger: #ba1a1a;
  --ok: #005dac;
  --shadow: 0 1px 8px rgba(0, 0, 0, 0.12);
  --frame: 1px solid #cbe7f5;
  --font-display: "Inter", sans-serif;
  --font-body: "Inter", sans-serif;
  
  --sidebar-bg: #001945;
  --sidebar-text: #b0c6ff;
  --sidebar-text-hover: #ffffff;
  --sidebar-hover-bg: #1976d2;
  --btn-text: #ffffff;
}"""
content = re.sub(r':root\s*\{[^}]+\}', root_vars, content, count=1)

# 2. Update rgba colors to new primary (#005dac -> 0, 93, 172)
content = content.replace('rgba(8, 185, 208', 'rgba(0, 93, 172')
content = content.replace('rgba(8, 121, 184', 'rgba(25, 118, 210')
content = content.replace('rgba(155, 224, 232', 'rgba(203, 231, 245') # light border
content = content.replace('rgba(255, 93, 115', 'rgba(186, 26, 26')
content = content.replace('rgba(62, 224, 176', 'rgba(0, 93, 172')

# 3. Update specific components for dark sidebar
content = re.sub(r'\.side-nav\s*\{[^}]+\}', """.side-nav {
  background: var(--sidebar-bg);
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  padding: 20px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: sticky;
  top: 0;
  height: 100vh;
  color: var(--sidebar-text-hover);
}""", content)

content = re.sub(r'\.side-nav \.brand-mark span\s*\{[^}]+\}', "", content) # Will rely on specific rules

content = re.sub(r'\.nav-link\s*\{[^}]+\}', """.nav-link {
  color: var(--sidebar-text);
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-left: 3px solid transparent;
}""", content)

content = re.sub(r'\.nav-link:hover,\s*\.nav-link\.active\s*\{[^}]+\}', """.nav-link:hover,
.nav-link.active {
  color: var(--sidebar-text-hover);
  background: var(--sidebar-hover-bg);
  border-left-color: var(--sidebar-text-hover);
}""", content)

# 4. Auth brand
content = re.sub(r'\.auth-brand\s*\{[^}]+\}', """.auth-brand {
  padding: 48px 40px;
  background:
    linear-gradient(180deg, rgba(0, 93, 172, 0.16), transparent 42%),
    var(--sidebar-bg);
  border-right: 3px solid var(--cyan);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: var(--sidebar-text-hover);
}""", content)

content = re.sub(r'\.auth-brand p\s*\{[^}]+\}', """.auth-brand p {
  color: var(--sidebar-text);
  max-width: 36ch;
}""", content)

content = re.sub(r'\.brand-mark span\s*\{[^}]+\}', """.brand-mark span {
  display: block;
  color: var(--sidebar-text);
  font-size: 0.75rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}""", content)

content = re.sub(r'\.btn\s*\{[^}]+\}', """.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 0;
  cursor: pointer;
  padding: 12px 18px;
  font-family: var(--font-display);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--btn-text);
  background: var(--cyan);
  transition: transform 0.15s ease, background 0.15s ease;
}""", content)

# Write back
with open('static/css/style.css', 'w') as f:
    f.write(content)
