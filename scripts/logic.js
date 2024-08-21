document.getElementById('scanBtn').addEventListener('click', async function () {
    const url = document.getElementById('url').value;

    try {
        const response = await fetch(`/get_data?url=${encodeURIComponent(url)}`);
        const data = await response.json();

        // Update the cookies list
        const cookiesList = document.getElementById('cookiesList');
        cookiesList.innerHTML = ''; // Clear any existing list items

        data.forEach(cookie => {
            const listItem = document.createElement('li');
            listItem.textContent = `${cookie.name}: Secure=${cookie.secure}, HttpOnly=${cookie.httponly}, SameSite=${cookie.samesite_value}, Expiration=${cookie.expiration_value}`;
            cookiesList.appendChild(listItem);
        });

        // Optionally update the compliance score or other elements
        document.getElementById('complianceScore').textContent = `Compliance Score: ${calculateComplianceScore(data)}/100`;

    } catch (error) {
        console.error('Error fetching data:', error);
    }
});

function calculateComplianceScore(data) {
    // Placeholder för att ha poäng att räkna med
    let score = 100;
    data.forEach(cookie => {
        if (!cookie.secure || !cookie.httponly || cookie.samesite === 'bad' || cookie.expiration === 'bad') {
            score -= 10;  // Deduct points for each non-compliant cookie
        }
    });
    return score;
}