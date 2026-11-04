# Retain the deployed encrypted-output include compatibility fix

Desktop clients request `output.encrypted_content`. The deployed machine had
already accepted this value, but the maintained wheel rejected it before
reaching account recovery. Preserve that compatibility in the fork without
changing unknown-value rejection or the requested response content.
