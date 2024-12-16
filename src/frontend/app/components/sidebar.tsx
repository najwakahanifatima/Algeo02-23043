import React, { useState } from 'react';

type SideBarProps = {
  type: string;
};

export default function SideBar({ type }: SideBarProps) {
  const [selectedAudioFile, setSelectedAudioFile] = useState<File[]>([]);
  const [selectedImageFile, setSelectedImageFile] = useState<File[]>([]);
  const [selectedMapperFile, setSelectedMapperFile] = useState<File[]>([]);
  const [selectedQueryFile, setSelectedQueryFile] = useState<File | null>(null);
  const [isDatabaseLoaded, setIsDatabaseLoaded] = useState(false);
  const [computationTime, setComputationTime] = useState<string | null>(null);
  const [compTimeImage, setCompTimeImage] = useState<string | null>(null);
  const [compTimeMusic, setCompTimeMusic] = useState<string | null>(null);

  const uploadFile = async (files: File[], endpoint: string): Promise<{ success: boolean; duration?: string }> => {
    if (files.length === 0) {
      alert("No files selected!");
      return { success: false };
    }
  
    const formData = new FormData();
    files.forEach((file: File) => formData.append("files", file)); // Append multiple files
    
    try {
      const response = await fetch(`http://localhost:8000/${endpoint}/`, {
        method: "POST",
        body: formData,
      });
      console.log(endpoint);
      console.log(response);
      if (!response.ok) throw new Error(`Failed to upload files to ${endpoint}`);
      console.log("hai1");
      const result = await response.json();
      alert(result.message);
      return { success: true, duration: result.duration };

    } catch (error) {
      console.log("hai");
      console.error(`Error uploading to ${endpoint}:`, error);
      alert(`Failed to upload files to ${endpoint}`);
      return { success: false };
    }
  };
  

  const handleLoadDatabase = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
  
    const audioUploaded = await uploadFile(selectedAudioFile, "upload-database-audio");
    const imageUploaded = await uploadFile(selectedImageFile, "upload-database-image");
    const mapperUploaded = await uploadFile(selectedMapperFile, "upload-mapper");
  
    if (audioUploaded.success && imageUploaded.success && mapperUploaded.success) {
      setIsDatabaseLoaded(true);
      setCompTimeImage(imageUploaded.duration || "N/A");
      setCompTimeMusic(audioUploaded.duration || "N/A");
      alert("Database successfully uploaded!");
    }
  };
  
  const handleStart = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
  
    if (!isDatabaseLoaded) {
      alert("Please load the database before starting a query.");
      return;
    }
  
    if (!selectedQueryFile) {
      alert("No files selected!");
      return;
    }
  
    try {
      const formData = new FormData();
      formData.append("file", selectedQueryFile); // Single file is appended here
  
      const endpoint = type === "album" ? "start-query/image" : "start-query/audio";
      const response = await fetch(`http://localhost:8000/${endpoint}/`, {
        method: "POST",
        body: formData,
      });
  
      if (!response.ok) throw new Error("Failed to start query");
  
      const result = await response.json();
  
      setComputationTime(result.duration || "N/A");
      alert(result.message);
    } catch (error) {
      console.error("Error starting query:", error);
      alert("Failed to start query.");
    }
  };

  return (
    <div className="bg-opacity-40 bg-white-25 h-[80vh] rounded-[23px] p-6 flex flex-col items-center gap-2">
      {/* Query Upload Section */}
      <div className="w-full h-[200px] bg-white-50 rounded-xl flex items-center justify-center cursor-pointer">
        <label className="text-black font-medium flex flex-col items-center">
          {type === 'album' ? 'Upload Image' : 'Upload Humming'}
          <input
            type="file"
            accept={type === 'album' ? '.jpg,.jpeg,.png' : '.mid'}
            className="hidden"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setSelectedQueryFile(e.target.files?.[0] || null)
            }
          />
        </label>
      </div>
      <p className="text-sm text-white-25">
        Query: {selectedQueryFile ? selectedQueryFile.name : 'none'}
      </p>
      <button
        onClick={handleStart}
        className="text-blue-25 mt-5 w-full bg-yellow-25 hover:bg-amber-500 py-2 rounded-lg font-medium"
      >
        START
      </button>

      {/* File Upload Section */}
      <div className="file-upload-container w-full flex flex-col items-center">
      <FileUpload
        label="Dataset Audio"
        accept=".zip,.rar,.mid"
        file={selectedAudioFile}
        setFile={setSelectedAudioFile}
        multiple={true}
      />
      <FileUpload
        label="Dataset Image"
        accept=".zip,.rar,.jpg,.png,.jpeg"
        file={selectedImageFile}
        setFile={setSelectedImageFile}
        multiple={true}
      />
      <FileUpload
        label="Mapper"
        accept=".json,.txt"
        file={selectedMapperFile}
        setFile={setSelectedMapperFile}
      />
        <button
          onClick={handleLoadDatabase}
          className="text-bold mt-3 w-[80%] bg-white-25 hover:amebr py-2 rounded-lg font-medium text-blue-25"
        >
          Load Database
        </button>
        <div className='mt-5 text-white-25 text-sm' >
          {compTimeMusic ? (
            <p>Load Time Audio: {compTimeMusic} s</p>
          ) : (
            <p>Load Time Audio: Unknown</p>
          )}  
          {compTimeImage ? (
            <p>Load Time Image: {compTimeImage} s</p>
          ) : (
            <p>Load Time Image: Unknown</p>
          )}  
        </div>
        <div className='mt-3 text-white-25 text-sm'>
          {computationTime ? (
            <p>Query Time: {computationTime} s</p> 
          ) : (
            <p>Query Time: Unknown</p>
          )} 
        </div>
      </div>
    </div>
  );
}

type FileUploadProps = {
  label: string;
  accept: string;
  file: File[];
  setFile: React.Dispatch<React.SetStateAction<File[]>>;
  multiple?:boolean;
};

const FileUpload: React.FC<FileUploadProps> = ({ label, accept, file, setFile, multiple = false }) => (
  <>
    <label className="text-white-25 mt-4 w-full bg-pink-25 hover:bg-red-500 py-2 rounded-lg text-sm text-center cursor-pointer">
      {label}
      <input
        type="file"
        accept={accept}
        className="hidden"
        multiple={multiple} // Allow multiple file selection
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          setFile(e.target.files ? Array.from(e.target.files) : [])
        }
      />
    </label>
    <p className="text-sm text-white-25">
      Selected: {file.length > 0 ? file.map((file : File) => file.name).join(", ") : "none"}
    </p>
  </>
);