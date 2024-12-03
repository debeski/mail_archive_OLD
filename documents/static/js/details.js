
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        if (timeoutId) {
            clearTimeout(timeoutId); // Clear the previous timeout
        }
        timeoutId = setTimeout(() => {
            func.apply(this, args); // Call the original function
        }, delay);
    };
}

// initialize tooltips for main document view:
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);

    });
});


// Delete Function:
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

// Details Pane:
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
