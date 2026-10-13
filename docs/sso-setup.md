# Acme Cloud — SSO Setup (Enterprise)

## Supported protocols

Acme Cloud supports **SAML 2.0** and **OpenID Connect** for single sign-on.

## Setup steps

1. In the admin console, go to Settings > Security > Single Sign-On.
2. Upload your identity provider's metadata XML (SAML) or enter the discovery URL (OIDC).
3. Map the `email` and `name` attributes. Group membership can be mapped from the `groups` claim.
4. Click **Test connection** before enforcing SSO for all users.

## Enforcing SSO

Once the test succeeds, toggle **Require SSO for all users**. Password logins
are disabled for all users except designated break-glass admin accounts.

## Troubleshooting

- **"Invalid signature"**: check that the IdP certificate has not expired.
- **"User not provisioned"**: enable Just-In-Time provisioning, or pre-create the user via SCIM.
