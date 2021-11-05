const path = require("path");
const fs = require("fs");
const { execSync } = require("child_process");

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
  execSync(cmd, { cwd: "src/modules", env: process.env });
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

/**
 *
 * @param {string} filename Image filename.
 * @returns Compressed image filename.
 */
function getNewFilename(filename) {
  [base, ext] = filename.split(".");
  return base + "-compressed." + ext;
}

/**
 *
 * @param {string} filename Image filename.
 */
function clean(filename) {
  const tempDir = "temp";
  const newFilename = getNewFilename(filename);
  fs.unlinkSync(path.join(tempDir, filename));
  fs.unlinkSync(path.join(tempDir, newFilename));
}

module.exports = { compress, getNewFilename, clean };
