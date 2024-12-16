import React from 'react'
import { useState } from 'react';

interface CardProperties {
  title: string;
  percentage: number;
  image: string;
}

const AudioBox: React.FC<CardProperties> = ({ title, percentage, image }) => {

  return (
    <div className='flex flex-col flex-wrap place-content-center'>
        <div className="w-[250px] h-[130px] bg-white-50 rounded-3xl flex items-center justify-center overflow-hidden shadow-xl">
            <img 
            className='w-full h-full object-cover'
            src={image}
            alt="" />          
        </div>
        <div className='flex flex-row'>
          <div className="w-[195px] h-[37px] bg-rose-400 rounded-l-2xl place-content-center mt-2 shadow-md">
            <p className="text-white-25 text-center align-middle text-md">{title}</p>
          </div>
          <div className='w-[50px] h-[37px] ml-[5px] bg-yellow-25 rounded-r-xl place-content-center mt-2 shadow-md'>
            <p className='text-white-25 text-center align-middle text-sm'>{percentage}%</p>
          </div>
        </div>
        
        
    </div>
    );
};

export default AudioBox;

