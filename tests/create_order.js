fetch("http://127.0.0.1:8000/order/pedido", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1NTg4NDkzfQ.qI8Z_IzZlYhr1mPzYJOdZiH0iOT9bF1BGEG3plBZeUI"
  }
  
})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err))