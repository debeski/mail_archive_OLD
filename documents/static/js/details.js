let currentPage = 1; // Track the current page number
let pdfDoc = null; // Store the PDF document

// Function to open the document details modal
// Main function to render PDF based on the source (file input or URL)
function renderPDF(source, isFileInput = false) {
    const pdfContainer = document.getElementById('pdf-preview');
    pdfContainer.innerHTML = ''; // Clear previous content

    if (isFileInput) {
        // Handle PDF from file input
        const fileReader = new FileReader();
        fileReader.onload = function() {
            const typedarray = new Uint8Array(this.result);
            loadAndRenderPDF(typedarray);
        };
        fileReader.readAsArrayBuffer(source.files[0]); // Use the file input directly
    } else {
        // Handle PDF from URL
        fetch(source)
            .then(response => response.json())
            .then(data => {
                if (data.pdf_file) {
                    loadAndRenderPDF(data.pdf_file);
                } else {
                    pdfContainer.innerHTML = '<div class="no-pdf-message">لا يوجد ملف PDF!</div>';
                }
            })
            .catch(error => console.error('Error fetching PDF:', error));
    }
}

// Load and render the PDF document
function loadAndRenderPDF(pdfSource) {
    const loadingTask = pdfjsLib.getDocument(pdfSource);
    loadingTask.promise.then(pdf => {
        pdfDoc = pdf; // Store the loaded PDF document
        currentPage = 1; // Reset the current page
        drawPage(currentPage); // Render the first page

        // Add scroll event listener for page navigation
        const pdfContainer = document.getElementById('pdf-preview');
        pdfContainer.addEventListener('wheel', handleScroll);
    }).catch(error => {
        console.error('Error loading PDF:', error);
        document.getElementById('pdf-preview').innerHTML = 'Error loading PDF file.';
    });
}

// Draw the specified page on the canvas and handle scroll events
function drawPage(pageNumber) {
    const pdfContainer = document.getElementById('pdf-preview');
    pdfContainer.innerHTML = ''; // Clear previous content

    pdfDoc.getPage(pageNumber).then(page => {
        const viewport = page.getViewport({ scale: 1 });
        const containerWidth = pdfContainer.clientWidth;
        const containerHeight = pdfContainer.clientHeight;

        const scale = Math.min(containerWidth / viewport.width, containerHeight / viewport.height);
        const scaledViewport = page.getViewport({ scale: scale });

        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.height = scaledViewport.height;
        canvas.width = scaledViewport.width;

        pdfContainer.appendChild(canvas);

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
        pageNumberDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
        pageNumberDiv.style.padding = '5px';
        pageNumberDiv.style.borderRadius = '3px';

        pdfContainer.appendChild(pageNumberDiv);
    });
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


// Usage for opening document details
function openDocumentDetails(modelType, documentId) {
    fetch(`/get_document_details/${modelType}/${documentId}/`)
        .then(response => response.json())
        .then(data => {
            // Populate modal fields dynamically based on the model type
            document.getElementById('modal-title').innerText = data.title || 'No title available';
            document.getElementById('modal-number').innerHTML = `رقم:<br>${data.number || ''}`;
            document.getElementById('modal-date').innerHTML = `التاريخ:<br>${data.date || ''}`;
            document.getElementById('modal-keywords').innerHTML = `الكلمات المفتاحية:<br>${data.keywords || ''}`;
            document.getElementById('modal-dept-from').innerHTML = `من:<br>${data.dept_from || ''}`;
            document.getElementById('modal-dept-to').innerHTML = `إلى:<br>${data.dept_to || ''}`;
            if (data.orig_number) {
                document.getElementById('modal-orig-number').innerHTML = `رقم الأصل:<br>${data.orig_number || ''}`;
                document.getElementById('modal-orig-date').innerHTML = `تاريخ الأصل:<br>${data.orig_date || ''}`;
            }
            if (data.minister) {
                document.getElementById('modal-minister').innerHTML = `الوزير:<br>${data.minister || ''}`;
            }
            if (data.government) {
                document.getElementById('modal-government').innerHTML = `الحكومة:<br>${data.government || ''}`;
            }
            if (data.attach_file) {
                document.getElementById('modal-attach-file').innerHTML = `<a href="${data.attach_file}">ملف مرفق</a>`;
            }

            // Render PDF from fetched data
            renderPDF(data.pdf_file, false); // Pass URL and indicate it's not a file input

            // Show the modal using Bootstrap's method
            $('#documentModal').modal('show');
        })
        .catch(error => console.error('Error fetching document details:', error));
}

// Usage for rendering PDF from file input
function handleFileInputChange() {
    const fileInput = document.getElementById('pdf_file');
    if (fileInput.files.length > 0) {
        renderPDF(fileInput, true); // Pass file input and indicate it's a file input
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

function upFileName() {
    const fileInput = document.getElementById('pdf_file');
    const fileNameSpan = document.getElementById('file-name');

    if (fileInput.files.length > 0) {
        fileNameSpan.innerText = fileInput.files[0].name; // Show selected file name
    } else {
        fileNameSpan.innerText = 'لا يوجد ملف مختار.'; // Default message
    }
}

