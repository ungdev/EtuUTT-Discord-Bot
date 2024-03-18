const checkbox = document.querySelector("#check_GDPR");
const submit = document.querySelector("#submit_button");
const admin = document.querySelector("#admin");
const admin_mention = document.querySelector("#admin_mention");

if (checkbox && submit) {
    if (!checkbox.checked) submit.setAttribute("disabled", "true");

    checkbox.addEventListener("change", () => {
        if (checkbox.checked) {
            submit.removeAttribute("disabled");
        } else {
            submit.setAttribute("disabled", "true");
        }
    });
}

if (admin) {
    admin.addEventListener("click",
        () => navigator.clipboard.writeText(admin_mention.textContent));
}
