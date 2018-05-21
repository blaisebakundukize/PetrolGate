 
export default class GetFormData{
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
