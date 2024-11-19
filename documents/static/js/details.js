

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


document.querySelectorAll('td').forEach(cell => {
    if (cell.textContent.length > 75) {
        cell.classList.add('long-text'); // Add class for long text
    }
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

