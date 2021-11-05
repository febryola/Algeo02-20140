const path = require("path");
const fs = require("fs");
const { exec } = require("child_process");
/**
 *
 * @param {string} filepath Uploaded image file path.
 * @param {string} name Image filename.
 */
function compress(filepath, name) {
  const compressModule = "./modules/compress.py";
  const newFilepath = rename(filepath, name);
  const imageFilePath = path.relative(compressModule, newFilepath);
  const cmd = [
    "py",
    path.basename(compressModule),
    path.normalize(imageFilePath),
    "0.15",
  ].join(" ");
  // TODO: Fix process execution, because somehow this
  // exec("py compress.py ..\\..\\temp\\Example.jpg 0.15", { cwd: "modules" });
  //       is working. But this is not.
  exec(cmd, { cwd: "modules" });
}

/**
 *
 * @param {string} filepath Path to the file to be renamed.
 * @param {string} name New filename.
 */
function rename(filepath, name) {
  let parsedPath = path.parse(filepath);
  const newPath = path.join(parsedPath.dir, name);
  fs.renameSync(filepath, newPath);
  return newPath;
}

module.exports = { compress };
