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
            const targetId = this.getAttribute('href').substring(1) || 'home';
            if (window.location.hash === '#' + targetId) {
                navigateToSection(targetId, true);
            } else {
                window.location.hash = targetId;
            }
            // Close mobile menu if open
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
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
// --- Slug and Category Mapping ---
const categorySlugs = {
    'projects-grid': 'instagram-carousels',
    'logos-grid': 'logo-designs',
    'festive-grid': 'festive-posts',
    'thumbnails-grid': 'instagram-thumbnails',
    'stories-grid': 'instagram-stories',
    'product-design-grid': 'product-design'
};

const categorySlugToGridId = {
    'instagram-carousels': 'projects-grid',
    'logo-designs': 'logos-grid',
    'festive-posts': 'festive-grid',
    'instagram-thumbnails': 'thumbnails-grid',
    'instagram-stories': 'stories-grid',
    'product-design': 'product-design-grid'
};

let currentCategorySlug = null;

function findProjectBySlug(slug) {
    const datasets = [
        typeof projectsData !== 'undefined' ? projectsData : [],
        typeof logoData !== 'undefined' ? logoData : [],
        typeof festiveData !== 'undefined' ? festiveData : [],
        typeof thumbnailData !== 'undefined' ? thumbnailData : [],
        typeof storiesData !== 'undefined' ? storiesData : [],
        typeof productDesignData !== 'undefined' ? productDesignData : []
    ];
    for (const dataset of datasets) {
        const found = dataset.find(p => p.slug === slug);
        if (found) return found;
    }
    return null;
}

function getCategorySlugForProject(project) {
    if (typeof projectsData !== 'undefined' && projectsData.includes(project)) return 'instagram-carousels';
    if (typeof logoData !== 'undefined' && logoData.includes(project)) return 'logo-designs';
    if (typeof festiveData !== 'undefined' && festiveData.includes(project)) return 'festive-posts';
    if (typeof thumbnailData !== 'undefined' && thumbnailData.includes(project)) return 'instagram-thumbnails';
    if (typeof storiesData !== 'undefined' && storiesData.includes(project)) return 'instagram-stories';
    if (typeof productDesignData !== 'undefined' && productDesignData.includes(project)) return 'product-design';
    return null;
}

function navigateToSection(sectionId, smooth = true) {
    const target = document.getElementById(sectionId);
    if (target) {
        target.scrollIntoView({
            behavior: smooth ? 'smooth' : 'auto'
        });
    }
}

function showCategoryUI(categorySlug, scroll = true) {
    const categoriesView = document.getElementById('categories-view');
    const projectsDisplayView = document.getElementById('projects-display-view');
    const activeCategoryTitle = document.getElementById('active-category-title');
    const grids = document.querySelectorAll('#projects-display-view .projects-grid');

    const targetGridId = categorySlugToGridId[categorySlug];
    if (!targetGridId) return false;

    const categoryCard = document.querySelector(`.category-card[data-target="${targetGridId}"]`);
    const categoryTitle = categoryCard ? categoryCard.querySelector('.category-title').textContent : 'Portfolio';

    categoriesView.style.display = 'none';
    projectsDisplayView.style.display = 'block';
    activeCategoryTitle.textContent = categoryTitle;

    grids.forEach(grid => {
        grid.style.display = 'none';
    });

    const targetGrid = document.getElementById(targetGridId);
    if (targetGrid) {
        targetGrid.style.display = 'grid';

        const cards = targetGrid.querySelectorAll('.project-card');
        cards.forEach((item, idx) => {
            if (!item.classList.contains('visible')) {
                setTimeout(() => {
                    item.classList.add('visible');
                }, idx * 50);
            }
        });
    }

    if (scroll) {
        navigateToSection('portfolio', true);
    }
    return true;
}

