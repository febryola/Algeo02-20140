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
const imgRes = document.getElementById("res");
const downloadButton = document.getElementsByClassName("download")[0];
let regExp = /[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_ ]+$/;

function defaultBtnActive() {
  defaultBtn.click();
}
defaultBtn.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function () {
      const result = reader.result;
      img.src = result;
      wrapper.classList.add("active");
    };
    cancelBtn.addEventListener("click", function () {
      img.src = "";
      wrapper.classList.remove("active");
    });
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
  const filename = fileInput.value.replace("C:\\fakepath\\", "");
  // TODO: Delete name field, add compression rate field from user input.
  formData.append("name", filename);
  //   const ext = filename.split(".")[1];
  formData.append("image", file);
  const xhr = new XMLHttpRequest();
  xhr.open("POST", apiUrl);
  xhr.responseType = "json";

  xhr.onload = () => {
    /**
     * @type {{dataUrl: string, time: string, pixelDiff: string}
     */
    const res = xhr.response;
    const { dataUrl, time, pixelDiff } = res;
    imgRes.src = dataUrl;
    const nameParts = filename.split(".");
    const name = `${nameParts[0]}-compressed.${nameParts[1]}`;
    downloadButton.addEventListener(
      "click",
      download.bind(null, dataUrl, name)
    );
  };

  xhr.send(formData);
});

function download(dataUrl, name) {
  const a = document.createElement("a");
  a.download = name;
  a.href = dataUrl;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
