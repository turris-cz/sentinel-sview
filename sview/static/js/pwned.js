function request_data(passwordHash) {
    fetch('http://' + server + ':' + port + '/api/leaked/',
        {
            mode: 'no-cors',
            method: 'post',
            headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': true
            },
            body: JSON.stringify({"msg_type": "request", "hash": passwordHash.toString().slice(0,6)})
        }
    ).then(response => console.log(response));
}

async function post() {
    let password = document.getElementById("password");
    let hexdigest = await digestMessage(password.value);
    let header = document.getElementById("header");
    header.textContent = hexdigest;
    request_data(hexdigest);
}

async function digestMessage(message) {
    console.log(message)
    const msgUint8 = new TextEncoder().encode(message);                           // encode as (utf-8) Uint8Array
    const hashBuffer = await crypto.subtle.digest('SHA-1', msgUint8);           // hash the message
    const hashArray = Array.from(new Uint8Array(hashBuffer));                     // convert buffer to byte array
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // convert bytes to hex string
    return hashHex;
  }
