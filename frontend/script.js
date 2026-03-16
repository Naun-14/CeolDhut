// CeòlDhut - Celtic Music Platform JavaScript



// DOM Elements



const navbar = document.getElementById('navbar');

const navMenu = document.getElementById('nav-menu');

const hamburger = document.getElementById('hamburger');

const miniPlayer = document.getElementById('mini-player');

const playPauseBtn = document.getElementById('play-pause');

const currentSong = document.getElementById('current-song');

const progressBar = document.getElementById('progress-bar');

const volumeSlider = document.getElementById('volume-slider');



// Startup

document.addEventListener('DOMContentLoaded', function() 

{

    initNavigation();

    initScrollEffects();

    initPlayer();

    initSearch();

});



// Planning

function initNavigation() 

{

    // Sticky navbar

if (navbar) 

{





    window.addEventListener('scroll', function()

     {

        if (window.scrollY > 100) {

            navbar.classList.add('sticky');

        } 

        else 

            {

            navbar.classList.remove('sticky');

        }

    });}



    // Mobile hamburger menu

    if

     (hamburger && navMenu) 

        {

    hamburger.addEventListener('click', function() 

    {

        navMenu.classList.toggle('active');

        hamburger.classList.toggle('active');

    });

}

    // Close mobile menu when clicking a link

    document.querySelectorAll('.nav-link').forEach(link =>

         {

        link.addEventListener('click', function() 

        {

            navMenu.classList.remove('active');

            hamburger.classList.remove('active');

        });

    });

}



// Scroll effects for fade-in animations

function initScrollEffects() 

{

    const observerOptions = 

    {

        threshold: 0.1,

        rootMargin: '0px 0px -50px 0px'

    };



    const observer = new IntersectionObserver(function(entries)

     {

        entries.forEach(entry => 

            {

            if (entry.isIntersecting) 

                {

                entry.target.classList.add('visible');

            }

        });

    },

     observerOptions);



    // Observe all fade-in sections

    document.querySelectorAll('.fade-in').forEach(section => 

        {

        observer.observe(section);

    });

}



// Music player functionality

function initPlayer() 

