document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = mobileMenuBtn.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Smooth Scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
                // Close mobile menu if open
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    const icon = mobileMenuBtn.querySelector('i');
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    });

    // Simple scroll animation (Intersection Observer)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-on-scroll').forEach((el) => {
        observer.observe(el);
    });
});
// --- Instagram Carousel Implementation ---

document.addEventListener('DOMContentLoaded', () => {
    const projectsGrid = document.getElementById('projects-grid');
    console.log("Checking project data...");

    if (projectsGrid) {
        if (typeof projectsData !== 'undefined') {
            console.log("Projects found:", projectsData.length);
            renderProjects(projectsData, 'projects-grid');

            // Render Festive Posts (if data exists)
            if (typeof festiveData !== 'undefined') {
                renderProjects(festiveData, 'festive-grid');
            }
        } else {
            console.error("projectsData is undefined. Check projects_data.js loading.");
            projectsGrid.innerHTML = '<p style="color: red;">Error loading projects data.</p>';
        }
    } else {
        console.error("projects-grid element not found!");
    }
});

function renderProjects(projects, containerId = 'projects-grid') {
    const projectsGrid = document.getElementById(containerId);
    if (!projectsGrid) {
        console.error(`Container with ID '${containerId}' not found.`);
        return;
    }

    // Clear existing content (optional, but good for re-renders)
    projectsGrid.innerHTML = '';

    projects.forEach((project, index) => {
        const card = document.createElement('div');
        card.className = 'project-card animate-on-scroll';
        card.style.animationDelay = `${index * 0.1}s`; // Staggered animation
        card.style.cursor = 'pointer'; // Indicate clickable

        // On Click -> Open Modal
        card.addEventListener('click', (e) => {
            // Check if click was on carousel button/dot, if so don't open modal (optional, but good UX)
            if (e.target.closest('.carousel-btn') || e.target.closest('.dot') || e.target.closest('.instagram-btn')) {
                return;
            }
            openModal(project);
        });

        // Generate slides HTML
        const slidesHtml = project.images.map((img, i) => {
            const imagePath = `${project.folder}/${img}`;
            return `
            <div class="carousel-slide">
                <img src="${imagePath}" alt="${project.title} - Slide ${i + 1}">
            </div>
        `}).join('');

        // Generate dots HTML
        const dotsHtml = project.images.length > 1 ? `
            <div class="carousel-dots">
                ${project.images.map((_, i) => `<span class="dot ${i === 0 ? 'active' : ''}" data-index="${i}"></span>`).join('')}
            </div>
        ` : '';

        // Generate buttons HTML
        const buttonsHtml = project.images.length > 1 ? `
            <button class="carousel-btn prev" aria-label="Previous Slide"><i class="fas fa-chevron-left"></i></button>
            <button class="carousel-btn next" aria-label="Next Slide"><i class="fas fa-chevron-right"></i></button>
        ` : '';

        const instagramBtnHtml = project.instagram_link ? `
            <a href="${project.instagram_link}" target="_blank" class="instagram-btn">
                <i class="fab fa-instagram"></i> View on Instagram
            </a>
        ` : '';

        // Default to 4/5 if not present
        const aspectRatio = project.aspect_ratio || (4 / 5);

        card.innerHTML = `
            <div class="carousel-container" id="carousel-${index}" style="aspect-ratio: ${aspectRatio};">
                <div class="carousel-track">
                    ${slidesHtml}
                </div>
                ${buttonsHtml}
                ${dotsHtml}
            </div>
            <div class="project-info">
                <div class="project-brand">${project.brand}</div>
                <div class="project-title">${project.title}</div>
                <p class="project-description">${project.description}</p>
                ${instagramBtnHtml}
            </div>
        `;

        projectsGrid.appendChild(card);

        // Trigger animation
        setTimeout(() => {
            card.classList.add('visible');
        }, 100 * index);

        // Initialize carousel functionality for this card
        if (project.images.length > 1) {
            initCarousel(card.querySelector('.carousel-container'), project.images.length, true);
        }
    });
}

