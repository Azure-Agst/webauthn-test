// Utility Functions
// FROM: https://webauthn.io/dist/js/webauthn.js

function bufferEncode(value) {
    return base64js.fromByteArray(value)
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=/g, "");
}

function bufferDecode(value) {
    var padding = 4 - (value.length % 4)
    for (var i = 0; i < padding; i++){
        value += "="
    }
    return base64js.toByteArray(value)
}

// Constants
const registerForm = document.getElementById("registerForm");
const loginForm = document.getElementById("loginForm");
const emailInput = document.getElementById("emailInput");
const userInput = document.getElementById("userInput");
const userLogin = document.getElementById("userLogin");

// Event Listeners
registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    await initUserReg();
});
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    await initUserAuth();
});