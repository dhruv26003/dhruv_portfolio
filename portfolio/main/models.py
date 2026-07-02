from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, help_text="e.g., Python Automation Engineer & Django Developer")
    bio = models.TextField(help_text="Short introductory bio for hero section")
    summary = models.TextField(help_text="Detailed professional summary for About section")
    profile_photo = models.ImageField(upload_to="profile/", blank=True, null=True, help_text="Hero section image")
    about_photo = models.ImageField(upload_to="profile/", blank=True, null=True, help_text="About section image")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=150, help_text="e.g., Gujarat, India")
    github_username = models.CharField(max_length=100, blank=True, help_text="Used to show custom GitHub profile information")
    visitor_count = models.IntegerField(default=0, help_text="Tracks total views on the portfolio")
    quick_facts = models.TextField(blank=True, help_text="Key-value style or points, one per line. E.g. 'Completed Projects: 30+' or 'Automation scripts: 150+'")
    
    # SEO Meta Tags
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO Title Tag")
    meta_description = models.TextField(blank=True, help_text="SEO Meta Description")
    meta_keywords = models.CharField(max_length=500, blank=True, help_text="SEO Meta Keywords (comma-separated)")
    
    def __str__(self):
        return self.name


class Resume(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="resumes/")
    is_active = models.BooleanField(default=True, help_text="If checked, this resume will be the active copy downloadable on the site.")
    uploaded_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Set all other Resumes to inactive
            Resume.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.title} (Active: {self.is_active})"


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False, verbose_name="Currently studying here")
    description = models.TextField(blank=True, help_text="Extra details or achievements")
    
    class Meta:
        ordering = ["-start_date"]
        
    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False, verbose_name="Currently working here")
    description = models.TextField(help_text="List duties and achievements. Separate points by double new lines (\n\n) or HTML break tags.")
    skills_used = models.ManyToManyField("Skill", blank=True, related_name="experiences")
    
    class Meta:
        ordering = ["-start_date"]
        
    def __str__(self):
        return f"{self.position} at {self.company}"
        
    @property
    def responsibilities_list(self):
        """Helper to break descriptions into lists by new lines."""
        if not self.description:
            return []
        return [point.strip() for point in self.description.split("\n") if point.strip()]


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="skills")
    proficiency = models.IntegerField(default=80, help_text="Percentage value from 0 to 100")
    icon_class = models.CharField(max_length=100, blank=True, help_text="FontAwesome class name, e.g., 'fa-brands fa-python'")
    
    class Meta:
        ordering = ["category", "-proficiency", "name"]
        
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    image = models.ImageField(upload_to="projects/", help_text="Mockup / preview image")
    description = models.TextField(help_text="Short description displayed on project card grids")
    detail_description = models.TextField(blank=True, help_text="Detailed HTML/Markdown/Text description shown on project details page")
    tech_stack = models.CharField(max_length=300, help_text="Comma separated tech stack. E.g., 'Django, Selenium, SQLite, Bootstrap 5'")
    github_url = models.URLField(blank=True, verbose_name="GitHub Repository URL")
    live_url = models.URLField(blank=True, verbose_name="Live Demo URL")
    featured = models.BooleanField(default=False, help_text="Show in featured list or priority sections")
    order = models.IntegerField(default=0, help_text="Display order, smaller numbers show first")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["order", "-created_at"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
        
    @property
    def tech_stack_list(self):
        if not self.tech_stack:
            return []
        return [tech.strip() for tech in self.tech_stack.split(",") if tech.strip()]


class Certificate(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=150)
    date_issued = models.DateField()
    image = models.ImageField(upload_to="certificates/", help_text="Image copy of the certificate")
    verification_url = models.URLField(blank=True, help_text="URL to verify certificate legitimacy online")
    
    class Meta:
        ordering = ["-date_issued"]
        
    def __str__(self):
        return f"{self.title} - {self.issuer}"


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(help_text="Short explanation of what this service offers")
    icon_class = models.CharField(max_length=100, help_text="FontAwesome icon class name. E.g., 'fa-solid fa-code' or 'fa-brands fa-searchengin'")
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ["order", "title"]
        
    def __str__(self):
        return self.title


class SocialLink(models.Model):
    platform_name = models.CharField(max_length=100, help_text="e.g. LinkedIn, GitHub, Instagram, Email")
    url = models.CharField(max_length=250, help_text="Full link URL (use mailto:email@domain.com for email links)")
    icon_class = models.CharField(max_length=100, help_text="FontAwesome class. E.g., 'fa-brands fa-linkedin', 'fa-regular fa-envelope'")
    
    def __str__(self):
        return self.platform_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
