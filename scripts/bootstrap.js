import Modal from "./imports/modal";

(function(){
	const button = document.querySelector('#button');
	button.addEventListener('click', function(){ 
	    document.querySelector('rs-modal')._show();
	});

	document.registerElement("rs-modal", Modal);
})();