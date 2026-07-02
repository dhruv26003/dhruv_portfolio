from .models import Profile, SocialLink, Resume

def global_context(request):
    """
    Context processor to make Profile, Social Links, and Active Resume
    available globally in all templates.
    """
    profile = Profile.objects.first()
    social_links = SocialLink.objects.all()
    active_resume = Resume.objects.filter(is_active=True).first()
    
    return {
        "profile": profile,
        "social_links": social_links,
        "active_resume": active_resume,
    }
