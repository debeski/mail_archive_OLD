// (( Document Sorting Functions ))

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
    const dateArrow = document.getElementById('dateArrow');
    const numberArrow = document.getElementById('numberArrow');
    const titleArrow = document.getElementById('titleArrow');
    const updatedAtArrow = document.getElementById('updatedAtArrow');


    if (dateArrow) dateArrow.innerHTML = '';
    if (numberArrow) numberArrow.innerHTML = '';
    if (titleArrow) titleArrow.innerHTML = '';
    if (updatedAtArrow) updatedAtArrow.innerHTML = '';

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



function viewDocumentDetails(button) {
    // Get the row of the clicked button
    const row = button.closest('tr');
    const Number = row.cells[0].innerText;
    const Date = row.cells[1].innerText;
    const documentTitle = row.cells[2].innerText;
    const pdfFile = row.dataset.pdfFile; // Assuming you have a data attribute for the PDF file
    const objectId = row.dataset.objectId; // Assuming you have a data attribute for the object ID

    // Populate modal fields
    document.getElementById('modal-title').innerText = documentTitle;
    document.getElementById('modal-number').innerText = `رقم الرسالة: ${Number}`;
    document.getElementById('modal-date').innerText = `التاريخ: ${Date}`;
    
    // Set the download link
    const modelName = 'your_model_name'; // Replace with your actual model name
    const downloadLink = document.getElementById('download-link');
    downloadLink.href = `{% url 'download_document' model_name=modelName object_id='${objectId}' %}`; // Set the href dynamically

    // Check if a PDF file is available
    const pdfContainer = document.getElementById('pdfPreviewContainer');
    pdfContainer.innerHTML = ''; // Clear previous content

    if (pdfFile) {
        const loadingTask = pdfjsLib.getDocument(pdfFile);
        loadingTask.promise.then(pdf => {
            return pdf.getPage(1);
        }).then(page => {
            const scale = 1.5;
            const viewport = page.getViewport({ scale });
            const canvas = document.createElement('canvas');
            pdfContainer.appendChild(canvas);
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            const renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            return page.render(renderContext).promise;
        }).catch(err => {
            console.error('Error loading PDF:', err);
        });
    } else {
        pdfContainer.innerHTML = '<p>لا يوجد ملف PDF متاح.</p>';
    }

    // Show the modal
    const modal = document.getElementById('documentModal');
    modal.style.display = 'block';
}





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

