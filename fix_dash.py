f = open('frontend/pages/dashboard.html', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace('<a href="study.html" class="btn btn-outline">Study</a><button onclick="logout()"',
                          '<a href="study.html" class="btn btn-outline">Study</a><a href="upgrade.html" class="btn btn-outline" style="color:#ff9800;border-color:#ff9800">Upgrade</a><button onclick="logout()"')
f = open('frontend/pages/dashboard.html', 'w', encoding='utf-8')
f.write(content)
f.close()
print('Upgrade added!')
