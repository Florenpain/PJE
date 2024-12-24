// import {useState} from "react";

export default function Notation(props) {
    // const [notation, setNotation] = useState(0);

    const annoter = async ( annotation ) => {
        const response = await fetch('http://127.0.0.1:8000/annotation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id_tweet: props.post.id,
                urlBase: props.urlMotCle,
                annotation: annotation,
            })
        })
        const data = await response.json()
        console.log(data)
    }

    return(
        <div className="p-2 flex flex-row">
            <button onClick={() => annoter(4)}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="black" className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </button>
            <button onClick={() => annoter(2)}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="black" className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 9h16.5m-16.5 6.75h16.5" />
                </svg>
            </button>
            <button onClick={() => annoter(0)}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="black" className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

        </div>
    )
}