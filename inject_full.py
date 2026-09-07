import os
import re

def process_file(filepath, replacements):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        modified = False
        for search_pattern, replacement in replacements:
            if re.search(search_pattern, content, flags=re.DOTALL):
                content = re.sub(search_pattern, replacement, content, flags=re.DOTALL)
                modified = True
                
        if modified:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Patched {filepath}")
    except FileNotFoundError:
        pass

# 1. Update login.html to actually use POST to the right endpoints and have names on inputs
login_replacements = [
    (r'<form\s*onsubmit="return false;"\s*>\s*<div class="field">\s*<input\s*type="email"\s*id="loginEmail"',
     r'<form action="{{ url_for(\'login\') }}" method="POST">\n      <div class="field">\n        <input name="loginEmail" type="email" id="loginEmail"'),
    (r'<input\s*type="password"\s*id="loginPassword"',
     r'<input name="loginPassword" type="password" id="loginPassword"'),
    (r'<div\s*id="signupForm".*?<form\s*onsubmit="return false;"\s*>\s*<div class="field">\s*<input\s*type="text"\s*id="signupName"',
     r'<div id="signupForm" class="hidden">\n    <h1>Create Account</h1>\n    <form action="{{ url_for(\'signup\') }}" method="POST">\n      <div class="field">\n        <input name="signupName" type="text" id="signupName"'),
    (r'<input\s*type="email"\s*id="signupEmail"',
     r'<input name="signupEmail" type="email" id="signupEmail"'),
    (r'<input\s*type="password"\s*id="signupPassword"',
     r'<input name="signupPassword" type="password" id="signupPassword"'),
    (r'<input\s*type="password"\s*id="signupConfirm"',
     r'<input name="signupConfirm" type="password" id="signupConfirm"')
]
process_file('templates/login.html', login_replacements)

# 2. Update question.html (Admin)
question_replacements = [
    (r'<tbody class="font-body-md text-body-md text-on-surface">.*?</tbody>',
     r'''<tbody class="font-body-md text-body-md text-on-surface">
{% for q in questions %}
<tr class="hover:bg-surface-container-low/60 transition-colors border-b border-surface-variant">
<td class="py-space-sm px-space-md text-center font-telemetry-mono text-on-surface-variant">{{ loop.index }}</td>
<td class="py-space-sm px-space-md"><span class="font-title text-title text-on-surface font-semibold hover:text-primary cursor-pointer">{{ q.question_text }}</span></td>
<td class="py-space-sm px-space-md"><span class="inline-flex items-center px-2 py-0.5 rounded-full {% if q.type == 'MCQ' %}bg-primary-fixed text-primary{% else %}bg-secondary-container/20 text-secondary{% endif %} font-label-sm font-semibold">{{ q.type }}</span></td>
<td class="py-space-sm px-space-md text-right font-telemetry-mono font-bold text-on-surface">{{ q.points }} pts</td>
<td class="py-space-sm px-space-md text-center"><span class="inline-flex items-center px-2.5 py-1 rounded-full bg-surface-container-high text-on-surface-variant font-label-sm">Active</span></td>
<td class="py-space-sm px-space-md text-center">
<div class="flex items-center justify-center gap-1">
<button class="p-1.5 rounded-lg hover:bg-surface-container text-on-surface-variant hover:text-primary transition-colors" title="Edit" type="button"><span class="material-symbols-outlined text-lg">edit</span></button>
<button class="delete-trigger p-1.5 rounded-lg hover:bg-error-container text-on-surface-variant hover:text-error transition-colors" data-question-num="{{ loop.index }}" data-question-title="{{ q.question_text }}" title="Delete" type="button"><span class="material-symbols-outlined text-lg">delete</span></button>
</div>
</td>
</tr>
{% endfor %}
</tbody>''')
]
process_file('templates/question.html', question_replacements)

