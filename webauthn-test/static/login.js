// 1.) Initiate User Login
function initUserAuth() {

    // Format data for server
    var data = {
        username: userLogin.value
    }

    // Print this out to console for now
    console.log("User Data:")
    console.log(data)

    // Contact the server with our info to get credential creation options
    fetch('/initUserAuth', {
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
            getSavedCreds(options);
        }
    })
}

// 2.) Get local credentials
function getSavedCreds(options) {

    // Let's decode some data before we continue...
    options.challenge = bufferDecode(options.challenge)
    if (options.allowCredentials) {
        for (var i = 0; i < options.allowCredentials.length; i++) {
            options.allowCredentials[i].id =
                bufferDecode(options.allowCredentials[i].id)
        }
    }

    // Now that we're in our callback, print our options
    console.log("Credential Auth Options")
    console.log(options)

    // Go ahead and get the creds
    navigator.credentials.get({
        publicKey: options
    })
    .then(creds => {

        // Here they are! Print them out!
        console.log("Credentials")
        console.log(creds)

        // verify assertion
        verifyAssertion(creds)

    })
    .catch((err) => {
        console.info(err);
    })
}

// 3.) Verify Assertion
function verifyAssertion(assertedCred) {

    // Move data into Arrays in case it is super long
    let authData = new Uint8Array(assertedCred.response.authenticatorData);
    let clientDataJSON = new Uint8Array(assertedCred.response.clientDataJSON);
    let rawId = new Uint8Array(assertedCred.rawId);
    let sig = new Uint8Array(assertedCred.response.signature);
    let userHandle = new Uint8Array(assertedCred.response.userHandle);

    // Format body
    const data = {
        id: assertedCred.id,
        rawId: bufferEncode(rawId),
        type: assertedCred.type,
        response: {
            authenticatorData: bufferEncode(authData),
            clientDataJSON: bufferEncode(clientDataJSON),
            signature: bufferEncode(sig),
            userHandle: bufferEncode(userHandle)
        }
    }

    // Post the data
    fetch('/verifyUserAuth', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status == "success"){
            window.location = "/dashboard"
        } else {
            alert("ERROR: " + options.status)
        }
    })
}