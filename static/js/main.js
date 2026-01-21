
document.addEventListener('DOMContentLoaded', function () {
    // 1. Page Fade-In Effect
    const content = document.querySelector('.content-wrapper') || document.body;
    content.classList.add('fade-in');

    // 2. Auto-dismiss alerts with smooth fade out
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.classList.remove('show'); // Bootstrap fade class processing
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150); // Remove from DOM after transition
        }, 5000);
    });

    // 3. Active Sidebar Link Highlighting
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('#sidebarMenu .nav-link');

    sidebarLinks.forEach(function (link) {
        link.classList.remove('active');
        const linkPath = link.getAttribute('href');
        if (linkPath && linkPath !== '#' && (currentPath === linkPath || currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });

    // 4. Enhanced Client-side Table Search
    const searchInput = document.getElementById('tableSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function () { // Changed from 'keyup' to 'input' for better response
            const filter = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('table tbody tr');
            let hasResults = false;

            tableRows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(filter)) {
                    row.style.display = '';
                    row.classList.add('fade-in'); // Re-trigger animation
                    hasResults = true;
                } else {
                    row.style.display = 'none';
                }
            });

            // Handle "No Results" message
            let noResultRow = document.getElementById('no-result-row');
            if (!hasResults && filter !== '') {
                if (!noResultRow) {
                    const tbody = document.querySelector('table tbody');
                    noResultRow = document.createElement('tr');
                    noResultRow.id = 'no-result-row';
                    noResultRow.innerHTML = `<td colspan="100%" class="text-center py-4 text-muted">لا توجد نتائج مطابقة لـ "${this.value}"</td>`;
                    tbody.appendChild(noResultRow);
                } else {
                    noResultRow.innerHTML = `<td colspan="100%" class="text-center py-4 text-muted">لا توجد نتائج مطابقة لـ "${this.value}"</td>`;
                    noResultRow.style.display = '';
                }
            } else if (noResultRow) {
                noResultRow.style.display = 'none';
            }
        });
    }

    // 5. Delete Confirmation (Simple but safer)
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!confirm('هل أنت متأكد من أنك تريد الحذف؟ هذا الإجراء لا يمكن التراجع عنه.')) {
                e.preventDefault();
            }
        });
    });

    // 6. Bootstrap Tooltips Initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
