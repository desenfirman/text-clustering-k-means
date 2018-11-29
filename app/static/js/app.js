var getUrl = window.location;
const app_urlsite = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];

function loadPage(page,div){
	$.ajax({
		url: app_urlsite+page,
		success: function(response){
			$(div).html(response);
		},
		dataType:"html"  		
	});
	return false;
}

function activeSidebar(el){
	$('.sidebar-sticky li a').removeClass('active');
	$(el).addClass('active');
}