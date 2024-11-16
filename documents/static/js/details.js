let currentPage = 1; // Track the current page number
let pdfDoc = null; // Store the PDF document

// Function to open the document details modal
function openDocumentDetails(documentId) {
    fetch(`/get_document_details/${documentId}/`)
        .then(response => response.json())
        .then(data => {
            // Populate modal fields with labels on separate lines
            document.getElementById('modal-title').innerText = data.title;
            document.getElementById('modal-reg-number').innerHTML = `رقم الرسالة:<br>${data.reg_number}`;
            document.getElementById('modal-out-date').innerHTML = `التاريخ:<br>${data.out_date}`;
            document.getElementById('modal-dept-from').innerHTML = `من:<br>${data.dept_from}`;
            document.getElementById('modal-dept-to').innerHTML = `إلى:<br>${data.dept_to}`;
            document.getElementById('modal-keywords').innerHTML = `الكلمات المفتاحية:<br>${data.keywords}`;

            const pdfContainer = document.getElementById('pdf-preview');
            pdfContainer.innerHTML = ''; // Clear previous content

            if (data.pdf_file) {
                const loadingTask = pdfjsLib.getDocument(data.pdf_file);
                loadingTask.promise.then(pdf => {
                    pdfDoc = pdf; // Store the loaded PDF document
                    currentPage = 1; // Reset the current page

                    renderPage(currentPage); // Render the first page

                    // Add scroll event listener
                    pdfContainer.addEventListener('wheel', handleScroll);
                }).catch(error => {
                    console.error('Error loading PDF:', error);
                });
            }

            // Show the modal
            const modal = document.getElementById('documentModal');
            modal.style.display = 'block';

            // Close modal behavior
            modal.onclick = function(event) {
                if (event.target === modal) {
                    modal.style.display = 'none';
                    pdfContainer.removeEventListener('wheel', handleScroll); // Clean up
                }
            };
        })
        .catch(error => console.error('Error fetching document details:', error));
}

// Function to render a specific page
function renderPage(pageNumber) {
    const pdfContainer = document.getElementById('pdf-preview');
    pdfContainer.innerHTML = ''; // Clear previous content

    pdfDoc.getPage(pageNumber).then(page => {
        const viewport = page.getViewport({ scale: 1 }); // Get the viewport at 100%
        
        const containerWidth = pdfContainer.clientWidth; // Get the width of the container
        const containerHeight = pdfContainer.clientHeight; // Get the height of the container

        // Calculate scale based on the container size and the PDF page size
        const scaleWidth = containerWidth / viewport.width;
        const scaleHeight = containerHeight / viewport.height;
        const scale = Math.min(scaleWidth, scaleHeight); // Use the smaller scale to ensure full visibility

        const scaledViewport = page.getViewport({ scale: scale }); // Get the viewport with the calculated scale

        // Create a canvas to render the PDF page
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.height = scaledViewport.height;
        canvas.width = scaledViewport.width;

        // Append the canvas to the PDF preview container
        pdfContainer.appendChild(canvas);

        // Render the page to the canvas
        const renderContext = {
            canvasContext: context,
            viewport: scaledViewport
        };
        page.render(renderContext);

        // Create and display page number
        const pageNumberDiv = document.createElement('div');
        pageNumberDiv.innerText = `Page ${pageNumber} of ${pdfDoc.numPages}`;
        pageNumberDiv.style.position = 'absolute';
        pageNumberDiv.style.bottom = '10px';
        pageNumberDiv.style.right = '10px';
        pageNumberDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.7)'; // Semi-transparent background
        pageNumberDiv.style.padding = '5px';
        pageNumberDiv.style.borderRadius = '3px';

        pdfContainer.appendChild(pageNumberDiv);
    });
}

// Handle scroll events
function handleScroll(event) {
    event.preventDefault(); // Prevent default scroll behavior

    if (event.deltaY < 0) {
        // Scrolling up
        if (currentPage > 1) {
            currentPage--;
            renderPage(currentPage);
        }
    } else {
        // Scrolling down
        if (pdfDoc && currentPage < pdfDoc.numPages) {
            currentPage++;
            renderPage(currentPage);
        }
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

    window.confirmDeletion = function(modelName, documentId) {
        currentModelName = modelName;
        currentDocumentId = documentId;
        const deleteModal = document.getElementById('deleteModal');
        deleteModal.style.display = 'block';

        // Close modal behavior when clicking outside
        deleteModal.onclick = function(event) {
            if (event.target === deleteModal) {
                closeModal();
            }
        };
    };

    window.closeModal = function() {
        document.getElementById('deleteModal').style.display = 'none';
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
                alert("There كان هناك مشكلة في حذف العنصر.");
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

