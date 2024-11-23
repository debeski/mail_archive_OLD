// Initialize flatpickr for the main date field
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


// initialize tooltips:
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);

    });
});


// Function to transform date format
function transformDateFormat() {
    let input = document.getElementById('id_date');
    let dateValue = input.value.trim();

    // Check if the date is already in YYYY-MM-DD format
    let isoDateRegex = /^\d{4}-\d{2}-\d{2}$/; // YYYY-MM-DD format
    if (isoDateRegex.test(dateValue)) {
        return; // If already in the correct format, do nothing
    }

    // Check if the date is in DD-MM-YYYY format
    let regex = /^(\d{2})-(\d{2})-(\d{4})$/;
    let match = dateValue.match(regex);

    if (match) {
        // Rearrange to YYYY-MM-DD format
        let day = match[1];
        let month = match[2];
        let year = match[3];

        // Set the input value in YYYY-MM-DD format
        input.value = `${year}-${month}-${day}`;
    }
}

// Add event listeners
const dateInput = document.getElementById('id_date');

// Trigger format conversion when focus is lost or user presses Tab
dateInput.addEventListener('blur', transformDateFormat);



// Print the PDF document
function printDocument() {
    if (pdfDoc && pdfDoc.numPages > 0) {
        // Create a new window for printing
        const printWindow = window.open('', '_blank');
        const pdfUrl = pdfDoc.loadingTask.url; // Use the URL for the PDF file

        printWindow.document.write(`
            <iframe src="${pdfUrl}" style="width:100%; height:100%;" frameborder="0"></iframe>
        `);
        printWindow.document.close();
        printWindow.onload = function () {
            printWindow.print();
            printWindow.onafterprint = function () {
                printWindow.close();
            };
        };
    } else {
        alert('No PDF available for printing.');
    }
}


// Handle scroll events to navigate pages
function handleScroll(event) {
    event.preventDefault(); // Prevent default scroll behavior

    if (event.deltaY < 0 && currentPage > 1) {
        // Scrolling up
        currentPage--;
        drawPage(currentPage);
    } else if (event.deltaY > 0 && pdfDoc && currentPage < pdfDoc.numPages) {
        // Scrolling down
        currentPage++;
        drawPage(currentPage);
    }
}


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
                document.getElementById(`document-row-${currentDocumentId}`).remove();
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


// Document Sort Functions
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

// Initialize the sort indicators based on the current URL parameters
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    currentSort = urlParams.get('sort') || 'updated_at'; // Default to updated_at
    currentOrder = urlParams.get('order') || 'desc';
    updateSortIndicators();
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
