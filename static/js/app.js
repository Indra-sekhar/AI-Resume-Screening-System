const fileInput = document.getElementById("resume");
const uploadArea = document.getElementById("uploadArea");
const fileName = document.getElementById("fileName");

const jobDescription = document.getElementById("jobDescription");
const charCount = document.getElementById("charCount");

const form = document.getElementById("resumeForm");
const analyzeBtn = document.getElementById("analyzeBtn");
const buttonText = document.getElementById("buttonText");
const loader = document.getElementById("loader");


/* File selection */

fileInput.addEventListener("change", function () {

    if (this.files.length > 0) {
        showFile(this.files[0]);
    }

});


function showFile(file) {

    if (file.type !== "application/pdf") {

        alert("Please select a PDF file.");

        fileInput.value = "";
        fileName.textContent = "";

        return;
    }

    if (file.size > 10 * 1024 * 1024) {

        alert("File size must be less than 10MB.");

        fileInput.value = "";
        fileName.textContent = "";

        return;
    }

    fileName.textContent = "✓ " + file.name;
}


/* Drag and drop */

uploadArea.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadArea.classList.add("dragover");

});


uploadArea.addEventListener("dragleave", function () {

    uploadArea.classList.remove("dragover");

});


uploadArea.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadArea.classList.remove("dragover");

    const files = event.dataTransfer.files;

    if (files.length > 0) {

        showFile(files[0]);

    }

});


/* Character counter */

function updateCharacterCount() {

    charCount.textContent = jobDescription.value.length;

}

jobDescription.addEventListener("input", updateCharacterCount);

updateCharacterCount();


/* Submit */

form.addEventListener("submit", function (event) {

    if (!fileInput.files.length) {

        event.preventDefault();

        alert("Please select a resume PDF.");

        return;
    }

    analyzeBtn.disabled = true;

    buttonText.textContent = "Analyzing Resume...";

    loader.style.display = "inline-block";

});