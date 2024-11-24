// (( Document Sorting Functions ))

let currentSort = 'updated_at';  // Set default sort to updated_at
let currentOrder = 'desc';        // Default order

function setSort(sortOption) {
    // Check if the option clicked is the current sort option
    if (currentSort === sortOption) {
        // Toggle order
        currentOrder = currentOrder === 'desc' ? 'asc' : 'desc';
    } else {
        // Set new sort option and default to descending
        currentSort = sortOption;
        currentOrder = 'desc';
    }

    // Update the indicator for the dropdown
    updateSortIndicators();

    // Redirect to the sorted page
    window.location.href = `?sort=${currentSort}&order=${currentOrder}`;
}

function updateSortIndicators() {
    // Reset all arrows
    document.getElementById('dateArrow').innerHTML = '';
    document.getElementById('numberArrow').innerHTML = '';
    document.getElementById('titleArrow').innerHTML = '';
    document.getElementById('updatedAtArrow').innerHTML = '';

    // Set arrow direction based on current sort
    const arrow = currentOrder === 'desc' ? '▼' : '▲';
    if (currentSort === 'date') {
        document.getElementById('dateArrow').innerHTML = arrow;
    } else if (currentSort === 'number') {
        document.getElementById('numberArrow').innerHTML = arrow;
    } else if (currentSort === 'title') {
        document.getElementById('titleArrow').innerHTML = arrow;
    } else if (currentSort === 'updated_at') {
        document.getElementById('updatedAtArrow').innerHTML = arrow;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    currentSort = urlParams.get('sort') || 'updated_at'; // Default to updated_at
    currentOrder = urlParams.get('order') || 'desc';
    updateSortIndicators();
});



// initialize tooltips for main document view:
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);

    });
});



// Initialize flatpickr for the date fields
document.addEventListener('DOMContentLoaded', function() {
    flatpickr("#id_date", {
        dateFormat: "Y-m-d", // Day-Month-Year format
        locale: {
            firstDayOfWeek: 7, // Start week on Sunday
            dir: "rtl", // Right-to-left support
            weekdays: {
                shorthand: ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت"], // Arabic week day names
                longhand: ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"] // Full day names
            },
            months: {
                shorthand: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"], // Arabic month names
                longhand: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"] // Full month names
            }
        },
        allowInput: true, // Allow user input
    });

    // Initialize flatpickr for the orig_date field
    flatpickr("#id_orig_date", {
        dateFormat: "Y-m-d", // Day-Month-Year format
        locale: {
            firstDayOfWeek: 7, // Start week on Sunday
            dir: "rtl", // Right-to-left support
            weekdays: {
                shorthand: ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت"], // Arabic week day names
                longhand: ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"] // Full day names
            },
            months: {
                shorthand: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"], // Arabic month names
                longhand: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"] // Full month names
            }
        },
        allowInput: true, // Allow user input
    });
});



// (( DateField Input Correction Functions ))
// Function to transform date from YYYY-MM-DD to DD-MM-YYYY format
function transformDateToDDMMYYYY(ids) {
    ids.forEach(id => {
        let input = document.getElementById(id);  // Reference to the date field by ID
        if (!input) return; // Skip if the input is not found
        
        let dateValue = input.value.trim();

        // If input is empty, do nothing
        if (dateValue === '') {
            return;
        }

        // Check if the date is in YYYY-MM-DD format
        let isoDateRegex = /^\d{4}-\d{2}-\d{2}$/; // YYYY-MM-DD format
        if (isoDateRegex.test(dateValue)) {
            // If in correct format, convert to DD-MM-YYYY
            let parts = dateValue.split('-');
            let day = parts[2].padStart(2, '0');  // Ensure two digits for day
            let month = parts[1].padStart(2, '0');  // Ensure two digits for month
            input.value = `${day}-${month}-${parts[0]}`;
        }
    });
}

// Function to transform date from DD-MM-YYYY to YYYY-MM-DD format
function transformDateToYYYYMMDD(ids) {
    ids.forEach(id => {
        let input = document.getElementById(id);  // Reference to the date field by ID
        if (!input) return; // Skip if the input is not found
        
        let dateValue = input.value.trim();

        // Check if the date is in DD-MM-YYYY format
        let dateRegex = /^(\d{1,2})-(\d{1,2})-(\d{4})$/; // DD-MM-YYYY format
        let match = dateValue.match(dateRegex);

        if (match) {
            // Ensure two digits for day and month, and four digits for year
            let day = match[1].padStart(2, '0');   // Ensure two digits for day
            let month = match[2].padStart(2, '0'); // Ensure two digits for month
            let year = match[3];                   // Year is already in the correct format

            // Set the input value to YYYY-MM-DD format
            input.value = `${year}-${month}-${day}`;
        }
    });
}

// Function to automatically add dashes to date field only if they are not already present
function autoAddDashes(ids) {
    ids.forEach(id => {
        let input = document.getElementById(id);  // Reference to the date field by ID
        if (!input) return; // Skip if the input is not found
        
        let dateValue = input.value.trim();

        // Check if the value already contains more than 1 dash (indicating proper formatting already exists)
        let dashCount = (dateValue.match(/-/g) || []).length;
        if (dashCount >= 2) {
            return;  // Skip adding dashes if they are already present
        }

        // Remove any non-digit characters
        dateValue = dateValue.replace(/\D/g, ''); 

        // Automatically add dashes as the user types (DD-MM-YYYY)
        if (dateValue.length <= 2) {
            input.value = dateValue; // Only day
        } else if (dateValue.length <= 4) {
            input.value = dateValue.slice(0, 2) + '-' + dateValue.slice(2); // DD-MM
        } else if (dateValue.length <= 6) {
            input.value = dateValue.slice(0, 2) + '-' + dateValue.slice(2, 4) + '-' + dateValue.slice(4); // DD-MM-YYYY
        } else {
            input.value = dateValue.slice(0, 2) + '-' + dateValue.slice(2, 4) + '-' + dateValue.slice(4, 8); // Limit to 8 digits
        }
    });
}

