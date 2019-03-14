let submitBtn = document.getElementById("submit")
let usernameInp = document.getElementById("username")
let passwordInp = document.getElementById("password")

let count = 0

function login(username, password) {
  count ++;
  console.log(count)
  const request = new XMLHttpRequest()
  request.open('POST', '/mySimon/api/login', true)
  request.setRequestHeader('Content-type', 'application/json')
  request.send('{"Username": "'+username+'", "Password": "675Jv@%BdR3,:sd"}');
  // request.send('{"Username": "'+username+'", "Password": "'+password+'"}');
	request.onreadystatechange = e => {
    if(request.responseText == "LOGGED IN") {
      getTimeTableHTML()
    }
	}
}

function getTimeTableHTML() {
  const requests = new XMLHttpRequest()
  requests.open('PUSH', '/mySimon/api/getTimeTableHTML', true)
  requests.setRequestHeader('Content-type', 'application/json')
  requests.send();
	requests.onreadystatechange = e => {
		console.log(requests.response);
	}
}

submitBtn.addEventListener('click', e => {
  let username = usernameInp.value
  let password = passwordInp.value

  login(username, password)
})
