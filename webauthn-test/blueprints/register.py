import secrets
from flask import Blueprint, request, session
from webauthn import generate_registration_options, \
    verify_registration_response, options_to_json, \
    base64url_to_bytes
from webauthn.helpers import parse_attestation_object, parse_client_data_json
from webauthn.helpers.structs import RegistrationCredential

from ..static import static
from ..db import make_new_user, get_user_data

# create register blueprint
register = Blueprint(
    "register", __name__, 
    template_folder="templates", 
    static_folder="static"
)

@register.route("/initUserReg", methods=['POST'])
def initUserReg():

    # Print separator
    print("\n=======================\n")

    # Get the form data from the client
    session['newUser_email'] = request.json['email']
    session['newUser_username'] = request.json['username']

    # see if user already exists
    user_data = get_user_data(session['newUser_username'])
    if user_data is not None:
        return {"status": f"User '{session['newUser_username']}' already exists"}, 400

    # generate a challenge
    # this would normally be handled by a DB or other storage mechanism
    # also important to note that js's base64url encoding panics in many cases
    # so i just encode a random hex string instead of random bytes
    static.challenge = secrets.token_bytes(32)

    # Generate the registration options
    reg_options = generate_registration_options(
        rp_id="localhost",
        rp_name="Localhost LLC",
        user_id=session['newUser_email'],
        user_name=session['newUser_username'],
        challenge=static.challenge,
    )

    # Print this, for debugging later
    print("Registration Options:")
    print(options_to_json(reg_options))

    # Return the registration options to the client
    return options_to_json(reg_options)

@register.route("/verifyUserReg", methods=['POST'])
def verifyUserReg():

    # Get JSON from client, but don't deserialize it yet
    body = request.get_data(as_text=True)
    
    # Verify Registration
    try:
        verif = verify_registration_response(
            credential=RegistrationCredential.parse_raw(body),
            expected_challenge=static.challenge,
            expected_origin="http://localhost:5000",
            expected_rp_id="localhost",
            require_user_verification=True,
        )

    # Catch any errors
    except Exception as e:
        return {"status": str(e)}, 500

    # By this point we can comfirm that the user was registered
    # Now we save their data for next time

    # Get credential id and public key from the response
    dec_attest = parse_attestation_object(verif.attestation_object)
    att_data = dec_attest.auth_data.attested_credential_data

    # Insert user into the database
    try:
        make_new_user(
            session['newUser_username'],
            session['newUser_email'],
            att_data.credential_id,
            att_data.credential_public_key
        )

    # Catch any errors
    except Exception as e:
        return {"status": str(e)}, 500

    # clear these session vars
    del session['newUser_email']
    del session['newUser_username']

    # Return success
    return {"status": "success"}
