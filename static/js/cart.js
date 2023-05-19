function updateOrder(id, action) {
  fetch('/update_item/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
      'productId': id,
      'action': action
    })
  })
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if(data.item_quantity <= 0){
      let del = document.getElementById(`item-${id}`);
      del.remove();
    }
    document.querySelector("#cart-total").innerHTML = data.total_items;
    document.querySelector(`#item-${id}-quantity`).innerHTML = data.item_quantity;
    document.querySelector(`#item-${id}-total`).innerHTML = "$"+data.total_items_price;
    document.querySelector(`#order-total`).innerHTML = "Total: $"+data.order_total;
  })
}

function addCookieItem(productId, action) {
  if(action === 'add'){
    if(cart[productId] === undefined){
      cart[productId] = {'quantity': 1};
    }else{
      cart[productId].quantity += 1;
    }
  }else{
    cart[productId].quantity -= 1;
    if(cart[productId].quantity<=0){
      delete cart[productId];
    }
  }
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

document.querySelectorAll('.update-cart').forEach(button => {
  button.onclick = function() {
    if(user === 'AnonymousUser'){
      addCookieItem(this.dataset.product, this.dataset.action);
    }else{
      updateOrder(this.dataset.product, this.dataset.action);
    }
  }
})