import secrets
from flask import Blueprint, request, session
from webauthn import generate_authentication_options, \
    verify_authentication_response, options_to_json
from webauthn.helpers.structs import \
    AuthenticationCredential, PublicKeyCredentialDescriptor

from ..static import static
from ..db import get_user_data

# create login blueprint
login = Blueprint(
    "login", __name__, 
    template_folder="templates", 
    static_folder="static"
)

@login.route("/initUserAuth", methods=['POST'])
def initUserAuth():
    
        # Print separator
        print("\n=======================\n")
    
        # See if user even exists
        session['login_user'] = request.json['username']
        user_data = get_user_data(session['login_user'])
        if user_data is None:
            return {"status": f"User '{session['login_user']}' doesn't exist"}, 400
    
        # Generate a challenge
        # see notes in register.py
        static.challenge = secrets.token_bytes(32)
    
        # Generate the registration options
        print("Using credential id:")
        print(static.credential_id)
        auth_options = generate_authentication_options(
            rp_id="localhost",
            challenge=static.challenge,
            allow_credentials=[
                PublicKeyCredentialDescriptor(
                    id=user_data['credential_id'],
                )
            ]
        )
    
        # Print this, for debugging later
        print("Auth Options:")
        print(options_to_json(auth_options))
    
        # Return the registration options to the client
        return options_to_json(auth_options)

@login.route("/verifyUserAuth", methods=['POST'])
def verifyUserAuth():

    # Get JSON from client, but don't deserialize it yet
    body = request.get_data(as_text=True)

    # Get database data again
    user_data = get_user_data(session['login_user'])
    
    # Verify Registration
    try:
        verif = verify_authentication_response(
            credential=AuthenticationCredential.parse_raw(body),
            expected_challenge=static.challenge,
            credential_public_key=user_data['credential_public_key'],
            expected_origin="http://localhost:5000",
            expected_rp_id="localhost",
            credential_current_sign_count=0,
            require_user_verification=True,
        )

    # catch any errors
    except Exception as e:
        return {"status": str(e)}, 500

    # Print this, for debugging later
    print("Registration Verification:")
    print(verif.json(indent=2))

    # clear these session vars
    del session['login_user']

    # set these others
    session['username'] = user_data['username']
    session['email'] = user_data['email']

    # Return success
    return {"status": "success"}