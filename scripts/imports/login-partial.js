
import Requests from "./requests";
export default class Login {
	constructor(){
		this.addEventListeners = this.addEventListeners.bind(this);
		this.collectData = this.collectData.bind(this);
		this.sendData = this.sendData.bind(this);
		this.response = this.response.bind(this);
		this.addEventListeners();
		this.formData = [];
		this.customizer();
	}
    /* take data from form*/
	collectData(){
		let password = document.getElementById("login-container-form-password").value;
		let username = document.getElementById("login-container-form-username").value;
		this.formData.push(password);
		this.formData.push(username);
		this.formatData();
	}
	/* format the data*/
	formatData(){
			let credentials = {
				"username": this.formData[1],
                "password": this.formData[0]
            };
				return credentials;
		}
    /*send data to the server with request API*/
	sendData(e){
	    e.preventDefault();
	    console.log("sending data");
		this.collectData();
		let data = this.formatData();
		let request = new Requests("POST", this.response, this.respondedWithError);
		request.dataType = "form";
		request.send("/login", data);

	}
	/* handle the response not yet finished testing remaining*/
	response(e){
		// const response = e.target.responseText;
		const response = JSON.parse(e.target.responseText); 
		const redirectToUrl = "/home";
		if(response.success){
			console.log('success');
			window.location.href = redirectToUrl;
		}else{
			this.displayError(response.errorMessage);
		}
		const data = e.target.responseText;
		console.log(data);
	}
	respondedWithError(evt){
		console.log(this.responseText);
	}
	/* handle the error*/
	displayError(message){
		let username = document.getElementById("login-container-form-username");
		let password = document.getElementById("login-container-form-password");
		let error = document.getElementById("login-error--message");
		username.classList.add("login-container-form-element--error");
		password.classList.add("login-container-form-element--error");
		error.style.display = "block";
		error.innerHTML = message;
		username.value = "";
		password.value = "";
	}
	/* customize the login page because it has no header as other pages*/
	customizer(){
		let mainContainer = document.querySelector(".main-container");
		let pageHeader = document.querySelector(".page-header");
		let profile = document.querySelector(".profile-popup");
		mainContainer.classList.add("main-container--no-header");
		pageHeader.style.display = "none";
		profile.style.display = "none";
	} 
	/* adding listener to the form */
	addEventListeners(){
	let form = document.getElementById("login-container-form");
	form.addEventListener("submit",this.sendData);
	}
}