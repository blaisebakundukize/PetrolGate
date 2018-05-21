export default class Modal extends HTMLElement{

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




