export default class SearchCompany{
	constructor(){
	    this.addEventListeners();
	}
	search(evt){
		this.data = ["Justin","Juslin","Patrick","Blaise","Diego","Semu"];
		this.searchContent = document.querySelector("#company_search_content");
		let search = document.getElementsByClassName("form-element--search")[0].value;
	    let searchUpperCase = search.toUpperCase();
	    if (this.searchContent.style.display = "none") {
	    	this.searchContent.style.display = "block";
	    	this.searchContent.innerHTML = "";
	    	for (let i = 0; i < this.data.length; i++) {
	    		if (this.data[i].toUpperCase().indexOf(searchUpperCase) > -1) {
	    			let p = document.createElement("p");
		            p.classList.add("company_search_content__p");
		            p.innerHTML = this.data[i];
		            this.searchContent.appendChild(p);
	    		}
	    	}
	    	if (this.searchContent.children.length == 0) {
	    		let p = document.createElement("p");
		        p.classList.add("company_search_content__p");
		        p.innerHTML = "No Company found";
		        this.searchContent.appendChild(p);
	    	}
	    	if (search == "") {
	    		let arrow = document.querySelector("#arrow-right");
		        let companyName = document.querySelector("#company-name");
	    		this.searchContent.style.display = "none";
	    		arrow.style.display = "none";
		        companyName.style.display = "none";

	    	}
	    }
	}
	getSelectedCompany(e){
		let arrow = document.querySelector("#arrow-right");
		let companyName = document.querySelector("#company-name");
		this.searchContent = document.querySelector("#company_search_content");
		this.searchInput = document.querySelector("#form-element--search");
		this.searchInput.value = e.target.innerHTML;
		this.searchContent.style.display = "none";
		arrow.style.display = "block";
		companyName.style.display = "block";
		this.selectedCompany = document.querySelector("#company-name__span");
		this.selectedCompany.innerHTML = e.target.innerHTML;
	}
	addEventListeners(){
		this.searchInput = document.querySelector("#form-element--search");
		this.searchContent = document.querySelector("#company_search_content");
		this.searchInput.addEventListener("keyup",this.search);
		this.searchContent.addEventListener("click",this.getSelectedCompany);
	}
}