document.addEventListener("DOMContentLoaded", function() {
    const dateInputs = document.querySelectorAll('input[type="text"][id$="_date"]');

    dateInputs.forEach(dateInput => {
        dateInput.addEventListener('input', function() {
            let value = dateInput.value.replace(/[^0-9]/g, ''); // Remove non-numeric characters
            
            // Automatically add dashes after day (2 digits) and month (2 digits)
            if (value.length > 0) {
                // Add dash after day
                if (value.length >= 2) {
                    value = value.slice(0, 2) + '-' + value.slice(2);
                }
                // Add dash after month
                if (value.length >= 5) {
                    value = value.slice(0, 5) + '-' + value.slice(5);
                }
                dateInput.value = value; // Set the formatted value
            }
        });

        dateInput.addEventListener('input', function() {
            const value = dateInput.value.trim();
            const parts = value.split('-');
            const dayPart = parts[0] || '';
            const monthPart = parts[1] || '';
            const yearPart = parts[2] || '';

            let isValid = true;

            // Day validation
            if (dayPart.length > 2 || (dayPart.length === 2 && parseInt(dayPart, 10) > 31)) {
                isValid = false;
                dateInput.style.borderColor = 'red'; // Change border color to red
                dateInput.value = dayPart.slice(0, 1); // Keep only the first digit
            } else if (dayPart.length === 2 && parseInt(dayPart, 10) <= 31) {
                dateInput.style.borderColor = ''; // Reset border color
                if (monthPart.length === 0) {
                    // Move to month if day is valid
                    dateInput.value = dayPart + '-';
                }
            }

            // Month validation
            if (monthPart.length > 2 || (monthPart.length === 2 && parseInt(monthPart, 10) > 12)) {
                isValid = false;
                dateInput.style.borderColor = 'red'; // Change border color to red
                dateInput.value = dayPart + '-'; // Keep day only
            } else if (monthPart.length === 2 && parseInt(monthPart, 10) <= 12) {
                dateInput.style.borderColor = ''; // Reset border color
                if (yearPart.length === 0) {
                    // Move to year if month is valid
                    dateInput.value = dayPart + '-' + monthPart + '-';
                }
            }

            // Year validation
            if (yearPart.length > 4 || (yearPart.length === 4 && (parseInt(yearPart, 10) < 1950 || parseInt(yearPart, 10) > new Date().getFullYear()))) {
                isValid = false;
                dateInput.style.borderColor = 'red'; // Change border color to red
            } else {
                dateInput.style.borderColor = ''; // Reset border color
            }
        });

        dateInput.addEventListener('focus', function() {
            const currentValue = dateInput.value;
            if (currentValue) {
                const parts = currentValue.split('-');
                if (parts.length === 3) {
                    const day = parts[0];
                    const month = parts[1];
                    const year = parts[2];
                    dateInput.value = `${day}-${month}-${year}`; // Show in DD-MM-YYYY format
                }
            }
        });
    });
});









function upFileName() {
    const fileInput = document.getElementById('pdf_file');
    const fileNameSpan = document.getElementById('file-name');

    if (fileInput.files.length > 0) {
        fileNameSpan.innerText = fileInput.files[0].name; // Show selected file name
    } else {
        fileNameSpan.innerText = 'لا يوجد ملف مختار.'; // Default message
    }
}