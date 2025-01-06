document.addEventListener('DOMContentLoaded', function() {
    // Category filtering
    const categoryButtons = document.querySelectorAll('.category-filter');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            window.location.href = `?category=${encodeURIComponent(category)}`;
        });
    });

    // Tag filtering
    const tagButtons = document.querySelectorAll('.tag-filter');
    tagButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const tag = this.dataset.tag;
            window.location.href = `?tag=${encodeURIComponent(tag)}`;
        });
    });

    // Top posts sorting
    const topButton = document.querySelector('.sort-by-top');
    if (topButton) {
        topButton.addEventListener('click', function(e) {
            e.preventDefault();
            const currentUrl = new URL(window.location.href);
            const sort = currentUrl.searchParams.get('sort');
            
            if (sort === 'top') {
                // If already sorted by top, remove sort parameter
                currentUrl.searchParams.delete('sort');
            } else {
                currentUrl.searchParams.set('sort', 'top');
            }
            
            window.location.href = currentUrl.toString();
        });
    }
}); 