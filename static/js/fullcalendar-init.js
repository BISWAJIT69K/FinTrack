// FullCalendar initialization for dashboard

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('dashboardCalendar');
    if (!calendarEl) return;

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: window.dashboardCalendarEvents || [],
        eventContent: function(arg) {
            // Custom rendering for event entries
            return {
                html: `<b>${arg.event.title}</b> <span>₹${arg.event.extendedProps.amount}</span>`
            };
        },
        height: 500
    });
    calendar.render();
});
