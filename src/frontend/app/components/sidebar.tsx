import React from "react";

export default function SideBar({ type }) {
    const [selectedAudioFile, setSelectedAudioFile] = useState(null);
    const [selectedImageFile, setSelectedImageFile] = useState(null);
    const [selectedMapperFile, setSelectedMapperFile] = useState(null);
    const [selectedQueryFile, setSelectedQueryFile] = useState(null);
    const [isDatabaseLoaded, setIsDatabaseLoaded] = useState(false);

    const handleDatabaseAudio = async () => {
        if (!selectedAudioFile) {
            alert('Please select an audio file.');
            return false;
        }

        const formData = new FormData();
        formData.append('file', selectedAudioFile);

        try {
            const response = await fetch('http://localhost:8000/upload-database-audio/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Failed to upload audio file');

            const result = await response.json();
            alert(result.message);
            return true;
        } catch (error) {
            alert('Audio database upload failed!');
            setSelectedAudioFile(null);
            return false;
        }
    };

    const handleDatabaseImage = async () => {
        if (!selectedImageFile) {
            alert('Please select an image file.');
            return false;
        }

        const formData = new FormData();
        formData.append('file', selectedImageFile);

        try {
            const response = await fetch('http://localhost:8000/upload-database-image/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Failed to upload image file');

            const result = await response.json();
            alert(result.message);
            return true;
        } catch (error) {
            alert('Image upload failed!');
            setSelectedImageFile(null);
            return false;
        }
    };

    const handleMapper = async () => {
        if (!selectedMapperFile) {
            alert('Please select a mapper file.');
            return false;
        }

        const formData = new FormData();
        formData.append('file', selectedMapperFile);

        try {
            const response = await fetch('http://localhost:8000/upload-mapper/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Failed to upload mapper file');

            const result = await response.json();
            alert(result.message);
            return true;
        } catch (error) {
            alert('Mapper upload failed!');
            setSelectedMapperFile(null);
            return false;
        }
    };

    const handleLoadDatabase = async (e) => {
        e.preventDefault();
        const audioUploaded = await handleDatabaseAudio();
        const imageUploaded = await handleDatabaseImage();
        const mapperUploaded = await handleMapper();

        if (audioUploaded && imageUploaded && mapperUploaded) {
            setIsDatabaseLoaded(true);
            alert('Database successfully loaded!');
        }
    };

    const handleStart = async (e) => {
        e.preventDefault();
        if (!isDatabaseLoaded) {
            alert('Please load the database before starting a query.');
            return;
        }

        if (!selectedQueryFile) {
            alert('Please select a query file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedQueryFile);

        try {
            const response = await fetch('http://localhost:8000/start-query/', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Failed to start query');

            const result = await response.json();
            alert(result.message);
        } catch (error) {
            alert('Query process failed!');
            setSelectedQueryFile(null);
        }
    };

    return (
        <div className="bg-opacity-40 bg-white-25 h-[80vh] rounded-[23px] p-6 flex flex-col items-center gap-2">
            <div className="w-full h-[200px] bg-white-50 rounded-lg flex items-center justify-center">
                <span className="text-black font-medium">upload humming</span>
            </div>
            <p className="text-sm text-white-25">Query: yyyy.zip</p>
            <button className="text-black font-bold mt-5 w-full bg-yellow-25 hover:bg-amber-500 py-2 rounded-lg font-medium">
                START
            </button>
            <button className="text-white-25 mt-4 w-full bg-pink-25 hover:bg-red-500 py-2 rounded-lg font-medium">
                Dataset Audio
            </button>
            <p className="text-sm text-white-25">Song: xxxx.zip</p>
            <button className="text-white-25 mt-1 w-full bg-pink-25 hover:bg-red-500 py-2 rounded-lg font-medium">
                Dataset Image
            </button>
            <p className="text-sm text-white-25">Image: xxxx.zip</p>
            <button className="text-white-25 mt-1 w-full bg-pink-25 hover:bg-red-500 py-2 rounded-lg font-medium">
                Mapper
            </button>
            <p className="text-sm text-white-25">Mapper: xxxx.json</p>
        </div>
    )
}