// Highlight today's date in FullCalendar with blue background

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('dashboardCalendar');
    if (!calendarEl || !window.FullCalendar) return;

    var calendar = calendarEl._fullCalendar;
    if (!calendar) return;

    // Add custom CSS for today
    var style = document.createElement('style');
    style.innerHTML = '.fc-day-today { background: #3b82f6 !important; color: #fff !important; }';
    document.head.appendChild(style);
});
