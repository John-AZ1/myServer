let submitBtn = document.getElementById("submit")
let usernameInp = document.getElementById("username")
let passwordInp = document.getElementById("password")

function login(username, password) {
  const request = new XMLHttpRequest()
  request.open('PUSH', '/mySimon/api/login', true)
  request.setRequestHeader('Content-type', 'application/json')
  request.send('{"Username": "'+username+'", "Password": "'+password+'"}');
  request.onreadystatechange = e => {
    console.log("Logged in!!")
  }
}


submitBtn.addEventListener('click', e => {
  let username = usernameInp.value
  let password = passwordInp.value

  login(username, password)
})
