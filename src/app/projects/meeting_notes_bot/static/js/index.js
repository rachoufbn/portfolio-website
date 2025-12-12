window.addEventListener('load', () => {

    const meetingsTablePlaceholder = document.getElementById('meetingsTablePlaceholder');
    const meetingsTableBody = document.getElementById('meetingsTableBody');
    const uploadMeetingForm = document.getElementById('uploadMeetingForm');

    // Set default meeting date to now
    document.getElementById('meetingDateTime').value = toLocalISOString(new Date());

    // Initialize search bar
    new SearchBar(
        document.getElementById('meetingSearch'),
        meetingsTableBody
    );

    // Handle delete meeting button clicks
    document.querySelectorAll('.deleteMeetingButton').forEach(button => {
        button.addEventListener('click', async function(event) {

            this.disabled = true;

            const meetingId = this.getAttribute('data-meeting-id');
            const meetingTitle = this.getAttribute('data-meeting-title');
            const success = await deleteMeeting(meetingId, meetingTitle);
            
            if(success){

                this.closest('tr').remove();

                if(meetingsTableBody.children.length === 0)
                    meetingsTablePlaceholder.classList.remove('d-none');

            } else {
                this.disabled = false;
            }

        });
    });

    // Handle upload meeting form submission
    uploadMeetingForm.addEventListener('submit', async function(e){
        e.preventDefault();

        const uploadMeetingResponseElement = document.getElementById('uploadMeetingResponse');
        const submitButton = uploadMeetingForm.querySelector('button[type="submit"]');

        submitButton.disabled = true;
        uploadMeetingResponseElement.classList.add('d-none');

        try {
            
            const data = await apiRequest('meetings', 'POST', new FormData(this));
            window.location.href = getMeetingLink(data.id);

        } catch (error) {
            uploadMeetingResponseElement.textContent = error.message;
            uploadMeetingResponseElement.classList.remove('d-none')
            submitButton.disabled = false;
        }        

    });

    async function deleteMeeting(meetingId, meetingTitle) {

        if (confirm(`Are you sure you want to delete the meeting "${meetingTitle}"?`)) {

            try {
                await apiRequest(`meetings/${meetingId}`, 'DELETE');
                return true;
            } catch (error) {
                alert("Failed to delete meeting: " + error.message);
                return false;
            }

        }
        
    }

    function toLocalISOString(date) {
        const timeZoneOffset = date.getTimezoneOffset() * 60000;
        const localDate = new Date(date - timeZoneOffset);
        const localISOString = localDate.toISOString().slice(0, 16);
        return localISOString;
    }

    function getMeetingLink(meetingId) {
        return `/projects/meeting_notes_bot/meetings/${meetingId}`;
    }

});