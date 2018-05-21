export default class Filter{
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