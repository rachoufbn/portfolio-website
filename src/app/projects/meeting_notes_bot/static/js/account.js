window.addEventListener('load', () => {

    const logoutBtn = document.getElementById('logoutBtn');
    const saveAccountBtn = document.getElementById('saveAccountBtn');

    function disableButtons(){
        logoutBtn.disabled = true;
        saveAccountBtn.disabled = true;
    }

    function enableButtons(){
        logoutBtn.disabled = false;
        saveAccountBtn.disabled = false;
    }

    logoutBtn.addEventListener('click', async function() {
        await logout();
    });

    saveAccountBtn.addEventListener('click', async function() {
        await saveAccountDetails();
    });

    async function logout() {

        disableButtons();

        try{
            await apiRequest('auth/logout', 'POST');
            window.location.href = '/projects/meeting_notes_bot/login';
        } catch (error) {
            alert("Log out failed: " + error.message);
            enableButtons();
        }

    }

    async function saveAccountDetails() {

        const accountForm = document.getElementById('accountForm');

        if (!accountForm.reportValidity())
            return;

        disableButtons();

        try {

            const userData = await apiRequest(
                "auth/me",
                "PATCH",
                new FormData(accountForm)
            );

            document.getElementById('accountButtonText').textContent = userData.name;

            showAccountMessage('Details updated successfully!', 'success');

        } catch (error) {
            showAccountMessage(error.message, 'danger', 20000);
        }

        enableButtons();

    }

    function showAccountMessage(message, type, timeout = 5000) {
        const messageElement = document.getElementById('accountMessage');
        messageElement.textContent = message;
        messageElement.className = `alert alert-${type}`;
        messageElement.classList.remove('d-none');
        
        setTimeout(() => {
            messageElement.classList.add('d-none');
        }, timeout);
    }

});