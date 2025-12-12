async function apiRequest(endpoint, method, data = null) {

    let url = "/projects/meeting_notes_bot/api/" + endpoint;

    const params = {
        method: method
    };

    if (data) {
        switch (method.toUpperCase()) {
            case "POST":
            case "PUT":
            case "PATCH":
                if (data instanceof FormData) {
                    // Upload form data directly
                    params.body = data;
                } else {
                    // Convert js object to JSON string
                    params.body = JSON.stringify(data);
                    params.headers = { 'Content-Type': 'application/json' };
                }
                break;
            case "GET":
            case "DELETE":
                const queryString = new URLSearchParams(data).toString();
                if (queryString) url += "?" + queryString;
                break;
            default:
                throw new Error("Unsupported HTTP method: " + method);
        }
    }

    const response = await fetch(url, params);

    if(!response.ok)
        console.error("HTTP error", response.status);

    const responseData = await response.json();

    if (responseData.success === false)
        throw new Error(responseData.data);

    return responseData.data;
}