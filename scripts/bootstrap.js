import Modal from "./imports/modal";
import Modaltest from "./imports/modal-test";
import SideNav from "./imports/side-nav";
import Filter from "./imports/filters";
import Login from "./imports/login-partial";
import Pagination from "./imports/pagination";
import Registration from "./imports/company-registration-partial";
import EmployeeRegistration from "./imports/employee-registration-partial";
import SearchCompany from "./imports/search_company";
import Credential from "./imports/user_credential_partial";


(function(){
	new Filter();
	new SideNav();
	new Login();
	new Registration();
	new EmployeeRegistration();
	new Credential();
	/*new Modaltest(); */
	// const searchCompany = 
	/*new SearchCompany();*/
	/*document.registerElement("rs-modal", Modal);*/
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
