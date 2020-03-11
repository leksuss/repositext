let contentFileElem = document.getElementById("id_content_file");
let nameElem = document.getElementById('document_id_name');

const setNameElemText = function () {
    let fileName = contentFileElem.value.split('\\').pop();
    nameElem.value = fileName;
}

const showAddFormDialog = function() {
    document.getElementById("add-folder-dialog").showModal();
}

const showAddDocumentDialog = function() {
    document.getElementById("add-document-dialog").showModal();
}

contentFileElem.onchange = setNameElemText;
