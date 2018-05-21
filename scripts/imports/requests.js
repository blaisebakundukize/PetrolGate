/**
 * @name REQUEST
 * @author BAHATI JUSTIN
 * @description THIS CLASS MAKES AJAX REQUEST ALLOWED REQUESTS METHODS: GET, POST, PUT and DELETE
 * */
export default class Requests {
    /**
     * 
     * @param {string} method DEFAULT{GET}: this defines the request method
     * @param {CALLBACK FUNCTION} onload CALLBACK FUNCTION. This is called when the request completes with success
     * @param {CALLBACK FUNCTION} onprogress CALLBACK FUNCTION. This is called when the request is in progress
     * @param {CALLBACK FUNCTION} onerror CALLBACK FUNCTION. This is called when the request completes with error
     */
    constructor (method='GET', onload=function(){}, onerror = function(){}, onprogress = function(){}) {

        this.METHODS = ['GET', 'POST', 'PUT', 'DELETE'];
        this.dataType = "form";
        this.method = method;
        this.request = new XMLHttpRequest();
        this.onload = onload;
        this.onprogress = onprogress;
        this.onerror = onerror;
    }

    /**
     * @param {string} url
     * @param {JSON} data
     */

    send(url=null, data = {} ){
        if(!url) return;
        const encodedData = this.urlEncodedData(data);
        this.url = `${url}?${encodedData}`;
        this.body = null;

        /** TEST IF THE REQUEST METHODS ARE ALLOWED OTHER WISE IT CANCELS THE REQUEST */
        if(!this.METHODS.includes(this.method.toUpperCase())){
            console.warn("Invalid request method:", this.method);
            
            return;
        }
        
        
        /** IF THE REQUEST METHOD IS NOT 'GET' OR DELETE, WE NEED TO  */
        if ( this.method.toUpperCase() != 'GET' && this.method.toUpperCase() != 'DELETE') {
            this.url = url;            
            this.body = this.urlEncodedData(data);            
            this.request.open(this.method, this.url, true);     
            this.request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

            // this.request.setRequestHeader('Content-Type', 'application/json');
            console.log("Datat type", this.dataType);
            if (this.dataType.toUpperCase() === "JSON") {
                this.body = JSON.stringify(data);
               /* console.log('is json data');*/
            }
            /*console.log('Posted as:', this.body);
            */
        }else{
            


            this.request.open(this.method, this.url, true);
        }
        // SETTING CALLBACK METHODS
        this.request.onload = this.onload;  
        this.request.onprogress = this.onprogress;
        this.request.onerror = this.onerror;  
        // console.log('body',this.body);
        this.request.send(this.body);
    }
    /**
     * encodes data to be sent
     * @param {JSON} data Datat to send to server
     */
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

/* Usage ....
request = new Request('DELETE', response, loading, error )
request.send('url',{})

function response(evt){
    console.log(this.responseText);    
}
function loading(evt){
    console.log(evt);    
}
function error(evt){
    console.log(evt);    
}
*/
