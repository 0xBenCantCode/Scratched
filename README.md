# Scratched
One-click itch.io account takeover via XSS and Oauth.

## Details
The markdown editor within itch.io was vulnerable to XSS in edit mode. When a user accepts an admin invite to a project, they are automatically redirected to the project's home page in edit mode. We can abuse this and embed a malicious script in our games description that makes a request to the attackers GitHub Oauth callback url and effectively links the victims itch.io account to the attackers GitHub account.

> Attacker creates malicious project -> Sends admin invite to victim -> victim accepts (one-click) -> payload executes -> Attacker GitHub account linked to victim account.
## Demo
