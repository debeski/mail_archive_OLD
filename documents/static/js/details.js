// Function to open the document details modal
function openDocumentDetails(documentId) {
    fetch(`/get_document_details/${documentId}/`)
        .then(response => response.json())
        .then(data => {
            // Populate modal fields
            document.getElementById('modal-title').innerText = data.title;
            document.getElementById('modal-reg-number').innerText = `رقم الرسالة: ${data.reg_number}`;
            document.getElementById('modal-out-date').innerText = `التاريخ: ${data.out_date}`;
            document.getElementById('modal-dept-from').innerText = `من: ${data.dept_from}`;
            document.getElementById('modal-dept-to').innerText = `إلى: ${data.dept_to}`;
            document.getElementById('modal-keywords').innerText = `الكلمات المفتاحية: ${data.keywords}`;

            const pdfContainer = document.getElementById('pdf-preview');
            pdfContainer.innerHTML = ''; // Clear previous content

            if (data.pdf_file) {
                const loadingTask = pdfjsLib.getDocument(data.pdf_file);
                loadingTask.promise.then(pdf => {
                    for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
                        pdf.getPage(pageNumber).then(page => {
                            const scale = 1.5; // Adjust scale for sizing
                            const viewport = page.getViewport({ scale: scale });
            
                            // Prepare canvas using PDF page dimensions
                            const canvas = document.createElement('canvas');
                            const context = canvas.getContext('2d');
                            canvas.height = viewport.height;
                            canvas.width = viewport.width;
            
                            // Append the canvas to the container
                            pdfContainer.appendChild(canvas);
            
                            // Render the PDF page into the canvas context
                            const renderContext = {
                                canvasContext: context,
                                viewport: viewport
                            };
                            page.render(renderContext);
                        });
                    }
                }, reason => {
                    console.error(reason); // Error loading PDF
                });
            }

            // Show the modal
            const modal = document.getElementById('documentModal');
            modal.style.display = 'block';
            
            // Ensure the close behavior works
            modal.onclick = function(event) {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            };
        })
        .catch(error => console.error('Error fetching document details:', error));
}