import { useState } from 'react'

export default function NombreTweets(props){

    return(
        <div className="p-2 w-72 text-black ">
            <p> Nombre de tweets :</p>
            <div className="mt-1 relative w-full cursor-default overflow-hidden rounded-lg bg-white text-left shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-teal-300 sm:text-sm">
                <input
                    className="w-full border-none py-2 pl-3 pr-10 text-sm leading-5 text-gray-900 focus:ring-0"
                    type="number"
                    min={0}
                    max={1000}
                    value={props.nombreTweets}
                    onChange={(event) => props.setNombreTweets(event.target.value)}
                />
            </div>
        </div>
    )
}