function handleRouting(isInitialLoad = false) {
    const hash = window.location.hash;
    
    // Detect active page markers
    const hasProjectsMark = document.getElementById('categories-view') !== null;
    const hasExperienceMark = document.getElementById('experience-page') !== null;
    
    const isProjectsPage = hasProjectsMark;
    const isExperiencePage = hasExperienceMark;
    const isIndexPage = !isProjectsPage && !isExperiencePage;
    
    if (isIndexPage) {
        // --- 1. HOME PAGE ROUTING ---
        if (!hash) {
            window.location.hash = 'home';
            return;
        }
        
        // Redirections from Home Page
        if (hash.startsWith('#project/') || hash.startsWith('#category/') || hash === '#portfolio') {
            window.location.href = 'projects.html' + hash;
            return;
        }
        // Scroll local sections
        const sectionId = hash.substring(1);
        const knownSections = ['home', 'experience', 'education', 'projects', 'contact'];
        if (knownSections.includes(sectionId)) {
            navigateToSection(sectionId, !isInitialLoad);
        }
        return;
    }
    
    if (isExperiencePage) {
        // --- 2. EXPERIENCE PAGE ROUTING ---
        if (!hash) {
            window.location.hash = 'experience';
            return;
        }
        
        // Redirections from Experience Page
        if (hash.startsWith('#project/') || hash.startsWith('#category/') || hash === '#portfolio') {
            window.location.href = 'projects.html' + hash;
            return;
        }
        if (hash === '#home' || hash === '#contact') {
            window.location.href = 'index.html' + hash;
            return;
        }
        
        // Scroll local sections on experience page
        const sectionId = hash.substring(1);
        const knownSections = ['experience', 'education'];
        if (knownSections.includes(sectionId)) {
            navigateToSection(sectionId, !isInitialLoad);
        }
        return;
    }
    
    if (isProjectsPage) {
        // --- 3. PROJECTS PAGE ROUTING ---
        // Force default slug hash if empty or legacy '#projects'
        if (!hash || hash === '#projects') {
            window.location.hash = 'portfolio';
            return;
        }

        // Redirections from Projects Page
        if (hash === '#home' || hash === '#contact') {
            window.location.href = 'index.html' + hash;
            return;
        }
        if (hash === '#experience' || hash === '#education') {
            window.location.href = 'index.html' + hash;
            return;
        }

        if (hash.startsWith('#project/')) {
            const projectSlug = hash.replace('#project/', '');
            const project = findProjectBySlug(projectSlug);

            if (project) {
                const categorySlug = getCategorySlugForProject(project);
                currentCategorySlug = categorySlug;

                if (categorySlug) {
                    showCategoryUI(categorySlug, false);
                }

                openModal(project);
            } else {
                window.location.hash = '#portfolio';
            }
        } else if (hash.startsWith('#category/')) {
            closeModal();
            const categorySlug = hash.replace('#category/', '');
            currentCategorySlug = categorySlug;
            const success = showCategoryUI(categorySlug, !isInitialLoad);
            if (!success) {
                window.location.hash = '#portfolio';
            }
        } else {
            closeModal();
            currentCategorySlug = null;

            const categoriesView = document.getElementById('categories-view');
            const projectsDisplayView = document.getElementById('projects-display-view');
            if (categoriesView && projectsDisplayView) {
                projectsDisplayView.style.display = 'none';
                categoriesView.style.display = 'grid';
            }
        }
        return;
    }
}

function goBackFromProject() {
    window.location.hash = currentCategorySlug ? `#category/${currentCategorySlug}` : '#portfolio';
}

// --- Instagram Carousel Implementation ---

document.addEventListener('DOMContentLoaded', () => {
    const projectsGrid = document.getElementById('projects-grid');
    console.log("Checking project data...");

    if (projectsGrid) {
        if (typeof projectsData !== 'undefined') {
            console.log("Projects found:", projectsData.length);
            renderProjects(projectsData, 'projects-grid');

            // Render Logos (if data exists)
            if (typeof logoData !== 'undefined') {
                renderProjects(logoData, 'logos-grid');
            }

            // Render Festive Posts (if data exists)
            if (typeof festiveData !== 'undefined') {
                renderProjects(festiveData, 'festive-grid');
            }

            // Render Thumbnails (if data exists)
            if (typeof thumbnailData !== 'undefined') {
                renderProjects(thumbnailData, 'thumbnails-grid');
            }

            // Render Instagram Stories (if data exists)
            if (typeof storiesData !== 'undefined') {
                renderProjects(storiesData, 'stories-grid');
            }

            // Render Product Designs (if data exists)
            if (typeof productDesignData !== 'undefined') {
                renderProjects(productDesignData, 'product-design-grid');
            }

            // Setup Category Navigation Dashboard
            setupCategoryNavigation();

            // Initialize Routing
            handleRouting(true);

            // Register hashchange listener
            window.addEventListener('hashchange', () => {
                handleRouting(false);
            });
        } else {
            console.error("projectsData is undefined. Check projects_data.js loading.");
            projectsGrid.innerHTML = '<p style="color: red;">Error loading projects data.</p>';
        }
    } else {
        console.log("projects-grid element not found (not on projects page). Initializing routing...");
        // Initialize Routing for home/experience pages
        handleRouting(true);

        // Register hashchange listener
        window.addEventListener('hashchange', () => {
            handleRouting(false);
        });
    }
});

