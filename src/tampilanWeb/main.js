document.addEventListener("DOMContentLoaded", () => {
  const fileInputId = "file";
  const submitButtonId = "submit";
  const apiUrl = "compress";

  /**
   * @type {HTMLInputElement}
   */
  const fileInput = document.getElementById(fileInputId);
  const submitButton = document.getElementById(submitButtonId);
  const fileName = document.querySelector(".file-name");
  const wrapper = document.querySelector(".wrapper");
  const defaultBtn = document.querySelector("#file");
  const cancelBtn = document.querySelector("#cancel-btn i");
  const img = document.querySelector("img");
  const imgRes = document.getElementById("res");
  const downloadButton = document.getElementsByClassName("download")[0];
  const uploadFileButton = document.getElementsByClassName("file-btn")[0];
  const resultBar = document.getElementsByClassName("result")[0];
  let listener = null;
  let regExp = /[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_ ]+$/;

  const selected = document.querySelector(".selected");
  const optionsContainer = document.querySelector(".options-container");
  const optionsList = document.querySelectorAll(".option");

  selected.addEventListener("click", () => {
    optionsContainer.classList.toggle("active");
  });

  optionsList.forEach((o) => {
    o.addEventListener("click", () => {
      const value = o.getAttribute("value");
      selected.setAttribute("value", value);
      selected.innerHTML = o.querySelector("label").innerHTML;
      optionsContainer.classList.remove("active");
    });
  });

  uploadFileButton.addEventListener("click", () => {
    defaultBtn.click();
  });
  defaultBtn.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function () {
        img.removeAttribute("hidden");
        imgRes.setAttribute("hidden", "");
        const result = reader.result;
        img.src = result;
        wrapper.classList.add("active");
      };
      cancelBtn.addEventListener("click", function () {
        img.src = "";
        imgRes.src = "";
        img.setAttribute("hidden", "");
        wrapper.classList.remove("active");
        defaultBtn.value = null;
        if (listener) {
          downloadButton.removeEventListener("click", listener);
        }
        downloadButton.setAttribute("disabled", "");
        resultBar.setAttribute("hidden", "");
      });
      reader.readAsDataURL(file);
      resultBar.setAttribute("hidden", "");
    } else {
      img.src = null;
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
    const value = selected.getAttribute("value");
    if (!file) {
      alert("Please upload an image file !");
      return;
    }
    if (!value) {
      // TODO: Display an error snackbar
      alert("Please choose chunk size & compression rank !");
      return;
    }
    const [chunkSize, rank] = value.split("-");
    formData.append("chunk_size", chunkSize);
    formData.append("rank", rank);
    formData.append("image", file);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", apiUrl);
    xhr.responseType = "json";

    xhr.onload = () => {
      if (listener) {
        downloadButton.removeEventListener("click", listener);
      }
      /**
       * @type {{dataUrl: string, time: string, pixelDiff: string}}
       */
      const res = xhr.response;
      const { dataUrl, time, pixelDiff } = res;
      const resText = `Compressed in ${time} seconds | Pixel differences : ${pixelDiff}%`;
      resultBar.innerText = resText;
      resultBar.removeAttribute("hidden");
      imgRes.src = dataUrl;
      imgRes.removeAttribute("hidden");
      downloadButton.removeAttribute("disabled");
      const nameParts = filename.split(".");
      const name = `${nameParts[0]}-compressed.${nameParts[1]}`;
      listener = download.bind(null, dataUrl, name);
      downloadButton.addEventListener("click", listener);
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
});
