// Newsletter data structure
let newsletters = [];
let filteredNewsletters = [];
let currentPage = 1;
const itemsPerPage = 6;

// DOM elements
const newslettersGrid = document.getElementById('newslettersGrid');
const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearch');
const loadMoreBtn = document.getElementById('loadMoreBtn');
const loadMoreContainer = document.getElementById('loadMoreContainer');
const loadingSpinner = document.getElementById('loadingSpinner');

// Stats elements
const totalNewslettersEl = document.getElementById('totalNewsletters');
const totalDownloadsEl = document.getElementById('totalDownloads');
const activeReadersEl = document.getElementById('activeReaders');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadNewsletters();
    setupEventListeners();
    updateStats();
});

// Setup event listeners
function setupEventListeners() {
    // Search functionality
    searchInput.addEventListener('input', debounce(handleSearch, 300));
    clearSearchBtn.addEventListener('click', clearSearch);
    
    // Load more functionality
    loadMoreBtn.addEventListener('click', loadMoreNewsletters);
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', handleNavbarScroll);
}

// Load newsletters from API or local data
async function loadNewsletters() {
    showLoading(true);
    
    try {
        // Try to fetch from API first
        const response = await fetch('/api/newsletters');
        if (response.ok) {
            newsletters = await response.json();
        } else {
            // Fallback to sample data
            newsletters = getSampleNewsletters();
        }
    } catch (error) {
        console.log('Using sample data:', error);
        newsletters = getSampleNewsletters();
    }
    
    filteredNewsletters = [...newsletters];
    displayNewsletters();
    showLoading(false);
}

// Sample newsletter data for demonstration
function getSampleNewsletters() {
    return [
        {
            id: 1,
            title: "July 2025 – Getting Started – Your Digital Foundation",
            date: "2025-07-01",
            filename: "july-2025-getting-started.pdf",
            downloads: 1250,
            description: "Kickstart your digital journey with foundational concepts and practical tips."
        },
        {
            id: 2,
            title: "June 2025 – AI Revolution – The Future is Now",
            date: "2025-06-01",
            filename: "june-2025-ai-revolution.pdf",
            downloads: 1890,
            description: "Explore the latest developments in artificial intelligence and machine learning."
        },
        {
            id: 3,
            title: "May 2025 – Cloud Computing – Scaling Your Dreams",
            date: "2025-05-01",
            filename: "may-2025-cloud-computing.pdf",
            downloads: 1420,
            description: "Master cloud technologies and learn how to scale your applications effectively."
        },
        {
            id: 4,
            title: "April 2025 – Cybersecurity – Protecting Your Digital Life",
            date: "2025-04-01",
            filename: "april-2025-cybersecurity.pdf",
            downloads: 1680,
            description: "Essential security practices to keep your digital assets safe and secure."
        },
        {
            id: 5,
            title: "March 2025 – Web Development – Building the Modern Web",
            date: "2025-03-01",
            filename: "march-2025-web-development.pdf",
            downloads: 2100,
            description: "Modern web development techniques and frameworks for 2025."
        },
        {
            id: 6,
            title: "February 2025 – Data Science – Insights from Information",
            date: "2025-02-01",
            filename: "february-2025-data-science.pdf",
            downloads: 1560,
            description: "Transform raw data into actionable insights with data science techniques."
        },
        {
            id: 7,
            title: "January 2025 – Blockchain & Web3 – The Decentralized Future",
            date: "2025-01-01",
            filename: "january-2025-blockchain-web3.pdf",
            downloads: 1780,
            description: "Understanding blockchain technology and the emerging Web3 ecosystem."
        },
        {
            id: 8,
            title: "December 2024 – DevOps & Automation – Streamlining Success",
            date: "2024-12-01",
            filename: "december-2024-devops-automation.pdf",
            downloads: 1340,
            description: "Automate your development workflow and deploy with confidence."
        }
    ];
}

// Display newsletters with pagination
function displayNewsletters() {
    const startIndex = 0;
    const endIndex = currentPage * itemsPerPage;
    const newslettersToShow = filteredNewsletters.slice(startIndex, endIndex);
    
    newslettersGrid.innerHTML = '';
    
    if (newslettersToShow.length === 0) {
        newslettersGrid.innerHTML = `
            <div class="col-12 text-center">
                <div class="no-results">
                    <i class="fas fa-search fa-3x text-primary mb-3"></i>
                    <h3 class="text-white">No newsletters found</h3>
                    <p class="text-white">Try adjusting your search terms or browse all newsletters.</p>
                    <button class="btn btn-outline-primary" onclick="clearSearch()">
                        <i class="fas fa-times me-2"></i>Clear Search
                    </button>
                </div>
            </div>
        `;
        return;
    }
    
    newslettersToShow.forEach(newsletter => {
        const newsletterCard = createNewsletterCard(newsletter);
        newslettersGrid.appendChild(newsletterCard);
    });
    
    // Show/hide load more button
    if (filteredNewsletters.length > endIndex) {
        loadMoreContainer.style.display = 'block';
    } else {
        loadMoreContainer.style.display = 'none';
    }
}

