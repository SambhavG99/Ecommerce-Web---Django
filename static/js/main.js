function getCookie(name) {
    let cookieArr = document.cookie.split(";");
    for (let index = 0; index < cookieArr.length; index++) {
        let cookieName = cookieArr[index].split("=");
        if(cookieName[0].trim() == name){
            return decodeURIComponent(cookieName[1])
        }
    }
    return null;
}

let cart = JSON.parse(getCookie('cart'));
if(!cart){
    cart = {};
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    console.log("Cookie created");
}
console.log("Cart",cart);


function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getToken('csrftoken');

let updateBtns = document.getElementsByClassName('update-cart');
for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log(`productId:${productId},Action:${action}`)
        if(user == "AnonymousUser"){
            addCookieItem(productId,action);
        }else {
            updateOrderItem(productId,action);
        }
    })
}

function addCookieItem(productId,action){
    if(action == "add"){
        if(!cart[productId]){
            cart[productId] = {"quantity" : 1}
        }else{
            cart[productId]['quantity'] += 1; 
        }
    }
    if(action == "remove"){
        cart[productId]['quantity'] -= 1;
        if(cart[productId]['quantity'] <= 0){
            delete cart[productId];
            console.log("Deleting Cookies");
        }
    }

    if(action == "delete"){
        delete cart[productId];
    }
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()
}

function updateOrderItem(productId,action){
    console.log("Sending Data...");
    url = "/updatecart/";
    fetch(url, {
        method:"POST",
        headers: {
            "Content-Type":"application/json",
            "X-CSRFTOKEN":csrftoken
        },
        body:JSON.stringify({"productId":productId,"action":action}),
    }    
    )
    .then((response) => {
        console.log(response);
        return response.json();
    })
    .then((data)=> {
        console.log(data);
        location.reload();    
    })
}

let viewBtn = document.getElementsByClassName('view-btn');
for (let index = 0; index < viewBtn.length; index++) {
        viewBtn[index].addEventListener('click', function(){
            let prod_id = this.dataset.productid;
            // console.log(prod_id);
            let hostname = window.location.hostname;
            if(hostname == "localhost"){
                location.href = `http://${hostname}:8000/product/?id=${prod_id}`;
            } else {
                location.href = `http://${hostname}/product/?id=${prod_id}`;
            }
        })
    
}
