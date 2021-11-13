const fs = require("fs");
const express = require("express");
const bp = require("body-parser");
const formidable = require("formidable").formidable;
const { compress, clean } = require("./src/compress");

const port = 8080;
const app = express();

if (!fs.existsSync("temp")) {
  fs.mkdirSync("temp");
}

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
    const chunkSize = fields["chunk_size"];
    const rank = fields["rank"];
    const image = files["image"];
    const filepath = image.filepath;
    /**
     * @type {string}
     */
    const filename = image.originalFilename;
    const compRes = compress(filepath, filename, {
      chunkSize,
      rank,
    });
    res.json(compRes);
    res.end();
    clean(filename);
  });
});
app.listen(port);
console.log(`listening to port ${port}: http://localhost:8080/`);
