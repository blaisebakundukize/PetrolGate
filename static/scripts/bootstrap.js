/*!
 * Build: 2018-05-17T15:53:02.767Z
 */
class Modal extends HTMLElement{
    createdCallback(){
        this.windowClick = this.windowClick.bind(this);
        this.allowWindowClick = this.allowWindowClick.bind(this);
        this._hide = this._hide.bind(this);
        this.KEYS = {
            ESC: 27
        };
    }
    attachedCallback(){
        this._setTitle();
        this._displayPrint();
        this.tabIndex = "1";
    }
    _show(){
        this._addEventListeners();
        this.previousActiviveEl = document.activeElement;
        this.setAttribute("visible", true);
        this.focus();
    }
    _hide(){
        this.setAttribute("visible", false);
        this.previousActiviveEl.focus();
        this._removeEventListeners();
    }
    _addEventListeners(){
        this.closeButton = this.querySelector(".modal-header-close");
        this.closeButton.addEventListener("click", this._hide);
        this.addEventListener("keydown", this._onKeyDown);
        window.addEventListener("click",this.allowWindowClick);
    }
    _removeEventListeners(){
        this.closeButton.removeEventListener("click", this._hide);
        this.removeEventListener("keydown", this._onKeyDown);
        window.removeEventListener("click",this.allowWindowClick);
    }
    _onKeyDown(evt){
        if(evt.keyCode == this.KEYS.ESC) this._hide();
    }
    windowClick(event){
        if (event.target == this) {
            this._hide();
        }
    }
    allowWindowClick(){
        if (this.hasAttribute("windowClick")) {
            this.windowClick(event);
        }
    }
    _insertBefore(insertIn,element,beforeThis){
         if(!element && !beforeThis) return;
        insertIn.insertBefore(element,beforeThis);
    }
    _setTitle(){
        let modalHeaderEl = this.createModalHeader();
        let modalContentsEl = this.querySelector("rs-modal-contents");
        this._insertBefore(modalContentsEl,modalHeaderEl,modalContentsEl.firstElementChild);
    }
    _addPrint(){
        let modalBody = this.querySelector("rs-modal-body");
        let printButton = this.createPrintButton();
        let modalContentsEl = this.querySelector("rs-modal-contents");
        console.log(modalContentsEl);
        this._insertBefore(modalContentsEl,printButton,modalBody);
    }
    _displayPrint(){
        if (this.hasAttribute("print")) {
            this._addPrint();
        }
    }
    createPrintButton(){
        let button = document.createElement("button");
        button.classList.add("button");
        button.classList.add("button--print");
        let iconEl = document.createElement("i");
        iconEl.classList.add("material-icons");
        iconEl.innerHTML = "print";
        button.appendChild(iconEl);
        return button;
    }
    createModalHeader(){
        let titleEl = document.createElement("h1");
        titleEl.classList.add("modal-header-title");
        titleEl.textContent = this.getAttribute("title");
        let closeButtonEl = document.createElement("button");
        closeButtonEl.classList.add("modal-header-close");
        closeButtonEl.innerHTML = "&times;";
        let modalHeaderEl = document.createElement("rs-modal-header");
        modalHeaderEl.appendChild(titleEl);
        modalHeaderEl.appendChild(closeButtonEl);
        return modalHeaderEl;
    }
}

