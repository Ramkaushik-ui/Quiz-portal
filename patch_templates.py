import os
import re

TEMPLATES_DIR = 'templates'

def patch_links(content):
    # Static files
    content = re.sub(r'href="css/style\.css"', r'href="{{ url_for(\'static\', filename=\'css/style.css\') }}"', content)
    content = re.sub(r'src="js/app\.js"', r'src="{{ url_for(\'static\', filename=\'js/app.js\') }}"', content)
    content = re.sub(r'src="assets/(.*?)"', r'src="{{ url_for(\'static\', filename=\'assets/\1\') }}"', content)

    # Student routes
    content = content.replace('href="dashboardstudent.html"', 'href="{{ url_for(\'student_dashboard\') }}"')
    content = content.replace('href="teamstudent.html"', 'href="{{ url_for(\'student_team\') }}"')
    content = content.replace('href="eventstudent.html"', 'href="{{ url_for(\'student_event\') }}"')
    content = content.replace('href="arenastudent.html"', 'href="{{ url_for(\'student_arena\') }}"')
    content = content.replace('href="leaderboardstudent.html"', 'href="{{ url_for(\'student_leaderboard\') }}"')
    content = content.replace('href="profilestudent.html"', 'href="{{ url_for(\'student_profile\') }}"')
    content = content.replace('href="registerstudent.html"', 'href="{{ url_for(\'student_register\') }}"')
    content = content.replace('href="indexstudent.html"', 'href="{{ url_for(\'student_index\') }}"')
    
    # Generic or admin routes
    content = content.replace('href="dashboard.html"', 'href="{{ url_for(\'dashboard\') }}"')
    content = content.replace('href="question.html"', 'href="{{ url_for(\'questions\') }}"')
    content = content.replace('href="team.html"', 'href="{{ url_for(\'teams\') }}"')
    content = content.replace('href="submission.html"', 'href="{{ url_for(\'submissions\') }}"')
    content = content.replace('href="login.html"', 'href="{{ url_for(\'login\') }}"')

    # Remove direct .html refs that might be left (like in arena.html -> arena)
    content = re.sub(r'href="(team|event|arena|leaderboard|profile)\.html"', r'href="{{ url_for(\'student_\1\') }}"', content)
    
    return content

for filename in os.listdir(TEMPLATES_DIR):
    if filename.endswith('.html'):
        filepath = os.path.join(TEMPLATES_DIR, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            
        content = patch_links(content)
        
        with open(filepath, 'w') as f:
            f.write(content)
