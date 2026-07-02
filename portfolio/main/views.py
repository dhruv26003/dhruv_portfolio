from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from .models import (
    Profile,
    Category,
    Education,
    Experience,
    Skill,
    Project,
    Certificate,
    Service,
    ContactMessage,
)
from .forms import ContactForm

def home_view(request):
    # Visitor counter (once per session)
    if not request.session.get("has_visited", False):
        profile = Profile.objects.first()
        if profile:
            profile.visitor_count += 1
            profile.save(update_fields=["visitor_count"])
        request.session["has_visited"] = True
        
    # Handle Contact Form submission
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_msg = "Thank you! Your message has been sent successfully. I will get back to you soon."
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True, "message": success_msg})
            messages.success(request, success_msg)
            return redirect("home")
        else:
            errors = form.errors.as_json()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": form.errors, "message": "Please correct the errors below."})
            messages.error(request, "Failed to send message. Please correct the errors.")
    else:
        form = ContactForm()

    # Query Data
    experiences = Experience.objects.prefetch_related("skills_used").all()
    education_history = Education.objects.all()
    
    # Fetch categories and group skills/projects
    categories = Category.objects.all()
    skills = Skill.objects.select_related("category").all()
    projects = Project.objects.select_related("category").all()
    certificates = Certificate.objects.all()
    services = Service.objects.all()

    # Quick Facts parsing from profile (e.g. key-value split by line)
    profile = Profile.objects.first()
    parsed_facts = []
    if profile and profile.quick_facts:
        for line in profile.quick_facts.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                parsed_facts.append({"key": key.strip(), "value": val.strip()})
            elif line.strip():
                parsed_facts.append({"key": None, "value": line.strip()})

    context = {
        "experiences": experiences,
        "education_history": education_history,
        "categories": categories,
        "skills": skills,
        "projects": projects,
        "certificates": certificates,
        "services": services,
        "contact_form": form,
        "parsed_facts": parsed_facts,
    }
    return render(request, "main/home.html", context)


def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    # Get related projects (same category, excluding current)
    related_projects = Project.objects.filter(category=project.category).exclude(id=project.id)[:3]
    
    context = {
        "project": project,
        "related_projects": related_projects,
    }
    return render(request, "main/project_detail.html", context)


def sitemap_view(request):
    """
    Dynamically generates sitemap.xml for SEO indexing.
    """
    domain = request.build_absolute_uri('/')[:-1]
    projects = Project.objects.all()
    
    # We will pass the URLs and last mod dates
    urls = [
        {"location": f"{domain}/", "priority": "1.0", "changefreq": "daily"},
    ]
    for project in projects:
        urls.append({
            "location": f"{domain}/project/{project.slug}/",
            "priority": "0.8",
            "changefreq": "weekly"
        })
        
    context = {"urls": urls}
    xml_content = render(request, "sitemap.xml", context)
    return HttpResponse(xml_content, content_type="application/xml")


def robots_txt_view(request):
    """
    Returns standard robots.txt.
    """
    domain = request.build_absolute_uri('/')[:-1]
    content = f"User-agent: *\nAllow: /\nSitemap: {domain}/sitemap.xml\n"
    return HttpResponse(content, content_type="text/plain")


def custom_404_view(request, exception=None):
    """
    Custom 404 handler.
    """
    response = render(request, "main/404.html", status=404)
    return response