# 3. Update team.html (Admin)
team_replacements = [
    (r'<tbody class="font-body-md text-body-md text-on-surface divide-y divide-surface-variant">.*?</tbody>',
     r'''<tbody class="font-body-md text-body-md text-on-surface divide-y divide-surface-variant">
{% for t in teams %}
<tr class="hover:bg-surface-container-low transition-colors">
<td class="px-space-md py-space-sm"><div class="flex items-center gap-space-sm"><div class="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center font-title text-title font-bold text-primary">{{ t.team_name[:2].upper() }}</div><div class="flex flex-col"><span class="font-title text-body-md text-on-surface font-semibold">{{ t.team_name }}</span></div></div></td>
<td class="px-space-md py-space-sm"><span class="font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-surface-container-high text-on-surface-variant">Active</span></td>
<td class="px-space-md py-space-sm text-center"><span class="font-telemetry-mono font-bold text-on-surface">{{ t.score }}</span></td>
<td class="px-space-md py-space-sm text-center"><span class="inline-flex items-center px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-telemetry-mono font-bold">Q4</span></td>
<td class="px-space-md py-space-sm text-right"><div class="flex items-center justify-end gap-1"><button class="p-1.5 rounded-lg hover:bg-surface-container text-on-surface-variant hover:text-primary transition-colors" title="View Details"><span class="material-symbols-outlined text-lg">visibility</span></button></div></td>
</tr>
{% endfor %}
</tbody>''')
]
process_file('templates/team.html', team_replacements)

# 4. Update submission.html (Admin)
submission_replacements = [
    (r'<tbody class="font-body-md text-body-md text-on-surface divide-y divide-surface-variant">.*?</tbody>',
     r'''<tbody class="font-body-md text-body-md text-on-surface divide-y divide-surface-variant">
{% for sub in submissions %}
<tr class="hover:bg-surface-container-low transition-colors">
<td class="px-space-md py-space-sm font-telemetry-mono text-outline">#{{ sub.id }}</td>
<td class="px-space-md py-space-sm"><span class="font-telemetry-mono text-on-surface-variant">Now</span></td>
<td class="px-space-md py-space-sm"><span class="font-title text-body-md text-on-surface font-semibold">{{ sub.team.team_name if sub.team else "Unknown" }}</span></td>
<td class="px-space-md py-space-sm"><span class="font-telemetry-mono text-label-md font-bold px-2 py-0.5 rounded bg-surface-container text-primary">Q{{ sub.question_id }}</span></td>
<td class="px-space-md py-space-sm"><span class="font-telemetry-mono text-on-surface font-semibold">{{ sub.submitted_option }}</span></td>
<td class="px-space-md py-space-sm text-center">
{% if sub.is_correct %}
<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-primary-container/20 text-primary font-label-sm font-bold"><span class="material-symbols-outlined text-sm">check_circle</span> Correct</span>
{% else %}
<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-error-container/50 text-on-error-container font-label-sm font-bold"><span class="material-symbols-outlined text-sm">cancel</span> Incorrect</span>
{% endif %}
</td>
</tr>
{% endfor %}
</tbody>''')
]
process_file('templates/submission.html', submission_replacements)

