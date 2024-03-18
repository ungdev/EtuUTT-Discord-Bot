const checkbox = document.querySelector("#check-GDPR");
const submit = document.querySelector("#submit-button");
const admin = document.querySelector("#admin");
const adminMention = document.querySelector("#admin-mention");

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
        () => navigator.clipboard.writeText(adminMention.textContent));
}
