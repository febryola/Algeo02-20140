const path = require("path");
const fs = require("fs");
const { execSync } = require("child_process");

/**
 *
 * @param {string} filepath Uploaded image file path.
 * @param {string} name Image filename.
 * @param {{chunkSize: string, rank: string}} options
 *        Compression options.
 * @return {{dataUrl: string, time: string, pixelDiff: string}}
 *         Image data url, compression time, and pixel differences.
 */
function compress(filepath, name, options) {
  const compressModule = "./modules/compress.py";
  const newFilepath = rename(filepath, name);
  const imageFilePath = path.relative(compressModule, newFilepath);
  const cmd = [
    "py",
    path.basename(compressModule),
    path.normalize(imageFilePath),
    options.chunkSize,
    options.rank,
  ].join(" ");
  execSync(cmd, { cwd: "src/modules", env: process.env });
  const imageData = fs.readFileSync(`temp/${getNewFilename(name)}`, "base64");
  const ext = path.extname(name);
  const dataUrl = `data:${getMimeType(ext)};base64,${imageData}`;
  let result = fs.readFileSync(`temp/${path.parse(name).name}-result.txt`, {
    encoding: "utf-8",
  });
  result = result.replace("\r", "");
  const [time, pixelDiff] = result.split("\n");
  return {
    dataUrl,
    time,
    pixelDiff,
  };
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
  const resFilename = `${path.parse(filename).name}-result.txt`;
  fs.unlinkSync(path.join(tempDir, filename));
  fs.unlinkSync(path.join(tempDir, newFilename));
  fs.unlinkSync(path.join(tempDir, resFilename));
}

/**
 *
 * @param {string} ext File extension
 */
function getMimeType(ext) {
  switch (ext) {
    case ".jpg":
    case ".jpeg":
      return "image/jpeg";
    case ".png":
      return "image/png";
    case ".webp":
      return "image/webp";
    case ".ico":
      return "image/vnd.microsoft.icon";
    case ".svg":
      return "image/svg+xml";
  }
}

module.exports = { compress, getNewFilename, clean };
