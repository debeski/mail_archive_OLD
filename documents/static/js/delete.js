document.addEventListener('DOMContentLoaded', function() {
    let currentModelName;
    let currentDocumentId;

    window.confirmDeletion = function(modelName, documentId) {
        currentModelName = modelName;
        currentDocumentId = documentId;
        document.getElementById('deleteModal').style.display = 'block';
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
