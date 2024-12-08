import React from "react";

export default function SideBar(){
    return(
        <div className="bg-opacity-40 bg-white-25 h-[80vh] rounded-[23px] p-6 flex flex-col items-center gap-2">
            <div className="w-full h-[200px] bg-white-50 rounded-lg flex items-center justify-center">
                <span className="text-black font-medium">upload humming</span>
            </div>
            <p className="text-sm text-white-25">Query: yyyy.zip</p>
            <button className="text-white-25 mt-5 w-full bg-pink-25 hover:bg-red-500 text-white py-2 rounded-lg font-medium">
                Dataset Audio
            </button>
            <p className="text-sm text-white-25">Song: xxxx.zip</p>
            <button className="text-white-25 mt-1 w-full bg-pink-25 hover:bg-red-500 text-white py-2 rounded-lg font-medium">
                Dataset Image
            </button>
            <p className="text-sm text-white-25">Image: xxxx.zip</p>
            <button className="text-white-25 mt-1 w-full bg-pink-25 hover:bg-red-500 text-white py-2 rounded-lg font-medium">
                Mapper
            </button>
            <p className="text-sm text-white-25">Mapper: xxxx.json</p>
        </div>
    )
}