// Function to validate date value
function isValidDate(day, month, year) {
    const currentYear = new Date().getFullYear();
    if (year < 1900 || year > currentYear) return false;
    if (month < 1 || month > 12) return false;
    const daysInMonth = new Date(year, month, 0).getDate();
    return day >= 1 && day <= daysInMonth;
}

// Function to validate the date input
function validateDateInput(input) {
    const dateValue = input.value.trim();
    const dateRegex = /^(\d{1,2})-(\d{1,2})-(\d{4})$/; // DD-MM-YYYY format
    const match = dateValue.match(dateRegex);

    if (match) {
        const day = parseInt(match[1], 10);
        const month = parseInt(match[2], 10);
        const year = parseInt(match[3], 10);

        // Validate the date
        if (!isValidDate(day, month, year)) {
            alert("Please enter a valid date.");
            input.value = ""; // Optionally clear the input
        }
    }
}

// event listeners to the date field
document.addEventListener('DOMContentLoaded', function () {
    const dateIds = ['id_date', 'id_orig_date']; // IDs
    const dateInputs = dateIds.map(id => document.getElementById(id));

    dateInputs.forEach(input => {
    // Trigger conversion to DD-MM-YYYY when the field is focused
        input.addEventListener('focus', () => transformDateToDDMMYYYY(dateIds));

        // Trigger conversion to YYYY-MM-DD when the field loses focus (blur event)
        input.addEventListener('blur', () => transformDateToYYYYMMDD(dateIds));

        // Add listener for input change to automatically add dashes only if necessary
        input.addEventListener('input', () => autoAddDashes(dateIds));

        input.addEventListener('input', function () {
            validateDateInput(input);
        });
    });
});



// Main Search Function
function searchDocuments() {
    const input = document.getElementById('search-input');
    const filter = input.value.toLowerCase();
    const tableBody = document.getElementById('document-table-body');
    const rows = tableBody.getElementsByTagName('tr');

    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let rowContainsSearchTerm = false;

        for (let j = 0; j < cells.length; j++) {
            if (cells[j]) {
                const cellValue = cells[j].textContent || cells[j].innerText;
                if (cellValue.toLowerCase().indexOf(filter) > -1) {
                    rowContainsSearchTerm = true;
                    break;
                }
            }
        }

        rows[i].style.display = rowContainsSearchTerm ? '' : 'none';
    }
}


// Delete Function
document.addEventListener('DOMContentLoaded', function() {
    let currentModelName;
    let currentDocumentId;
    const deleteModalElement = document.getElementById('deleteModal');

    // Create a Bootstrap modal instance
    const deleteModal = new bootstrap.Modal(deleteModalElement);

    window.confirmDeletion = function(modelName, documentId, documentNumber) {
        currentModelName = modelName;
        currentDocumentId = documentId;

        // Set the document number in the modal
        document.getElementById('documentNumber').textContent = documentNumber;

        // Show the modal using Bootstrap's modal API
        deleteModal.show();
    };

    window.closeModal = function() {
        // Hide the modal using Bootstrap's modal API
        deleteModal.hide();
    };

    document.getElementById('confirmDeleteButton').onclick = function() {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        fetch(`/delete_document/${currentModelName}/${currentDocumentId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Remove the row from the DOM
                const row = document.getElementById(`document-row-${currentDocumentId}`);
                if (row) {
                    row.remove(); // Remove the row completely
                }
                closeModal();
            } else {
                alert("كان هناك مشكلة في حذف العنصر.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("حدث خطأ أثناء حذف العنصر.");
        });
    };
});



// Obsolete Functions
// document.querySelectorAll('td').forEach(cell => {
//     if (cell.textContent.length > 75) {
//         cell.classList.add('long-text'); // Add class for long text
//     }
// });


// function upFileName() {
//     const fileInput = document.getElementById('pdf_file');
//     const fileNameSpan = document.getElementById('file-name');

//     if (fileInput.files.length > 0) {
//         fileNameSpan.innerText = fileInput.files[0].name; // Show selected file name
//     } else {
//         fileNameSpan.innerText = 'لا يوجد ملف مختار.'; // Default message
//     }
// }

// Print the PDF document
// function printDocument() {
//     if (pdfDoc && pdfDoc.numPages > 0) {
//         // Create a new window for printing
//         const printWindow = window.open('', '_blank');
//         const pdfUrl = pdfDoc.loadingTask.url; // Use the URL for the PDF file

//         printWindow.document.write(`
//             <iframe src="${pdfUrl}" style="width:100%; height:100%;" frameborder="0"></iframe>
//         `);
//         printWindow.document.close();
//         printWindow.onload = function () {
//             printWindow.print();
//             printWindow.onafterprint = function () {
//                 printWindow.close();
//             };
//         };
//     } else {
//         alert('No PDF available for printing.');
//     }
// }


// // Handle scroll events to navigate pages
// function handleScroll(event) {
//     event.preventDefault(); // Prevent default scroll behavior

//     if (event.deltaY < 0 && currentPage > 1) {
//         // Scrolling up
//         currentPage--;
//         drawPage(currentPage);
//     } else if (event.deltaY > 0 && pdfDoc && currentPage < pdfDoc.numPages) {
//         // Scrolling down
//         currentPage++;
//         drawPage(currentPage);
//     }
// }

