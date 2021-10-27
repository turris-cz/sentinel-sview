async function request_data(passwordHash) {
    const res = await fetch('http://' + server + ':' + port + '/api/leaked/',
        {
            mode: 'no-cors',
            method: 'post',
            headers: {
            'Accept': 'application/json, text/json',
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({"msg_type": "request", "hash": passwordHash.toString().slice(0,6)})
        });//.then(res => {return res.json();}).then(res => console.log(res)).catch(error=> {console.log(error)});
    return await res.json();
}

async function post() {
    const password = document.getElementById("password");
    const hexdigest = await digestMessage(password.value);
    const header = document.getElementById("header");
    header.textContent = hexdigest;
    const data = await request_data(hexdigest);
    console.log(data); 
}

async function digestMessage(message) {
    console.log(message)
    const msgUint8 = new TextEncoder().encode(message);                           // encode as (utf-8) Uint8Array
    const hashBuffer = await crypto.subtle.digest('SHA-1', msgUint8);           // hash the message
    const hashArray = Array.from(new Uint8Array(hashBuffer));                     // convert buffer to byte array
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // convert bytes to hex string
    return hashHex;
  }