class SideNav{
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

class Filter{
	constructor(){
		this.table;
		this.status = 0;
		this.celIndex;
		this.ids = {
			"less_than": 1,
			"greater_than": 2,
			"equal": 3,
			"range": 4
		};
		this._onKeyUp = this._onKeyUp.bind(this);
		this.setStatus = this.setStatus.bind(this);
		this._addEventListeners = this._addEventListeners.bind(this);
		this._removeEventListeners = this._removeEventListeners.bind(this);
		this.outFocus = this.outFocus.bind(this);
		this.onFocus = this.onFocus.bind(this);
		this._addEventListeners();
	}
	setStatus(e){
		let id = e.target.getAttribute("id");
		this.status = this.ids[id];
	}
	_onKeyUp(e){
		let data = Number(e.target.value);
		switch(this.status) {
			case 0:
			this.message();
			break;
			case 1:
			this.less_than(data);
			break;
			case 2:
			this.greater_than(data);
			break;
			case 3:
			this.equal(data);
			break;
			case 4:
			this.range(data);
		}
	}
	message(){
		alert("Select the filter");
	}
	less_than(donne){
		let tr = this.table.querySelectorAll("tr:not(.unfiltable)");
		for (let i = 0; i < tr.length; i++) {
			let td = tr[i].getElementsByTagName("td")[this.celIndex];
			if (td) {
				if (donne > Number(td.innerHTML) || donne === 0) {
					tr[i].style.display = "";
				} else {
					tr[i].style.display = "none";
				}
			}
		}
	}
	greater_than(donne){
		let tr = this.table.querySelectorAll("tr:not(.unfiltable)");
		for (let i = 0; i < tr.length; i++) {
			let td = tr[i].getElementsByTagName("td")[this.celIndex];
			if (td) {
				if (donne < Number(td.innerHTML) || donne === 0) {
					tr[i].style.display = "";
				} else {
					tr[i].style.display = "none";
				}
			}
		}
	}
	equal(donne){
		let tr = this.table.querySelectorAll("tr:not(.unfiltable)");
		for (let i = 0; i < tr.length; i++) {
			let td = tr[i].getElementsByTagName("td")[this.celIndex];
			if (td) {
				if (Number(td.innerHTML) === donne || donne === 0) {
					tr[i].style.display = "";
				} else {
					tr[i].style.display = "none";
				}
			}
		}
	}
	range(donne){
		console.log("range");
	}
	outFocus(){
		this.status = 0;
	}
	onFocus(e){
		let currentFilter = e.target;
		let holder = currentFilter.parentNode;
		let filterWidget = holder.parentNode;
		let cell = filterWidget.parentNode;
		let tr = cell.parentNode;
		let currentTable = tr.parentNode;
		this.table = currentTable;
		let currentCellIndex = cell.cellIndex;
		this.celIndex = currentCellIndex;
	}
	resetTable(){
		for (let i = 0; i < this.tr.length; i++) {
			this.tr[i].style.display = "";
		}
		document.getElementsByClassName("form-element--filter-greater")[0].value = " ";
	}
	_addEventListeners(){
		let filter = document.querySelectorAll(".form-element--filter-greater");
		for (var i = 0; i < filter.length; i++) {
			filter[i].addEventListener("keyup",this._onKeyUp);
			filter[i].addEventListener("focusout",this.outFocus);
			filter[i].addEventListener("focus",this.onFocus);
		}
		let filterButton = document.querySelectorAll(".filter-button");
		for (var i = 0; i < filterButton.length; i++) {
			filterButton[i].addEventListener("click",this.setStatus);
		}
    }
    _removeEventListeners(){
       let filter = document.querySelectorAll(".form-element--filter-greater");
		for (var i = 0; i < filter.length; i++) {
			filter[i].removeEventListener("keyup",this._onKeyUp);
			filter[i].removeEventListener("focusout",this.outFocus);
		}
		let filterButton = document.querySelectorAll(".filter-button");
		for (var i = 0; i < filterButton.length; i++) {
			filterButton[i].removeEventListener("click",this.setStatus);
		}
    }
}

class Requests$1 {
    constructor (method='GET', onload=function(){}, onerror = function(){}, onprogress = function(){}) {
        this.METHODS = ['GET', 'POST', 'PUT', 'DELETE'];
        this.dataType = "form";
        this.method = method;
        this.request = new XMLHttpRequest();
        this.onload = onload;
        this.onprogress = onprogress;
        this.onerror = onerror;
    }
    send(url=null, data = {} ){
        if(!url) return;
        const encodedData = this.urlEncodedData(data);
        this.url = `${url}?${encodedData}`;
        this.body = null;
        if(!this.METHODS.includes(this.method.toUpperCase())){
            console.warn("Invalid request method:", this.method);
            return;
        }
        if ( this.method.toUpperCase() != 'GET' && this.method.toUpperCase() != 'DELETE') {
            this.url = url;
            this.body = this.urlEncodedData(data);
            this.request.open(this.method, this.url, true);
            this.request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            console.log("Datat type", this.dataType);
            if (this.dataType.toUpperCase() === "JSON") {
                this.body = JSON.stringify(data);
            }
        }else{
            this.request.open(this.method, this.url, true);
        }
        this.request.onload = this.onload;
        this.request.onprogress = this.onprogress;
        this.request.onerror = this.onerror;
        this.request.send(this.body);
    }
    urlEncodedData(data){
        var urlEncodedData = "";
        var urlEncodedDataPairs = [];
        for(let name in data) {
            let pair = encodeURIComponent(name) + '=' + encodeURIComponent(data[name]);
            urlEncodedDataPairs.push(pair);
        }
        urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');
        return urlEncodedData;
    }
}

class Login {
	constructor(){
		this.addEventListeners = this.addEventListeners.bind(this);
		this.collectData = this.collectData.bind(this);
		this.sendData = this.sendData.bind(this);
		this.response = this.response.bind(this);
		this.addEventListeners();
		this.formData = [];
		this.customizer();
	}
	collectData(){
		let password = document.getElementById("login-container-form-password").value;
		let username = document.getElementById("login-container-form-username").value;
		this.formData.push(password);
		this.formData.push(username);
		this.formatData();
	}
	formatData(){
			let credentials = {
				"username": this.formData[1],
                "password": this.formData[0]
            };
				return credentials;
		}
	sendData(e){
	    e.preventDefault();
	    console.log("sending data");
		this.collectData();
		let data = this.formatData();
		let request = new Requests$1("POST", this.response, this.respondedWithError);
		request.dataType = "form";
		request.send("/login", data);
	}
	response(e){
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
	customizer(){
		let mainContainer = document.querySelector(".main-container");
		let pageHeader = document.querySelector(".page-header");
		let profile = document.querySelector(".profile-popup");
		mainContainer.classList.add("main-container--no-header");
		pageHeader.style.display = "none";
		profile.style.display = "none";
	}
	addEventListeners(){
	let form = document.getElementById("login-container-form");
	form.addEventListener("submit",this.sendData);
	}
}

class Pagination{
		constructor(tableId,paginationId,data,pageNumber){
			this.page = 1;
			this.pageRecords = pageNumber;
			this.data = data;
			this.addEventListeners = this.addEventListeners.bind(this);
			this.loadTable = this.loadTable.bind(this);
			this.click = this.click.bind(this);
			this.paginationSize = Math.ceil(this.data.length/this.pageRecords);
			this.table = document.querySelector("#"+tableId);
			this.paginationContainer = document.querySelector("#"+paginationId);
			this.loadTable(this.page);
			this.loadPagination(this.page,this.paginationSize);
			this.addEventListeners();
		}
		next(){
			this.page++;
			if (this.page > this.paginationSize) {
				this.page = this.paginationSize;
			}else{
				this.loadTable(this.page);
			}
		}
		prev(){
			this.page--;
			if (this.page < 1) {
				this.page = 1;
			}else{
				this.loadTable(this.page);
			}
		}
		loadPagination(s,f){
			for (let i = s; i <= f; i++) {
				let a = document.createElement("a");
				let attributeId = document.createAttribute("id");
				let currentId ="page"+i;
				attributeId.nodeValue = currentId;
				a.setAttributeNode(attributeId);
				a.classList.add("pagination__a");
				a.innerHTML =""+i;
				this.paginationContainer.appendChild(a);
			}
			this.activePagination();
		}
		activePagination(){
			let other = this.paginationContainer.querySelectorAll(".pagination__a");
			for (var i = 0; i < other.length; i++) {
				other[i].classList.remove("pagination__a--active");
			}
			this.paginationContainer.querySelector("#page"+this.page).classList.add("pagination__a--active");
		}
		click(e){
			if (e.target.parentNode.nextElementSibling == this.paginationContainer) {
				this.prev();
				this.activePagination();
			}else if (e.target.parentNode.previousElementSibling == this.paginationContainer) {
				this.next();
				this.activePagination();
			}else{
				if (e.target.parentNode == this.paginationContainer) {
						this.page = Number(e.target.innerHTML);
						this.loadTable(this.page);
						this.activePagination();
					}
				}
		}
		loadTable(page){
			let from = (this.page -1)*this.pageRecords;
			let to = (this.pageRecords*this.page-1)+1;
			let currentRange = this.data.slice(from,to);
			if (this.table!=null) {
				let tbody = this.table.querySelector("tbody");
			}
			tbody.innerHTML = "";
			for (let i = 0; i < currentRange.length; i++) {
				let tr = document.createElement("tr");
				let keys =  Object.getOwnPropertyNames(currentRange[i]);
				for (let j = 0; j < keys.length; j++) {
					let currentkey = keys[j];
					let td = document.createElement("td");
					td.innerHTML = currentRange[i][currentkey];
					tr.appendChild(td);
				}
				tbody.appendChild(tr);
			}
		}
		addEventListeners(){
			let paginations = document.querySelectorAll(".pagination__a");
			for (var i = 0; i < paginations.length; i++) {
				paginations[i].addEventListener("click",this.click);
			}
		}
	}

class GetFormData{
	constructor(){
	}
	get_form_data(form = null){
		let formData = {};
		let isInvalid = false;
		let hasFieldsets=false;
		if(form.querySelector('fieldset') !== null ) hasFieldsets = true;
		if(form==null && !(form instanceof HTMLElement) ) return formData;
		if (hasFieldsets) {
			const fieldsets = form.querySelectorAll('fieldset');
			fieldsets.forEach(fieldset =>{
				let fieldsetObject = this.makeFormObject(fieldset);
				formData[fieldset.name] = fieldsetObject;
			});
		}else{
			formData = this.makeFormObject(form);
			if(!formData) isInvalid = true;
		}
		isInvalid ? formData = false : formData;
		return formData;
	}
makeFormObject(elementSet){
	let formData = {};
	let isInvalid = false;
	Array.from(elementSet.elements).forEach(element =>{
    	if (element.type != "submit"){
    		if(element.required && !element.value) isInvalid = true;
	        if(!element.name) isInvalid = true;
	        formData[element.name] = element.value;
	    }
    });
     isInvalid ? formData =  false : formData;
     return formData;
}
}

class Registration{
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
	sendData(data){
		let request = new Requests$1("POST", this.response.bind(this), this.respondedWithError.bind(this)/*,this.showPreloader.bind(this)*/);
		request.dataType = "json";
		console.write(request);
		request.send("/registration/company",data);
	}
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
	displayConfirmation(){
		let modal = document.getElementById("company_success_message");
		modal._show();
	}
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

class EmployeeRegistration{
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
	sendData(data){
		let request = new Requests$1("POST", this.response.bind(this), this.respondedWithError.bind(this),this.showPreloader.bind(this));
		request.send("http://e52cbac.ngrok.io/register/employee",data);
	}
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
	displayConfirmation(){
		let modal = document.getElementById("company_success_message");
		modal._show();
	}
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

class Credential{
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
	collectData(){
		let password = document.getElementById("password").value;
		let username = document.getElementById("username").value;
		this.formData.push(password);
		this.formData.push(username);
	}
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
	sendData(data){
		let request = new Requests$1("POST", this.response.bind(this), this.respondedWithError.bind(this),this.showPreloader.bind(this));
		request.send("http://1a139e3b.ngrok.io/register/user",data);
	}
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
	displayConfirmation(){
		let modal = document.getElementById("user_success_message");
		modal._show();
	}
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

(function(){
	new Filter();
	new SideNav();
	new Login();
	new Registration();
	new EmployeeRegistration();
	new Credential();
	let data = [
			        {"name": "Patrick","age": 26},
			        {"name": "Justin","age": 25},
			        {"name": "Blaise","age": 26},
			        {"name": "Semu","age": 24},
			        {"name": "Diego","age": 26},
			        {"name": "Samuel","age": 26}
			];
	if (document.querySelector('table.table')!=null) {
	new Pagination("paginationTable1","pagination-number1",data,2);
	new Requests('GET', response ).send('/static/scripts/pagination-data.json');
	}
	function response(evt){
		const data = JSON.parse(this.responseText).data;
		new Pagination("paginationTable","pagination-number",data,4);
	}
})();
