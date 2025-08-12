const editButtons = document.querySelectorAll('.edit-btn');
const formBody = document.getElementById('form-body');
const cardForm = document.getElementById('card-form');
const formTitle = document.getElementById('form-title');
const formTitleInput = document.getElementById('id_title');
const formContent = document.getElementById('id_content');
const submitButton = document.getElementById('submit-btn');

const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
const deleteButtons = document.querySelectorAll('.delete-btn');
const deleteConfirm = document.getElementById('deleteConfirm');

/**
 * Initialises edit functionality for the provided edit buttons.
**/

for (let button of editButtons) {
    button.addEventListener('click', (e) => {
        // Retrieve card ID from button's data atttribute
        let cardId = e.target.dataset.cardId;
        // Retrieve card title and content from DOM
        let cardTitle = document.getElementById(`card-title${cardId}`);
        let cardContent = document.getElementById(`card-content${cardId}`);
        // Populate form fields with card data
        formTitleInput.value = cardTitle.innerText;
        formContent.value = cardContent.innerText;
        // Alter form title and submit button text
        formTitle.innerText = "Edit Card";
        submitButton.innerText = "Update Card";
        // Set form action to the card's update URL
        cardForm.setAttribute('action', `/my-cards/edit_card/${cardId}/`);
        // Refocus on title input field for user convenience
        formTitleInput.focus();
        // Add highlight styling to form body to draw user attention
        formBody.classList.add('focus');
});
}

// Delete functionality for delete buttons
for (let button of deleteButtons) {
    button.addEventListener('click', (e) => {
        // Retrieve card ID from button's data attribute
        let cardId = e.target.dataset.cardId;
        // Set the delete confirmation link on the modal to the card's delete URL view
        deleteConfirm.href = `/my-cards/delete-card/${cardId}/`;
        // Show the delete confirmation modal
        deleteModal.show();
    });
}

