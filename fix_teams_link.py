import os
import glob

for filepath in glob.glob('templates/*student.html'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We only want to replace the wrong 'teams' route with 'student_team'
    if "url_for('teams')" in content:
        content = content.replace("url_for('teams')", "url_for('student_team')")
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed teams link in {filepath}")
