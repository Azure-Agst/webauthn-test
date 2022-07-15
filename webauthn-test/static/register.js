// 1.) Initiate User Registration 
function initUserReg() {

    if (emailInput.value == "" || userInput.value == ""){
        alert("Username + Email must both be populated!")
        return
    }

    // Format data for server
    var data = {
        email: emailInput.value,
        username: userInput.value
    }

    // Print this out to console for now
    console.log("User Data:")
    console.log(data)

    // Contact the server with our info to get credential creation options
    fetch('/initUserReg', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then((options) => {
        if (options.status){
            alert("ERROR: " + options.status)
        } else {
            genPubKey(options);
        }
    })
}

// 2.) Generate Public Key
function genPubKey(options) {

    // Let's decode some data before we continue...
    options.challenge = bufferDecode(options.challenge)
    options.user.id = bufferDecode(options.user.id)
    if (options.excludeCredentials) {
        for (var i = 0; i < options.excludeCredentials.length; i++) {
            options.excludeCredentials[i].id =
                bufferDecode(options.excludeCredentials[i].id)
        }
    }

    // Now that we're in our callback, print our options
    console.log("Credential Creation Options")
    console.log(options)

    // Go ahead and make our credentials
    navigator.credentials.create({
        publicKey: options
    })
    .then((newCreds) => {

        // Here they are! Print them out!
        console.log("New Credentials")
        console.log(newCreds)

        // Now let's register these!
        registerCreds(newCreds)

    })
    .catch((err) => {
        console.info(err);
    })
}

// 3.) Register Creds with Server
function registerCreds(newCreds) {

    // Move data into Arrays in case it is super long
    let attestationObject = new Uint8Array(newCreds.response.attestationObject);
    let clientDataJSON = new Uint8Array(newCreds.response.clientDataJSON);
    let rawId = new Uint8Array(newCreds.rawId);

    // Format body
    const data = {
        id: newCreds.id,
        rawId: bufferEncode(rawId),
        type: newCreds.type,
        response: {
            attestationObject: bufferEncode(attestationObject),
            clientDataJSON: bufferEncode(clientDataJSON)
        }
    }

    // Post the data
    fetch('/verifyUserReg', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status == "success") {
            alert("You are now registered! Try logging in!")
        }
    })
}