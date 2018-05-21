export default class Modaltest {
	constructor(){
		this.addEventListeners();
	}
	addEventListeners(){
		const button = document.querySelector('#button');
		button.addEventListener('click', this.selectModal);
	}
	selectModal(){
		let activeModal = document.getElementById("modal1");
		activeModal._show();
	} 
}
