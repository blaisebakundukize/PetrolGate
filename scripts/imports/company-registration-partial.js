import GetFormData from "./get_form_data";
import Requests from "./requests";
import Modal from "./modal";
export default class Registration{
	constructor(){
		this.addEventListeners();
	}
	addEventListeners(){
		const form = document.querySelector("form.company-registration-form");
		if (!form) return;
		form.addEventListener('submit',this.submitForm.bind(this));
		let buttonConfirm = document.querySelector("#modal-button--confirm");
		buttonConfirm.addEventListener("click",this.finishProcess.bind(this));
	}
	submitForm(evt){
		evt.preventDefault();
		let getFormData = new GetFormData();
		this.sendData(getFormData.get_form_data(evt.target));
		let data = getFormData.get_form_data(evt.target);
		let jsonData = JSON.stringify(data);
		console.log(typeof jsonData);
		console.log(jsonData);
		this.sendData(jsonData);
	}
	/*send data to the server with request API*/
	sendData(data){
		let request = new Requests("POST", this.response.bind(this), this.respondedWithError.bind(this)/*,this.showPreloader.bind(this)*/);
		request.dataType = "json"
		console.write(request)
		request.send("/registration/company",data);
	}
	/* handle the response*/
	response(e){
		/*console.log(JSON.parse(e.target.responseText)); */
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
		let modal = document.getElementById("company_success_message");
		modal._show();
	}
	/* dispalaying an error */
	displayError(ErrorMessage){
		let messageParagraph = document.querySelector(".confirmation_message");
		messageParagraph.innerHTML = ErrorMessage;
		let modal = document.getElementById("company_success_message");
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
document.registerElement("rs-modal", Modal);