// Create newsletter card element
function createNewsletterCard(newsletter) {
    const col = document.createElement('div');
    col.className = 'col-lg-6 col-xl-4 mb-4';
    
    const date = new Date(newsletter.date);
    const formattedDate = date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long' 
    });
    
    col.innerHTML = `
        <div class="newsletter-card">
            ${newsletter.preview_image ? `
                <div class="newsletter-preview">
                    <img src="/newsletters/${newsletter.preview_image}" alt="Preview of ${newsletter.title}" class="preview-image">
                </div>
            ` : `
                <div class="newsletter-preview-placeholder">
                    <i class="fas fa-image"></i>
                    <span>No preview available</span>
                </div>
            `}
            <h3 class="newsletter-title">${newsletter.title}</h3>
            <div class="newsletter-date">
                <i class="fas fa-calendar-alt"></i>
                ${formattedDate}
            </div>
            <p class="newsletter-description mb-3">${newsletter.description}</p>
            <div class="newsletter-actions">
                <a href="/newsletters/${newsletter.filename}" 
                   class="btn btn-download" 
                   download
                   onclick="trackDownload(${newsletter.id})">
                    <i class="fas fa-download"></i>
                    Download PDF
                </a>
            </div>
        </div>
    `;
    
    return col;
}

// Search functionality
function handleSearch() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    if (searchTerm === '') {
        filteredNewsletters = [...newsletters];
    } else {
        filteredNewsletters = newsletters.filter(newsletter => {
            return newsletter.title.toLowerCase().includes(searchTerm) ||
                   newsletter.description.toLowerCase().includes(searchTerm) ||
                   new Date(newsletter.date).toLocaleDateString('en-US', { 
                       year: 'numeric', 
                       month: 'long' 
                   }).toLowerCase().includes(searchTerm);
        });
    }
    
    currentPage = 1;
    displayNewsletters();
}

// Clear search
function clearSearch() {
    searchInput.value = '';
    filteredNewsletters = [...newsletters];
    currentPage = 1;
    displayNewsletters();
}

// Load more newsletters
function loadMoreNewsletters() {
    currentPage++;
    displayNewsletters();
}

// Track download
function trackDownload(newsletterId) {
    // In a real application, you would send this to your analytics service
    console.log(`Download tracked for newsletter ${newsletterId}`);
    
    // Update local stats
    const newsletter = newsletters.find(n => n.id === newsletterId);
    if (newsletter) {
        newsletter.downloads++;
        updateStats();
    }
}



// Update statistics
function updateStats() {
    const totalNewsletters = newsletters.length;
    const totalDownloads = newsletters.reduce((sum, newsletter) => sum + newsletter.downloads, 0);
    const activeReaders = Math.floor(totalDownloads * 0.8); // Estimate active readers
    
    // Animate the numbers
    animateNumber(totalNewslettersEl, totalNewsletters);
    animateNumber(totalDownloadsEl, totalDownloads);
    animateNumber(activeReadersEl, activeReaders);
}

// Animate number counting
function animateNumber(element, target) {
    const start = 0;
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// Show/hide loading spinner
function showLoading(show) {
    if (show) {
        loadingSpinner.style.display = 'flex';
    } else {
        loadingSpinner.style.display = 'none';
    }
}

// Handle navbar scroll effect
function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(15, 15, 35, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
    } else {
        navbar.style.background = 'rgba(15, 15, 35, 0.95)';
        navbar.style.boxShadow = 'none';
    }
}

// Utility function: Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add some interactive effects
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to newsletter cards
    document.addEventListener('mouseover', function(e) {
        if (e.target.closest('.newsletter-card')) {
            e.target.closest('.newsletter-card').style.transform = 'translateY(-5px)';
        }
    });
    
    document.addEventListener('mouseout', function(e) {
        if (e.target.closest('.newsletter-card')) {
            e.target.closest('.newsletter-card').style.transform = 'translateY(0)';
        }
    });
    
    // Add click effects to buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn')) {
            const btn = e.target.closest('.btn');
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                btn.style.transform = '';
            }, 150);
        }
    });
});

// Export functions for potential use in other scripts
window.NewsletterApp = {
    loadNewsletters,
    searchNewsletters: handleSearch,
    clearSearch,
    trackDownload,
    trackRead,
    updateStats
}; 