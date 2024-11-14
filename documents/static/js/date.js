document.addEventListener("DOMContentLoaded", function() {
    const dateInputs = document.querySelectorAll('input[type="text"][id$="_date"]');

    dateInputs.forEach(dateInput => {
        dateInput.addEventListener('blur', function() {
            const value = dateInput.value.trim();
            if (value) {
                const parts = value.split('-');
                if (parts.length === 3) {
                    const day = parts[0].padStart(2, '0'); // Ensure two digits
                    const month = parts[1].padStart(2, '0'); // Ensure two digits
                    const year = parts[2]; // Assume it's a four-digit year

                    // Set the new value in yyyy-mm-dd format
                    dateInput.value = `${year}-${month}-${day}`;
                } else {
                    // Handle invalid input
                    alert("Please enter the date in DD-MM-YYYY format.");
                }
            }
        });
    });
});