{

    let isPlaying = false;

    let currentTrack = null;



    // Play/pause button

    if (playPauseBtn) 

        {

    playPauseBtn.addEventListener('click', function() 

    {

        isPlaying = !isPlaying;

        playPauseBtn.textContent = isPlaying ? '⏸' : '▶';



        if (isPlaying) 

            {

            // Simulate progress

            simulateProgress();

        }

    });



    // Volume control

    if (volumeSlider) 

        {

    volumeSlider.addEventListener('input', function() 

    {

        // actual audio volume

        console.log('Volume:', this.value);

    });
}



    // Click on play buttons to change current song

    document.querySelectorAll('.play-btn, .play-icon').forEach(btn => 

        {

        btn.addEventListener('click', function() 

        {

            const card = this.closest('.featured-card, .track-card');

            if (card) 

                {

               const titleElement = card.querySelector('h3, h4');

               const title = titleElement ? titleElement.textContent : '';

               const artistElement = card.querySelector('.artist, p');

               const artist = artistElement ? artistElement.textContent : '';

                currentSong.textContent = `${title} - ${artist}`;

                isPlaying = true;

                playPauseBtn.textContent = '⏸';

                progressBar.style.width = '0%';

                simulateProgress();

            }

        });

    });



    function simulateProgress() 

    {

        let progress = 0;

        const interval = setInterval(() => 

            {

            if (!isPlaying) 

                {

                clearInterval(interval);

                return;

            }

            progress += 0.5;

            if (progress >= 100) 

                {

                progress = 0;

                isPlaying = false;

                playPauseBtn.textContent = '▶';

                clearInterval(interval);

            }

            progressBar.style.width = progress + '%';

        }, 100);

    }

}



// Search functionality

function initSearch() 

{
    const searchInput = document.getElementById('search-input');
    
    if (searchInput) 
    {
        const genreFilter = document.getElementById('genre-filter');
        const regionFilter = document.getElementById('region-filter');
        const popularityFilter = document.getElementById('popularity-filter');

        // Search input handler
        searchInput.addEventListener('input', function() 
        {
            filterContent();
        });

        // Filter handlers
        [genreFilter, regionFilter, popularityFilter].forEach(filter => 
        {
            filter.addEventListener('change', function() 
            {
                filterContent();
            });
        });
    }



    function filterContent()

     {

        const searchTerm = searchInput.value.toLowerCase();

        const genreValue = genreFilter.value;

        const regionValue = regionFilter.value;

        const popularityValue = popularityFilter.value;



        // Filter featured cards

        document.querySelectorAll('.featured-card').forEach(card =>

             {

            const title = card.querySelector('h3').textContent.toLowerCase();

            const artist = card.querySelector('.artist').textContent.toLowerCase();

            const genre = card.querySelector('.genre').textContent.toLowerCase();



            const matchesSearch = title.includes(searchTerm) || artist.includes(searchTerm);

            const matchesGenre = !genreValue || genre.includes(genreValue);

            const region = card.dataset.region;

            const matchesRegion = !regionValue || region === regionValue;

            const matchesPopularity = true;

            if (matchesSearch && matchesGenre && matchesRegion && matchesPopularity) {

                card.style.display = 'block';

            } else 

                {

                card.style.display = 'none';

            }

        });



        // Filter track cards

        document.querySelectorAll('.track-card').forEach(card =>

        {

            const title = card.querySelector('h4').textContent.toLowerCase();

            const artist = card.querySelector('p').textContent.toLowerCase();



            const matchesSearch = title.includes(searchTerm) || artist.includes(searchTerm);



            if

             (matchesSearch) 

                {

                card.style.display = 'flex';

            } 

            else 

                {

                card.style.display = 'none';

            }

        });

    }

}



document.querySelectorAll('.region-card').forEach(card => {

    card.addEventListener('click', function() {

        const title = this.querySelector('h3');

        if (title) {
            const region = title.textContent.toLowerCase();
            alert(`Exploring ${region} music!`);
        }

    });

});


  card.addEventListener('click', function() 
  {
    const region = this.querySelector('h3').textContent.toLowerCase();

    // In a real app, this would navigate to a region-specific page
    alert(`Exploring ${region} music!`);
});


// Add to playlist functionality

document.querySelectorAll('.add-btn').forEach(btn => {

    btn.addEventListener('click', function() {

        // In a real app, this would add to user's playlist

        this.textContent = '✓ Added';

        this.style.background = '#4CAF50';

        setTimeout(() => {

            this.textContent = '+ Add';

            this.style.background = '#d4af37';

        }, 2000);

    });

});



// Keyboard navigation improvements



document.addEventListener('keydown', function(e) 

{

    // Close mobile menu with Escape key

    if (e.key === 'Escape' && navMenu.classList.contains('active'))

    {

        navMenu.classList.remove('active');

        hamburger.classList.remove('active');

    }

});



// Smooth scrolling for anchor links

document.querySelectorAll('a[href^="#"]').forEach(anchor =>

     {

    anchor.addEventListener('click', function(e) 

    {

        e.preventDefault();

        const target = document.querySelector(this.getAttribute('href'));

        if (target) 

        {

            target.scrollIntoView({

                behavior: 'smooth',

                block: 'start'

            });

        }

    });

});



// Performance optimization: Lazy load images

const images = document.querySelectorAll('img[data-src]');

const imageObserver = new IntersectionObserver((entries, observer) => 

    {

    entries.forEach(entry =>

         {

        if (entry.isIntersecting) 

            {

            const img = entry.target;

            img.src = img.dataset.src;

            img.classList.remove('lazy');

            observer.unobserve(img);

        }

    });

});



images.forEach(img => imageObserver.observe(img));



// Console log for debugging (remove in production)

console.log('CeòlDhut Celtic Music Platform loaded successfully!');
}