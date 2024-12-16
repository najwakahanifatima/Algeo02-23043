"use client"

import { useRouter } from "next/navigation";
import Navbar from "./navbar";

export default function Home() {
  const router = useRouter();
  return (
    <div>
      <Navbar/>
      <main className="text-left relative py-16 px-20 grid grid-flow-col scroll-smooth">
        <div>
          <h1 className="text-[6rem] font-extrabold text-gray-50 mb-[-75px]">Find Your</h1>
          <h1 className="text-[10rem] font-extrabold text-gray-50"> <span className="text-rose-400 font-extrabold">Muse</span>ic</h1>
          <p className="text-left text-gray-50 text-[1.25rem] ml-2">
            Music information retrieval and album finder <br/>
            using principal component analysis.
          </p>
            <a href="#viewmore">
            <button className="mt-10 object-left px-10 py-4 bg-yellow-500 text-gray-50 text-xl font-semibold rounded-full shadow hover:bg-yellow-600">
              View More
            </button> 
            </a>
          
        </div>
        <div className="justify-center ml-[100px]">
          <img src="homepage.png" alt="" className="w-[30rem] h-[30rem]" />
        </div>        
      </main>

      <div id='viewmore' className="bg-white-25 py-7 relative flex flex-col shadow-2xl">
        <div>
          <h2 className="text-4xl font-bold text-center text-blue-25">MuseIc Features</h2>
          <p className="text-gray-400 text-center">Click to Start</p>  
        </div>
        <div className="flex flex-row justify-evenly mt-5">
          <button 
            onClick={()=>router.push('/music_retrieval')}
            className="flex flex-col justify-center items-center bg-rose-400 w-full my-[2rem] mx-[6rem] rounded-3xl shadow-xl py-10           hover:bg-slate-500 hover:-translate-y-1">
              <img src="\Music Equalizer.svg" alt="" className="w-[10rem] h-[10rem]" />
              <p className="text-white-25 font-semibold text-4xl mt-7">Query by Humming</p>
          </button>
          <button 
            onClick={()=>router.push('/album_finder')}
            className="flex flex-col justify-center items-center bg-rose-400 w-full my-[2rem] mx-[6rem] rounded-3xl shadow-xl py-10
            hover:bg-slate-500 hover:-translate-y-1">
            <img src="\Music Folder Song.svg" alt="" className="w-[10rem] h-[10rem]" />
            <p className="text-white-25 font-semibold text-4xl mt-7">Album Finder PCA</p>
          </button>
        </div>
      </div>

      <div className="flex flex-col border m-8">
        <p className="font-bold text-white-25 text-4xl">The Contributors</p>
        <p className="text-white-25 text-lg mt-1">Kelompok Menjajal Nilai Maksimal</p>
        <div className="grid grid-cols-3 gap-5 justify-items-center mt-7 border">
            <div className="bg-yellow-25 px-12 py-2 rounded-3xl shadow-xl">
              Najwa Kahani Fatima - 13523043 - K01
            </div>
            <div className="bg-yellow-25 px-12 py-2 rounded-3xl shadow-xl">
              Mayla Yaffa Ludmilla - 13523050 - K02
            </div>
            <div className="bg-yellow-25 px-12 py-2 rounded-3xl shadow-xl">
              Nayla Zahira - 13523079 - K01
            </div>
        </div>
      </div>
    </div>
  );
}
