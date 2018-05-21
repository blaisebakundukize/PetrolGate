import GetFormData from "./get_form_data";
import Requests from "./requests";
import Modal from "./modal";
export default class EmployeeRegistration{
	constructor(){
		this.addEventListeners();
	}
	addEventListeners(){
		const form = document.querySelector("form.employee-registration-form");
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
		console.log(jsonData);
		this.sendData(jsonData);
	}
	/*send data to the server with request API*/
	sendData(data){
		let request = new Requests("POST", this.response.bind(this), this.respondedWithError.bind(this),this.showPreloader.bind(this));
		request.send("http://e52cbac.ngrok.io/register/employee",data);
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
		console.log(this.responseText);
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
		let employeeModal = document.getElementById("employee_success_message");
		employeeModal._show();
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
/*document.registerElement("rs-modal", Modal);*/