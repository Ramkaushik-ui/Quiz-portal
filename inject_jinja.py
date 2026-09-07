import re

def inject_jinja(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # In dashboardstudent.html, replace the hardcoded leaderboard rows with a Jinja loop
    if 'dashboardstudent.html' in filepath:
        # Find the leaderboard preview section
        start_marker = "<!-- LEADERBOARD PREVIEW -->"
        end_marker = "</main>"
        
        if start_marker in content and end_marker in content:
            before, rest = content.split(start_marker, 1)
            middle, after = rest.split(end_marker, 1)
            
            # The middle contains the section. We will replace all .lb-row divs with a jinja loop.
            new_middle = re.sub(
                r'<div class="lb-row.*?</section>',
                r'''{% for t in teams %}
      <div class="lb-row {% if t.id == team.id %}current{% endif %}">
        <span class="rank-badge">{{ loop.index }}</span>
        <div class="lb-team">
          <strong>{{ t.team_name }}</strong>
          <span>{% if t.id == team.id %}Your team{% else %}Participant{% endif %}</span>
        </div>
        <strong class="lb-score">{{ t.score }}</strong>
      </div>
      {% endfor %}
    </section>''',
                middle,
                flags=re.DOTALL
            )
            content = before + start_marker + new_middle + end_marker + after
            
    with open(filepath, 'w') as f:
        f.write(content)

inject_jinja('templates/dashboardstudent.html')
