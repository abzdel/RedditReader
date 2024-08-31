document.addEventListener('DOMContentLoaded', () => {
    const toggleSidebarButton = document.getElementById('toggleSidebar');
    const historyContent = document.getElementById('historyContent');

    toggleSidebarButton.addEventListener('click', () => {
        if (historyContent.classList.contains('collapsed')) {
            historyContent.classList.remove('collapsed');
        } else {
            historyContent.classList.add('collapsed');
        }
    });
});
