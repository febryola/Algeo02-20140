const fileInputId = "file";
const submitButtonId = "submit";
const apiUrl = "http://localhost:8080/compress";

/**
 * @type {HTMLInputElement}
 */
const fileInput = document.getElementById(fileInputId);
const submitButton = document.getElementById(submitButtonId);

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
