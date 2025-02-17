# Scratched  

### One-Click itch.io Account Takeover via XSS and OAuth  

## Details  

The markdown editor within itch.io was vulnerable to **XSS in edit mode**.  
When a user accepts an **admin invite** to a project, they are automatically redirected to the project's home page in **edit mode**.  

This vulnerability allowed an attacker to embed a **malicious script** in the game’s description, which would make a request to the attacker's **GitHub OAuth callback URL**—effectively linking the victim's itch.io account to the attacker's GitHub account.  

### Exploit Flow  

1. **Attacker creates a malicious project**  
2. **Sends an admin invite to the victim**  
3. **Victim accepts (one-click takeover)**  
4. **Payload executes automatically**  
5. **Attacker's GitHub account is linked to the victim's itch.io account**  

## Demo  

[![Exploit Demo](https://github.com/user-attachments/assets/99b2f9ff-be44-4d2a-80e4-ad0f96c3722c)](https://github.com/user-attachments/assets/99b2f9ff-be44-4d2a-80e4-ad0f96c3722c)  

---

**Disclaimer:** Bug has been patched and itch.io agreed to public disclosure