function setupCategoryNavigation() {
    const categoryCards = document.querySelectorAll('.category-card');
    const backToCategoriesBtn = document.getElementById('back-to-categories-btn');

    categoryCards.forEach(card => {
        card.addEventListener('click', () => {
            const targetGridId = card.getAttribute('data-target');
            const slug = categorySlugs[targetGridId];
            if (slug) {
                window.location.hash = `#category/${slug}`;
            }
        });
    });

    if (backToCategoriesBtn) {
        backToCategoriesBtn.addEventListener('click', () => {
            window.location.hash = '#portfolio';
        });
    }
}

function getDesignType(containerId) {
    switch (containerId) {
        case 'projects-grid':
            return 'Instagram Carousel';
        case 'logos-grid':
            return 'Logo Design';
        case 'festive-grid':
            return 'Festive Post';
        case 'thumbnails-grid':
            return 'Instagram Thumbnail';
        case 'stories-grid':
            return 'Instagram Story';
        case 'product-design-grid':
            return 'Product Design';
        default:
            return 'Design';
    }
}

function renderProjects(projects, containerId = 'projects-grid') {
    const projectsGrid = document.getElementById(containerId);
    if (!projectsGrid) {
        console.error(`Container with ID '${containerId}' not found.`);
        return;
    }

    // Clear existing content
    projectsGrid.innerHTML = '';

    const designType = getDesignType(containerId);

    projects.forEach((project, index) => {
        const card = document.createElement('div');
        card.className = 'project-card animate-on-scroll';
        card.style.animationDelay = `${index * 0.05}s`; // Staggered animation
        card.style.cursor = 'pointer'; // Indicate clickable

        // On Click -> Open Modal via hash routing
        card.addEventListener('click', () => {
            window.location.hash = `#project/${project.slug}`;
        });

        // Show only the first image as a preview card
        const imagePath = `${project.folder}/${project.images[0]}`;
        const aspectRatio = project.aspect_ratio || (4 / 5);

        const instagramBtnHtml = project.instagram_link ? `
            <a href="${project.instagram_link}" target="_blank" class="instagram-btn">
                <i class="fab fa-instagram"></i> View on Instagram
            </a>
        ` : '';

        card.innerHTML = `
            <div class="project-image-wrapper" style="aspect-ratio: ${aspectRatio}; overflow: hidden; position: relative;">
                <img src="${imagePath}" alt="${project.title}" loading="lazy">
            </div>
            <div class="project-info">
                <div class="project-type-subtext">${designType}</div>
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
        }, 50 * index);
    });
}

let activeAutoPlayTimer = null;

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
        activeAutoPlayTimer = autoPlayTimer;
    }

    function stopAutoPlay() {
        if (autoPlayTimer) clearInterval(autoPlayTimer);
        if (activeAutoPlayTimer === autoPlayTimer) activeAutoPlayTimer = null;
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
        goBackFromProject();
    }
}

if (modal) {
    window.onclick = function (event) {
        if (event.target == modal) {
            goBackFromProject();
        }
    }
}

// Escape key listener for closing modal
window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('project-modal');
        if (modal && modal.style.display === 'flex') {
            goBackFromProject();
        }
    }
});

function closeModal() {
    if (modal && modal.classList.contains('show')) {
        modal.classList.remove('show');
        if (activeAutoPlayTimer) {
            clearInterval(activeAutoPlayTimer);
            activeAutoPlayTimer = null;
        }
        setTimeout(() => {
            modal.style.display = "none";
            document.body.style.overflow = "auto";
            if (modalBody) modalBody.innerHTML = '';
        }, 300); // Wait for transition
    }
}

function openModal(project) {
    if (!modal) return;

    if (activeAutoPlayTimer) {
        clearInterval(activeAutoPlayTimer);
        activeAutoPlayTimer = null;
    }

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
            initCarousel(modalBody.querySelector('.carousel-container'), project.images.length, true);
        }
    }

    // Show Modal
    modal.style.display = "flex";
    // Trigger reflow to ensure transition happens
    void modal.offsetWidth;
    modal.classList.add('show');
    document.body.style.overflow = "hidden"; // Disable background scroll
}
