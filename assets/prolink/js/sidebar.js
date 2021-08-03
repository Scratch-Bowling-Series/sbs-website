$(document).ready(function()
{
	var sidebarOpen = false;
	$('.sidebar').on("mouseenter", function() {
        $('.sidebar-icon').addClass('sidebar-icon-close');
			$('.sidebar').addClass('sidebar-expanded');
			sidebarOpen = true;
    }).on("mouseleave", function() {
        $('.sidebar').removeClass('sidebar-icon-close');
			$('.sidebar').removeClass('sidebar-expanded');
			sidebarOpen = false;
    });
});