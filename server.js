const express = require("express");
const bp = require("body-parser");
const formidable = require("formidable").formidable;
const { compress } = require("./src/compress");

const fs = require("fs");

const port = 8080;
const app = express();

app.use(bp.json());
app.use(bp.urlencoded({ extended: true }));
app.use(express.static("./src/tampilanWeb"));
app.post("/compress", (req, res) => {
  const form = formidable({ uploadDir: "temp" });

  form.parse(req, (err, fields, files) => {
    if (err) {
      console.log(err);
      res.status(500);
    }
    const image = files["image"];
    const path = image.filepath;
    const name = image.originalFilename;
    compress(path, name);
    // TODO: Send the compressed file as response.
    res.send("");
  });
});
app.listen(port);
console.log(`listening to port ${port}`);
