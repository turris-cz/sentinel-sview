async function request_data(passwordHash) {
    const res = await fetch('http://' + server + ':' + port + '/api/leaked/',
        {
            mode: 'no-cors',
            method: 'post',
            headers: {
            'Accept': 'application/json, text/json',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': true
            },
            body: JSON.stringify({"msg_type": "request", "hash": passwordHash.toString().slice(0,6)})
        }
    );
    const data = await res.json();
    console.log(data)
    //.then(response => {console.log(response);})//.then(response => console.log(response)).catch(error=> {console.log(error)});
}

async function post() {
    let password = document.getElementById("password");
    let hexdigest = await digestMessage(password.value);
    let header = document.getElementById("header");
    header.textContent = hexdigest;
    await request_data(hexdigest);
}

async function digestMessage(message) {
    console.log(message)
    const msgUint8 = new TextEncoder().encode(message);                           // encode as (utf-8) Uint8Array
    const hashBuffer = await crypto.subtle.digest('SHA-1', msgUint8);           // hash the message
    const hashArray = Array.from(new Uint8Array(hashBuffer));                     // convert buffer to byte array
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // convert bytes to hex string
    return hashHex;
  }
