import React, { useState, useEffect } from "react";
import Pagination from "./pagination";
import mapper from "../../../backend/database/mapper/mapper.json";



interface MainContainerProps {
  showQueryType: boolean;
  queryType: string;
}

interface MergedData {
  title: string;
  percentage: string;
  image: string;
}

const MainContainer: React.FC<MainContainerProps> = ({ showQueryType, queryType }) => {

  const [mergedData, setMergedData] = useState<MergedData[]>([]);
  const fetchData = async () => {
    try {
      const query = await import("../../../backend/database/query/query.json");
      return query
    } catch (err) {
      alert("Error loading query data: " + err);
      return null;
    }};
      
  useEffect(() => {
    const fetchDataAndCombine = async () => {
    
      try {
        // Fetch images
        const response = await fetch("http://127.0.0.1:8000/images");
        const images = await response.json();

        // Determine combined data based on `showQueryType` and `queryType`
        let combinedData: MergedData[] = [];

        if (!showQueryType) {
          // Default case: If `showQueryType` is false
          combinedData = mapper.map((item) => {
            const image = images.find((img) => img.name === item.pic_name);
            return {
              title: item.title,
              percentage: "0", // Default percentage
              image: image ? `http://localhost:8000${image.url}` : "Image not found",
            };
          });
        } else if (queryType === "music" || queryType === "album") {
          combinedData = (query.music as [string, number][]).map(([audioFile, percentage]) => {
            const percentageItem = mapper.find((p) => p.audio_file === audioFile);

            if (percentageItem) {
              const image = images.find((img) => img.name === percentageItem.pic_name);
              return {
                title: percentageItem.title,
                percentage: percentage.toString(),
                image: image ? `http://localhost:8000${image.url}` : "Image not found",
              };
            }
            return null; // Return null if no match
          }).filter((item) => item !== null) as MergedData[];
        }

        // Update merged data state
        setMergedData(combinedData);
      } catch (error) {
        console.error("Error fetching or combining data:", error);
      }
    };

    fetchDataAndCombine();
  }, [showQueryType, queryType]); // Re-run only if these props change

  return (
    <div className="pb-4">
      <div className="text-center text-white-25 font-semibold justify-items-stretch mb-4">
        <div>
          Result: <span className="text-yellow-25 font-bold">{mergedData.length}</span> Data
        </div>
      </div>
      <Pagination items={mergedData} itemsPerPage={12} />
    </div>
  );
};

export default MainContainer;
