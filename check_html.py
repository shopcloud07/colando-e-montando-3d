content = open('index.html', 'r', encoding='utf-8').read()
print('CSS links:', content.count('rel="stylesheet"'))
print('</head> found:', '</head>' in content)
print('<style> blocks:', content.count('<style'))
print('<body tag:', '<body' in content)
print('</body>:', '</body>' in content)
# Check if any unclosed script tags
import re
scripts_open = len(re.findall(r'<script', content))
scripts_close = len(re.findall(r'</script>', content))
print('Script open tags:', scripts_open)
print('Script close tags:', scripts_close)
