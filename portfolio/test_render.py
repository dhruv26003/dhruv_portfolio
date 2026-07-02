import os
import django
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.template.loader import render_to_string
from main.models import Profile, Category

def test():
    try:
        # Check if database is populated
        profile_count = Profile.objects.count()
        category_count = Category.objects.count()
        
        log = []
        log.append(f"Database stats: Profile count = {profile_count}, Category count = {category_count}")
        
        context = {
            "experiences": [],
            "education_history": [],
            "categories": [],
            "skills": [],
            "projects": [],
            "certificates": [],
            "services": [],
            "parsed_facts": [],
        }
        
        rendered = render_to_string('main/home.html', context)
        log.append("Template rendered successfully.")
        
        # Check if the literal brackets are in the output
        if "{{" in rendered:
            log.append("WARNING: Found literal double curly braces '{{' in the rendered HTML output!")
            # Find lines containing double curly braces
            lines = rendered.splitlines()
            for i, line in enumerate(lines):
                if "{{" in line:
                    log.append(f"Line {i}: {line.strip()}")
        else:
            log.append("No literal double curly braces found in rendered output.")
            
        with open('render_output.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(log))
            
    except Exception as e:
        with open('render_output.txt', 'w', encoding='utf-8') as f:
            f.write(f"EXCEPTION ENCOUNTERED: {str(e)}")

if __name__ == '__main__':
    test()
