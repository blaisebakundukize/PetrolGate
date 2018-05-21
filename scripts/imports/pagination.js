/**
 * @name Pagination
 * @description this class takes data formatted json and builds a table with pagination
 * */
export default class Pagination{
	
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
				a.setAttributeNode(attributeId)
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