const express = require("express");
const bp = require("body-parser");
const formidable = require("formidable").formidable;
const { compress, getNewFilename, clean } = require("./src/compress");

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
    const filepath = image.filepath;
    /**
     * @type {string}
     */
    const filename = image.originalFilename;
    compress(filepath, filename);

    res.sendFile(getNewFilename(filename), { root: "temp" }, (err) => {
      clean(filename);
      res.end();
    });
  });
});
app.listen(port);
console.log(`listening to port ${port}`);
