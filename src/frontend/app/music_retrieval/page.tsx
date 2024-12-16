"use client";

import React, { useState } from "react";
import Sidebar from "../components/sidebar";
import { useRouter } from "next/navigation";
import MainContainer from "../components/maincontainer";

const MusicRetrieval: React.FC = () => {
	const [showType, setshowType] = useState(false);
	
	// Callback to handle query result
	const handleQueryResult = (isStarted: boolean) => {
		setshowType(true);
	};
  	
	const router = useRouter()

	return (
		<div className="flex flex-col">
			<div className="flex flex-row align-middle justify-between mt-3 w-full z-50 border-b-2 pb-2">
				{/*Left Component*/}
				<div className="flex flex-row gap-5 ml-7"> 
					<button>
						<img 
						onClick={()=>router.push('/')}
						src="\Home 3.svg" alt="" className="w-6 h-6 pb-0.5"/>
					</button>
					<button>
						<img 
						onClick={()=>router.push('/')}
						src="\MuseIc.svg" alt="" className="w-20"/>
					</button>
				</div>
			{/*Right Components*/}
				<div className="flex flex-row align-middle justify-items-center">
					<button 
						onClick={()=>router.push("/music_retrieval")}
						className="button-navbar-off bg-yellow-25">
						<img src="\Music Equalizer.svg" alt="" className="w-5 h-5" />
						<span className="text-white"> Music Retrieval </span>
					</button>
					<button
						onClick={()=>router.push("/album_finder")}
						className="button-navbar-off">
						<img src="\Music Folder Song.svg" alt="" className="w-5 h-5" />
						<span className="text-white"> Album Finder </span>
					</button>
				</div>
			</div>
			{/*Body*/}
			<div className="grid grid-cols-5 gap-8 ml-7 mr-7 mt-10">
				{/*Side Bar*/}
				<Sidebar 
				type="music" 
        		onQueryResult={handleQueryResult}/>
				{/*Main Page Bar*/}
				<div className="border col-span-4">
					<MainContainer showQueryType={showType} queryType="music" />
				</div>
			</div>
		</div>
	);
};

export default MusicRetrieval;
