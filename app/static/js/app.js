var getUrl = window.location;
const app_urlsite = getUrl .protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];


function activeSidebar(el){
	$('.sidebar-sticky li a').removeClass('active');
	$(el).addClass('active');
}


function validate(evt) {
	var theEvent = evt || window.event;
  
	// Handle paste
	if (theEvent.type === 'paste') {
		key = event.clipboardData.getData('text/plain');
	} else {
	// Handle key press
		var key = theEvent.keyCode || theEvent.which;
		key = String.fromCharCode(key);
	}
	var regex = /[0-9]|\./;
	if( !regex.test(key) ) {
	  theEvent.returnValue = false;
	  if(theEvent.preventDefault) theEvent.preventDefault();
	}
  }