function initCarousel(container, slideCount, enableAutoPlay = false) {
    const track = container.querySelector('.carousel-track');
    const prevBtn = container.querySelector('.prev');
    const nextBtn = container.querySelector('.next');
    const dots = container.querySelectorAll('.dot');
    let autoPlayTimer;

    let currentIndex = 0;

    function updateCarousel() {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;

        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % slideCount;
        updateCarousel();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + slideCount) % slideCount;
        updateCarousel();
    }

    // Auto-play Logic
    function startAutoPlay() {
        if (!enableAutoPlay) return;
        stopAutoPlay(); // Clear existing to be safe
        autoPlayTimer = setInterval(nextSlide, 3000); // 3 seconds
    }

    function stopAutoPlay() {
        if (autoPlayTimer) clearInterval(autoPlayTimer);
    }

    // Start auto-play initially (only if visible)
    if (enableAutoPlay) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    startAutoPlay();
                } else {
                    stopAutoPlay();
                }
            });
        }, { threshold: 0.5 }); // 50% visible

        observer.observe(container);
    } else {
        // If auto-play is disabled (e.g. modal), we don't need observer
    }

    // Pause on interaction
    container.addEventListener('mouseenter', stopAutoPlay);
    container.addEventListener('mouseleave', startAutoPlay);
    container.addEventListener('touchstart', stopAutoPlay, { passive: true });
    container.addEventListener('touchend', startAutoPlay, { passive: true });


    if (nextBtn) {
        nextBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            stopAutoPlay(); // Reset timer on manual interaction
            nextSlide();
            // Optional: Restart timer after delay? simple startAutoPlay() rely on mouseleave
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            stopAutoPlay();
            prevSlide();
        });
    }

    // Dot navigation
    dots.forEach((dot, i) => {
        dot.addEventListener('click', (e) => {
            e.stopPropagation();
            stopAutoPlay();
            currentIndex = i;
            updateCarousel();
        });
    });

    // Touch support (Swipe)
    let touchStartX = 0;
    let touchEndX = 0;

    container.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    container.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const threshold = 50;
        if (touchEndX < touchStartX - threshold) {
            // Swipe Left -> Next
            nextSlide();
        }
        if (touchEndX > touchStartX + threshold) {
            // Swipe Right -> Prev
            prevSlide();
        }
    }
}

// --- Modal Logic ---
const modal = document.getElementById('project-modal');
const closeModalBtn = document.querySelector('.close-modal');
const modalBody = document.querySelector('.modal-body');

if (closeModalBtn) {
    closeModalBtn.onclick = function () {
        closeModal();
    }
}

if (modal) {
    window.onclick = function (event) {
        if (event.target == modal) {
            closeModal();
        }
    }
}

function closeModal() {
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        }, 300); // Wait for transition
    }
}

function openModal(project) {
    if (!modal) return;

    // Populate Modal Content
    // Re-use logic to generate carousel, but adapted for modal
    const slidesHtml = project.images.map((img, i) => {
        const imagePath = `${project.folder}/${img}`;
        return `
        <div class="carousel-slide">
            <img src="${imagePath}" alt="${project.title} - Slide ${i + 1}">
        </div>
    `}).join('');

    const dotsHtml = project.images.length > 1 ? `
        <div class="carousel-dots">
            ${project.images.map((_, i) => `<span class="dot ${i === 0 ? 'active' : ''}" data-index="${i}"></span>`).join('')}
        </div>
    ` : '';

    const buttonsHtml = project.images.length > 1 ? `
        <button class="carousel-btn prev" aria-label="Previous Slide"><i class="fas fa-chevron-left"></i></button>
        <button class="carousel-btn next" aria-label="Next Slide"><i class="fas fa-chevron-right"></i></button>
    ` : '';

    const instagramBtnHtml = project.instagram_link ? `
        <a href="${project.instagram_link}" target="_blank" class="instagram-btn" style="margin-top: 20px; font-size: 1.1rem;">
            <i class="fab fa-instagram"></i> View on Instagram
        </a>
    ` : '';

    if (modalBody) {
        modalBody.innerHTML = `
            <div class="modal-carousel-wrapper"> 
                <div class="carousel-container">
                    <div class="carousel-track">
                        ${slidesHtml}
                    </div>
                    ${buttonsHtml}
                    ${dotsHtml}
                </div>
            </div>
            <div class="modal-info-wrapper">
                <div class="modal-project-brand">${project.brand}</div>
                <h2 class="modal-project-title">${project.title}</h2>
                <p class="modal-project-description">${project.description}</p>
                ${instagramBtnHtml}
            </div>
        `;

        // Initialize carousel inside modal
        if (project.images.length > 1) {
            initCarousel(modalBody.querySelector('.carousel-container'), project.images.length, false);
        }
    }

    // Show Modal
    modal.style.display = "flex";
    // Trigger reflow to ensure transition happens
    void modal.offsetWidth;
    modal.classList.add('show');
    document.body.style.overflow = "hidden"; // Disable background scroll
}
