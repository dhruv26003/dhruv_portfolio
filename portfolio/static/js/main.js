document.addEventListener("DOMContentLoaded", () => {
    
    /* ==========================================================================
       THEME CONTROLLER (DARK/LIGHT TOGGLE)
       ========================================================================== */
    const themeToggle = document.getElementById("themeToggle");
    const htmlElement = document.documentElement;
    const toggleIcon = themeToggle ? themeToggle.querySelector(".toggle-icon") : null;

    // Load theme from localStorage or fallback to default 'dark'
    const currentTheme = localStorage.getItem("theme") || "dark";
    htmlElement.setAttribute("data-theme", currentTheme);
    updateToggleIcon(currentTheme);

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            let targetTheme = "dark";
            if (htmlElement.getAttribute("data-theme") === "dark") {
                targetTheme = "light";
            }
            htmlElement.setAttribute("data-theme", targetTheme);
            localStorage.setItem("theme", targetTheme);
            updateToggleIcon(targetTheme);
        });
    }

    function updateToggleIcon(theme) {
        if (!toggleIcon) return;
        if (theme === "light") {
            toggleIcon.className = "fa-solid fa-sun text-warning toggle-icon";
        } else {
            toggleIcon.className = "fa-solid fa-moon text-yellow toggle-icon";
        }
    }

    /* ==========================================================================
       ANIMATIONS INITIALIZER (AOS & TYPED.JS)
       ========================================================================== */
    // Initialize AOS
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 800,
            easing: "ease-in-out",
            once: true,
            mirror: false
        });
    }

    // Initialize Typed.js for Hero taglines
    const typedElement = document.getElementById("typed");
    if (typedElement && typeof Typed !== "undefined") {
        new Typed("#typed", {
            strings: [
                "Python Automation Engineer",
                "Django Developer",
                "Backend Developer",
                "AI Automation Specialist"
            ],
            typeSpeed: 60,
            backSpeed: 40,
            backDelay: 2000,
            loop: true
        });
    }

    /* ==========================================================================
       LOADER DISSOLVE EFFECT
       ========================================================================== */
    const loader = document.getElementById("loader");
    if (loader) {
        window.addEventListener("load", () => {
            setTimeout(() => {
                loader.style.opacity = "0";
                loader.style.visibility = "hidden";
            }, 600);
        });
        
        // Safety timeout if window load takes too long
        setTimeout(() => {
            loader.style.opacity = "0";
            loader.style.visibility = "hidden";
        }, 3000);
    }

    /* ==========================================================================
       STICKY NAVBAR & SCROLL PROGRESS INDICATOR
       ========================================================================== */
    const navbar = document.querySelector(".custom-navbar");
    const scrollProgress = document.getElementById("scrollProgress");
    const backToTopBtn = document.getElementById("backToTop");
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    const sections = document.querySelectorAll("section");

    window.addEventListener("scroll", () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        
        // 1. Update Scroll Progress Bar
        if (scrollProgress && docHeight > 0) {
            const scrollPercent = (scrollTop / docHeight) * 100;
            scrollProgress.style.width = scrollPercent + "%";
        }

        // 2. Sticky Navbar state
        if (navbar) {
            if (scrollTop > 50) {
                navbar.classList.add("navbar-scrolled");
            } else {
                navbar.classList.remove("navbar-scrolled");
            }
        }

        // 3. Back To Top Visibility
        if (backToTopBtn) {
            if (scrollTop > 400) {
                backToTopBtn.classList.add("show");
            } else {
                backToTopBtn.classList.remove("show");
            }
        }

        // 4. Update Active Nav Link on Scroll
        let currentSectionId = "";
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            if (scrollTop >= sectionTop && scrollTop < sectionTop + sectionHeight) {
                currentSectionId = section.getAttribute("id");
            }
        });

        if (currentSectionId) {
            navLinks.forEach(link => {
                link.classList.remove("active");
                if (link.getAttribute("href").includes(currentSectionId)) {
                    link.classList.add("active");
                }
            });
        }
    });

    // Back to top scroll execution
    if (backToTopBtn) {
        backToTopBtn.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }

    /* ==========================================================================
       SKILLS REAL-TIME FILTERING & SEARCH
       ========================================================================== */
    const skillSearchBar = document.getElementById("skillSearch");
    const skillFilterButtons = document.querySelectorAll(".skill-filter-btn");
    const skillCards = document.querySelectorAll(".skill-card-wrapper");

    function filterSkills() {
        const query = skillSearchBar ? skillSearchBar.value.toLowerCase().trim() : "";
        
        // Find current active category
        let activeCategory = "all";
        skillFilterButtons.forEach(btn => {
            if (btn.classList.contains("active")) {
                activeCategory = btn.getAttribute("data-category");
            }
        });

        skillCards.forEach(card => {
            const skillName = card.getAttribute("data-skill-name");
            const skillCategory = card.getAttribute("data-skill-category");
            
            const matchQuery = skillName.includes(query);
            const matchCategory = activeCategory === "all" || skillCategory === activeCategory;

            if (matchQuery && matchCategory) {
                card.style.display = "block";
                setTimeout(() => { card.style.opacity = "1"; card.style.transform = "scale(1)"; }, 10);
            } else {
                card.style.opacity = "0";
                card.style.transform = "scale(0.85)";
                setTimeout(() => { card.style.display = "none"; }, 300);
            }
        });
    }

    if (skillSearchBar) {
        skillSearchBar.addEventListener("input", filterSkills);
    }

    skillFilterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            skillFilterButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            filterSkills();
        });
    });

    /* ==========================================================================
       PROJECTS REAL-TIME FILTERING & SEARCH
       ========================================================================== */
    const projectSearchBar = document.getElementById("projectSearch");
    const projectFilterButtons = document.querySelectorAll(".project-filter-btn");
    const projectCards = document.querySelectorAll(".project-card-wrapper");

    function filterProjects() {
        const query = projectSearchBar ? projectSearchBar.value.toLowerCase().trim() : "";
        
        let activeCategory = "all";
        projectFilterButtons.forEach(btn => {
            if (btn.classList.contains("active")) {
                activeCategory = btn.getAttribute("data-category");
            }
        });

        projectCards.forEach(card => {
            const projName = card.getAttribute("data-project-name");
            const projStack = card.getAttribute("data-project-stack");
            const projCategory = card.getAttribute("data-project-category");

            const matchQuery = projName.includes(query) || projStack.includes(query);
            const matchCategory = activeCategory === "all" || projCategory === activeCategory;

            if (matchQuery && matchCategory) {
                card.style.display = "block";
                setTimeout(() => { card.style.opacity = "1"; card.style.transform = "scale(1)"; }, 10);
            } else {
                card.style.opacity = "0";
                card.style.transform = "scale(0.85)";
                setTimeout(() => { card.style.display = "none"; }, 300);
            }
        });
    }

    if (projectSearchBar) {
        projectSearchBar.addEventListener("input", filterProjects);
    }

    projectFilterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            projectFilterButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            filterProjects();
        });
    });

    /* ==========================================================================
       CONTACT FORM AJAX SUBMISSION
       ========================================================================== */
    const contactForm = document.getElementById("contactForm");
    const submitBtn = document.getElementById("submitContactBtn");
    const contactAlert = document.getElementById("contactAlert");

    if (contactForm) {
        contactForm.addEventListener("submit", (e) => {
            // Prevent default HTML submit redirect
            e.preventDefault();
            
            // UI Loading state
            if (submitBtn) {
                const btnText = submitBtn.querySelector(".btn-text");
                const btnLoader = submitBtn.querySelector(".btn-loader");
                
                submitBtn.disabled = true;
                if (btnText) btnText.classList.add("d-none");
                if (btnLoader) btnLoader.classList.remove("d-none");
            }

            // Prepare details
            const actionUrl = contactForm.getAttribute("action");
            const formData = new FormData(contactForm);

            // Fetch request
            fetch(actionUrl, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (contactAlert) {
                    contactAlert.className = "alert"; // Reset classes
                    contactAlert.classList.remove("d-none");
                    
                    if (data.success) {
                        contactAlert.classList.add("alert-success");
                        contactAlert.innerHTML = `<i class="fa-solid fa-circle-check me-2"></i>${data.message}`;
                        contactForm.reset();
                        
                        // Clear success alert after 8 seconds
                        setTimeout(() => {
                            contactAlert.classList.add("d-none");
                        }, 8000);
                    } else {
                        contactAlert.classList.add("alert-danger");
                        let errText = data.message || "Submission failed. Please check form parameters.";
                        if (data.errors) {
                            errText += "<ul class='mb-0 mt-2'>";
                            for (let field in data.errors) {
                                errText += `<li><strong>${field}:</strong> ${data.errors[field][0]}</li>`;
                            }
                            errText += "</ul>";
                        }
                        contactAlert.innerHTML = `<i class="fa-solid fa-circle-exclamation me-2"></i>${errText}`;
                    }
                }
            })
            .catch(error => {
                console.error("AJAX Error:", error);
                if (contactAlert) {
                    contactAlert.className = "alert alert-danger";
                    contactAlert.classList.remove("d-none");
                    contactAlert.innerHTML = `<i class="fa-solid fa-triangle-exclamation me-2"></i>Network communication error. Please try again later.`;
                }
            })
            .finally(() => {
                // UI Restore state
                if (submitBtn) {
                    const btnText = submitBtn.querySelector(".btn-text");
                    const btnLoader = submitBtn.querySelector(".btn-loader");
                    
                    submitBtn.disabled = false;
                    if (btnText) btnText.classList.remove("d-none");
                    if (btnLoader) btnLoader.classList.add("d-none");
                }
            });
        });
    }

    /* ==========================================================================
       INTERACTIVE CANVAS PARTICLES
       ========================================================================== */
    const canvas = document.getElementById("particleCanvas");
    if (canvas) {
        const ctx = canvas.getContext("2d");
        let particlesArray = [];
        let mouse = {
            x: null,
            y: null,
            radius: 120
        };

        // Resize Canvas dynamically
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener("resize", resizeCanvas);

        // Track cursor
        window.addEventListener("mousemove", (event) => {
            mouse.x = event.x;
            mouse.y = event.y;
        });

        window.addEventListener("mouseleave", () => {
            mouse.x = null;
            mouse.y = null;
        });

        // Particle blueprints
        class Particle {
            constructor(x, y, directionX, directionY, size, color) {
                this.x = x;
                this.y = y;
                this.directionX = directionX;
                this.directionY = directionY;
                this.size = size;
                this.color = color;
            }

            // Draw individual node
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
                ctx.fillStyle = this.color;
                ctx.fill();
            }

            // Process movement
            update() {
                // Check edge collisions
                if (this.x > canvas.width || this.x < 0) {
                    this.directionX = -this.directionX;
                }
                if (this.y > canvas.height || this.y < 0) {
                    this.directionY = -this.directionY;
                }

                // Check mouse collision (push vectors)
                if (mouse.x != null && mouse.y != null) {
                    let dx = mouse.x - this.x;
                    let dy = mouse.y - this.y;
                    let distance = Math.sqrt(dx*dx + dy*dy);
                    
                    if (distance < mouse.radius) {
                        if (mouse.x < this.x && this.x < canvas.width - this.size * 10) {
                            this.x += 2;
                        }
                        if (mouse.x > this.x && this.x > this.size * 10) {
                            this.x -= 2;
                        }
                        if (mouse.y < this.y && this.y < canvas.height - this.size * 10) {
                            this.y += 2;
                        }
                        if (mouse.y > this.y && this.y > this.size * 10) {
                            this.y -= 2;
                        }
                    }
                }

                // Move node
                this.x += this.directionX;
                this.y += this.directionY;
                this.draw();
            }
        }

        // Initialize particles count proportional to screen area
        function initParticles() {
            particlesArray = [];
            let numberOfParticles = (canvas.width * canvas.height) / 12000;
            numberOfParticles = Math.min(numberOfParticles, 120); // Cap nodes count

            const isLightTheme = () => htmlElement.getAttribute("data-theme") === "light";

            for (let i = 0; i < numberOfParticles; i++) {
                let size = (Math.random() * 2) + 1;
                let x = (Math.random() * ((canvas.width - size * 2) - size * 2)) + size * 2;
                let y = (Math.random() * ((canvas.height - size * 2) - size * 2)) + size * 2;
                
                // Speed ratios
                let directionX = (Math.random() * 0.4) - 0.2;
                let directionY = (Math.random() * 0.4) - 0.2;
                
                let color = isLightTheme() ? "rgba(2, 132, 199, 0.12)" : "rgba(56, 189, 248, 0.18)";
                
                particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
            }
        }

        // Connect nodes close together with lines
        function connectParticles() {
            const isLightTheme = () => htmlElement.getAttribute("data-theme") === "light";
            let opacityValue = 1;
            
            for (let a = 0; a < particlesArray.length; a++) {
                for (let b = a; b < particlesArray.length; b++) {
                    let dx = particlesArray[a].x - particlesArray[b].x;
                    let dy = particlesArray[a].y - particlesArray[b].y;
                    let distance = Math.sqrt(dx*dx + dy*dy);
                    
                    let limit = 110;
                    if (distance < limit) {
                        opacityValue = 1 - (distance / limit);
                        let lineColor = isLightTheme() 
                            ? `rgba(2, 132, 199, ${opacityValue * 0.08})` 
                            : `rgba(56, 189, 248, ${opacityValue * 0.12})`;
                            
                        ctx.strokeStyle = lineColor;
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                        ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                        ctx.stroke();
                    }
                }
            }
        }

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < particlesArray.length; i++) {
                particlesArray[i].update();
            }
            connectParticles();
        }

        initParticles();
        animate();

        // Regenerate particles on theme toggler click
        if (themeToggle) {
            themeToggle.addEventListener("click", () => {
                setTimeout(initParticles, 100);
            });
        }
    }
});
