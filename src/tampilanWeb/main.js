const fileInputId = "file";
const submitButtonId = "submit";
const apiUrl = "http://localhost:8080/compress";

/**
 * @type {HTMLInputElement}
 */
const fileInput = document.getElementById(fileInputId);
const submitButton = document.getElementById(submitButtonId);
const fileName = document.querySelector(".file-name");
const wrapper = document.querySelector(".wrapper");
const defaultBtn = document.querySelector("#file");
const customBtn = document.querySelector("#custom-btn");
const cancelBtn = document.querySelector("#cancel-btn i");
const img = document.querySelector("img");
let regExp = /[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_ ]+$/;

function defaultBtnActive() {
    defaultBtn.click();
}
defaultBtn.addEventListener("change", function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function() {
            const result = reader.result;
            img.src = result;
            wrapper.classList.add("active");
        }
        cancelBtn.addEventListener("click", function() {
            img.src = "";
            wrapper.classList.remove("active");
        })
        reader.readAsDataURL(file);
    }
    if (this.value) {
        let valueStore = this.value.match(regExp);
        fileName.textContent = valueStore;
    }
});
submitButton.addEventListener("click", () => {
  const file = fileInput.files[0];
  const formData = new FormData();
  // TODO: Delete name field, add compression rate field from user input.
  formData.append("name", fileInput.value.replace("C:\\fakepath\\", ""));
  formData.append("image", file);
  const xhr = new XMLHttpRequest();
  xhr.open("POST", apiUrl);

  xhr.onload = () => {
    // TODO: Display the image
  };

  xhr.send(formData);
});
