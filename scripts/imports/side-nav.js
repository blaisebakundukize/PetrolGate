export default class SideNav{
	constructor(){
		this.windowOnClick = this.windowOnClick.bind(this);
		this.addEventListeners();
		this.KEYS = {
            ESC: 27
        };
	}
	_onKeyDown(evt){
        if(evt.keyCode == this.KEYS.ESC) this.toggleNavigation();
    }
	togglePopup(){
		var profilePopUp = document.querySelector(".profile-popup");
		var arrowUp = document.querySelector(".arrow-up");
    	profilePopUp.classList.toggle("show-profile");
    	arrowUp.classList.toggle("show-profile");
    }
    toggleNavigation() {
    	var navMenu = document.querySelector(".nav-container");
    	var navContainer = document.querySelector(".side-nav-container");
        navContainer.classList.toggle("show-navigation-container");
        navMenu.classList.toggle("show-navigation");
    }
    windowOnClick(event) {
    	var navContainer = document.querySelector(".side-nav-container");
        if (event.target === navContainer) {
            this.toggleNavigation();
        }
    }
    addEventListeners(){
    	var navContainer = document.querySelector(".side-nav-container");
    	var toggleButton = document.querySelectorAll(".page-header__show-button");
    	for (var i = 0; i < toggleButton.length; i++) {
    		toggleButton[i].addEventListener("click", this.toggleNavigation);
    	}
    	var profile = document.querySelector(".profile");
    	window.addEventListener("click", this.windowOnClick);
    	profile.addEventListener("click", this.togglePopup);
    	navContainer.addEventListener('keydown', this._onKeyDown);
    }
}