# 5. Update dashboard.html (Admin)
dashboard_replacements = [
    (r'<tbody class="font-body-md text-body-md text-on-surface divide-y-0">.*?</tbody>',
     r'''<tbody class="font-body-md text-body-md text-on-surface divide-y-0">
{% for t in teams[:5] %}
<tr class="hover:bg-surface-container-low transition-colors h-12 border-b border-surface-container">
<td class="px-space-sm py-space-xs font-telemetry-mono text-primary font-bold">#{{ loop.index }}</td>
<td class="px-space-sm py-space-xs"><span class="font-title text-body-md font-semibold text-on-surface">{{ t.team_name }}</span></td>
<td class="px-space-sm py-space-xs"><span class="font-telemetry-mono text-label-md font-bold px-2 py-0.5 rounded bg-surface-container text-primary">Q4</span></td>
<td class="px-space-sm py-space-xs text-right font-telemetry-mono font-bold text-on-surface">{{ t.score }} pts</td>
<td class="px-space-sm py-space-xs text-center"><span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-surface-container-high text-primary font-label-sm font-semibold"><span class="w-1.5 h-1.5 rounded-full bg-primary"></span>Active</span></td>
</tr>
{% endfor %}
</tbody>'''),
    (r'<div class="space-y-space-xs">.*?</div></div><a',
     r'''<div class="space-y-space-xs">
{% for sub in submissions %}
<div class="p-space-sm rounded-lg bg-surface-container-low flex items-center justify-between gap-space-xs">
<div class="min-w-0">
<div class="flex items-center gap-1.5"><span class="font-title text-body-md text-on-surface font-semibold truncate">{{ sub.team.team_name if sub.team else "Unknown" }}</span><span class="font-label-sm text-label-sm px-1.5 py-0.5 rounded bg-surface-container text-primary font-bold">Q{{ sub.question_id }}</span></div>
<p class="font-body-sm text-body-sm text-on-surface-variant truncate mt-0.5">Answer: <span class="font-telemetry-mono text-on-surface font-semibold">"{{ sub.submitted_option }}"</span></p>
</div>
<div class="text-right flex-shrink-0">
{% if sub.is_correct %}
<span class="font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-surface-container-high text-primary font-bold block">Correct</span>
{% else %}
<span class="font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-error-container text-on-error-container font-bold block">Incorrect</span>
{% endif %}
<span class="font-label-sm text-label-sm text-outline mt-0.5 block font-telemetry-mono">Just now</span>
</div>
</div>
{% endfor %}
</div></div><a''')
]
process_file('templates/dashboard.html', dashboard_replacements)

# 6. Update arenastudent.html
arenastudent_replacements = [
    (r'<div class="q-rail">.*?</div>\s*<!-- STAGE -->',
     r'''<div class="q-rail">
{% for q in questions %}
<button class="q-node {% if loop.first %}current{% endif %}">{{ loop.index }}</button>
{% endfor %}
</div>
<!-- STAGE -->'''),
    (r'<div class="question-stage">.*?</div>\s*<!-- SIDE METER -->',
     r'''<div class="question-stage">
{% if questions %}
<div class="q-meta"><span>ROUND 02</span><span>10 PTS</span></div>
<h2>{{ questions[0].question_text }}</h2>
<p class="prompt">Select the correct option</p>
<div class="options">
<div class="option selected"><div class="key">A</div><span>{{ questions[0].option_a }}</span></div>
<div class="option"><div class="key">B</div><span>{{ questions[0].option_b }}</span></div>
<div class="option"><div class="key">C</div><span>{{ questions[0].option_c }}</span></div>
<div class="option"><div class="key">D</div><span>{{ questions[0].option_d }}</span></div>
</div>
<div class="arena-actions">
<div class="feedback" id="feedback"></div>
<button class="btn btn-arena" onclick="document.getElementById('feedback').innerText='Submitted!';">Submit Answer -></button>
</div>
{% else %}
<h2>No questions available</h2>
{% endif %}
</div>
<!-- SIDE METER -->''')
]
process_file('templates/arenastudent.html', arenastudent_replacements)

# 7. Update User Profile Name logic in dashboardstudent.html & teamstudent.html & sidebar
sidebar_replacements = [
    (r'<strong>Harini G</strong>', r'<strong>{{ user.get("fullname", "Student") }}</strong>'),
    (r'Welcome back, Harini\.', r'Welcome back, {{ user.get("fullname", "Student") }}.')
]
process_file('templates/dashboardstudent.html', sidebar_replacements)
process_file('templates/teamstudent.html', sidebar_replacements)
process_file('templates/profilestudent.html', sidebar_replacements)
process_file('templates/arenastudent.html', sidebar_replacements)
process_file('templates/eventstudent.html', sidebar_replacements)
process_file('templates/leaderboardstudent.html', sidebar_replacements)

