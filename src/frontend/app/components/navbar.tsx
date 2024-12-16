"use client";

import React from 'react'
import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter()
  return (
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
                  className="button-navbar-off">
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
  )
}