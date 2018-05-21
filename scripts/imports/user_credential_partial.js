import GetFormData from "./get_form_data";
import Requests from "./requests";
import Modal from "./modal";
export default class Credential{
	constructor(){
		this.addEventListeners();
		this.formData = [];
		this.isUsernameMatch = true;
		this.isPasswordMatch = true;
	}
	addEventListeners(){
		const form = document.querySelector("form.credentials-form");
		if (!form) return;
		form.addEventListener('submit',this.submitForm.bind(this));
		let buttonConfirm = document.querySelector("#modal-button--confirm");
		buttonConfirm.addEventListener("click",this.finishProcess.bind(this));
		let repeatUsername = document.querySelector("#repeat_username");
		let repeatPassword = document.querySelector("#repeat_password");
		repeatPassword.addEventListener("change",this.checkPassword.bind(this));
		repeatUsername.addEventListener("change",this.checkUsername.bind(this));
	}
	checkUsername(){
		let error = document.getElementById("match-username");
		let repeatUsername = document.querySelector("#repeat_username");
		let username = document.getElementById("username");
		if (repeatUsername.value !== username.value) {
			this.isUsernameMatch = false;
			console.log(this.isUsernameMatch);
			repeatUsername.classList.add("login-container-form-element--error");
			repeatUsername.focus();
			repeatUsername.style.outline = "none";
		    error.style.display = "block";
		    repeatUsername.value = "";
		}
	}
	checkPassword(){
		let error = document.getElementById("match-password");
		let repeatPassword = document.querySelector("#repeat_password");
		let password = document.getElementById("password");
		if (repeatPassword.value !== password.value) {
			this.isPasswordMatch = false;
			console.log(this.isPasswordMatch);
			repeatPassword.classList.add("login-container-form-element--error");
			repeatPassword.focus();
			repeatPassword.style.outline = "none";
		    error.style.display = "block";
		    repeatPassword.value = "";
		}
	}
	/* take data from form*/
	collectData(){
		let password = document.getElementById("password").value;
		let username = document.getElementById("username").value;
		this.formData.push(password);
		this.formData.push(username);
	}
	/* format the data*/
	formatData(){
			let credentials = {
				"username": this.formData[1],
                "password": this.formData[0]
            };
				return credentials;
		}
	submitForm(evt){
		evt.preventDefault();
		this.collectData();
		let data = this.formatData();
		console.log(data);
		this.sendData(data);
	}
	/*send data to the server with request API*/
	sendData(data){
		let request = new Requests("POST", this.response.bind(this), this.respondedWithError.bind(this),this.showPreloader.bind(this));
		request.send("http://1a139e3b.ngrok.io/register/user",data);
	}
	/* handle the response*/
	response(e){
		const response = JSON.parse(e.target.responseText); 
		if(response.success){
			this.hidePreloader();
			this.displayConfirmation();
		}else{
			this.displayError(response.ErrorMessage);
		}
	}
	respondedWithError(evt){
		console.log(evt.target.responseText);
	}
	/* confirmation */
	displayConfirmation(){
		let modal = document.getElementById("user_success_message");
		modal._show();
	}
	/* dispalaying an error */
	displayError(ErrorMessage){
		let messageParagraph = document.querySelector(".confirmation_message");
		messageParagraph.innerHTML = ErrorMessage;
		let modal = document.getElementById("user_success_message");
		modal._show();
		console.log(messageParagraph);
	}
	finishProcess(){
		location.reload();
	}
	showPreloader(){
		let preloader = document.querySelector(".preloader");
		console.log(preloader);
		preloader.classList.add("show-preloader");
	}
	hidePreloader(){
		let preloader = document.querySelector(".preloader");
		preloader.classList.remove("show-preloader");
	}
}
