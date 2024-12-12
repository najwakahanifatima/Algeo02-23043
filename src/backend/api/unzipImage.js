import fs from 'fs';
import path from 'path';
import JSZip from 'jszip';
import formidable from 'formidable';

export const config = {
  api: {
    bodyParser: false, // membuat next.js tidak langsung menbaca informasi seperti JSON file
  },
};

const uploadHandler = async (req, res) => {
  try {
    // Parse the incoming request to get the uploaded file
    const form = new formidable.IncomingForm();
    form.uploadDir = path.join(process.cwd(), 'public'); // Temporary file storage location
    form.keepExtensions = true;

    form.parse(req, async (err, fields, files) => {
      if (err) {
        return res.status(500).json({ message: 'File upload error' });
      }

      // file path
      const zipFilePath = files.file[0].path;

      // baca file zip
      const zipData = fs.readFileSync(zipFilePath);

      const zip = await JSZip.loadAsync(zipData);
      const fileNames = Object.keys(zip.files); // nama file dalam zip

      const extractedFiles = [];

      // extract setiap file
      for (const fileName of fileNames) {
        const file = zip.files[fileName];

        const content = await file.async('base64'); //pake base64 soalnya gambarnya mau didisplay di web 
        extractedFiles.push({ fileName, content });
      }

      // Clean up the temporary file 
      fs.unlinkSync(zipFilePath);

      // kirim extractes files n message
      res.status(200).json({
        message: 'ZIP file processed successfully',
        extractedFiles,
      });
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
};

export default uploadHandler;
