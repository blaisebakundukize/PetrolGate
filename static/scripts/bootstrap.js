/*!
 * Build: 2018-04-04T18:57:11.973Z
 */
class Modal extends HTMLElement{
    createdCallback(){
        this._hide = this._hide.bind(this);
        this.KEYS = {
            ESC: 27
        };
    }
    attachedCallback(){
        this._setTitle();
        this._addEventListeners();
        this.tabIndex = '1';
    }
    _show(){
        this.previousActiviveEl = document.activeElement;
        this.setAttribute('visible', true);
        console.log(this.previousActiviveEl);
        this.focus();
        console.log(document.activeElement);
    }
    _hide(){
        this.setAttribute('visible', false);
        this.previousActiviveEl.focus();
    }
    _addEventListeners(){
        this.closeButton = this.querySelector('.modal-header-close');
        this.closeButton.addEventListener('click', this._hide);
        this.addEventListener('keydown', this._onKeyDown);
    }
    _onKeyDown(evt){
        if(evt.keyCode == this.KEYS.ESC) this._hide();
        console.log('this:',this);
        console.log('evt:', document.activeElement);
    }
    _setTitle(){
        let modalHeaderEl = this.createModalHeader();
        let modalContentsEl = this.querySelector('rs-modal-contents');
        if(!modalContentsEl) return;
        modalContentsEl.insertBefore(modalHeaderEl, modalContentsEl.firstElementChild);
    }
    createModalHeader(){
        let titleEl = document.createElement('h1');
        titleEl.classList.add('modal-header-title');
        titleEl.textContent = this.getAttribute('title');
        let closeButtonEl = document.createElement('button');
        closeButtonEl.classList.add('modal-header-close');
        closeButtonEl.innerHTML = "&times;";
        let modalHeaderEl = document.createElement('rs-modal-header');
        modalHeaderEl.appendChild(titleEl);
        modalHeaderEl.appendChild(closeButtonEl);
        return modalHeaderEl;
    }
}

(function(){
	const button = document.querySelector('#button');
	button.addEventListener('click', function(){
	    document.querySelector('rs-modal')._show();
	});
	document.registerElement("rs-modal", Modal);
})();
