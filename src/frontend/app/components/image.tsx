"use client";

import React from "react";
import SideBar from "./sidebar";
import { useRouter } from "next/navigation";

export default function ImageRetrieval(){
    const router = useRouter()
    return(
        <div className="flex flex-col">
            {/*Navigation Bar*/}
            <div className="flex flex-row border align-middle justify-between mt-3">
                {/*Left Component*/}
                <div className="flex flex-row gap-5 ml-7"> 
                    <button>
                        <img src="\Home 3.svg" alt="" className="w-6 h-6 pb-0.5"/>
                    </button>
                    <button>
                        <img src="\MuseIc.svg" alt="" className="w-20"/>
                    </button>
                </div>
                {/*Right Components*/}
                <div className="flex flex-row align-middle justify-items-center">
                    <button 
                        onClick={()=>router.push("/music_retrieval")}
                        className="button-navbar-off">
                        <img src="\Music Equalizer.svg" alt="" className="w-5 h-5" />
                        <span className="text-white"> Music Retrieval </span>
                    </button>
                    <button className="button-navbar-on">
                        <img src="\Music Folder Song.svg" alt="" className="w-5 h-5" />
                        <span className="text-white"> Album Finder </span>
                    </button>
                </div>
            </div>
            {/*Body*/}
            <div className="grid grid-cols-5 gap-8 ml-7 mr-7 mt-10">
                {/*Side Bar*/}
                <SideBar/>
                {/*Main Page Bar*/}
                <div className="border col-span-4">
                    Main Container
                </div>
            </div>
        </div>
        
    )
}
