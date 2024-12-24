import React from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import {useEffect, useState} from 'react'

export default function Statistiques(props) {

    ChartJS.register(ArcElement, Tooltip, Legend);

    const tweets_recuperes = props.tweets_recuperes
    let [categories, setCategories] = useState( {
        Positif:[] ,
        Neutre:[] ,
        Négatif:[] ,
    } )

    useEffect(() => {
        let newCategories = {Positif:[], Neutre:[], Négatif:[]}
        tweets_recuperes.forEach( (tweet) => {
            if (tweet['annote'] === 4) {
                newCategories.Positif.push(tweet)
            } else if (tweet['annote'] === 2) {
                newCategories.Neutre.push(tweet)
            } else {
                newCategories.Négatif.push(tweet)
            }
        })
        setCategories(newCategories)
    }, [tweets_recuperes])

    const nombre_tweets_positifs = categories.Positif.length
    const nombre_tweets_neutres = categories.Neutre.length
    const nombre_tweets_negatifs = categories.Négatif.length

    const data = {
        labels: Object.keys(categories),
        datasets: [
            {
                label: 'Nombre de Tweets',
                data: [nombre_tweets_positifs, nombre_tweets_neutres, nombre_tweets_negatifs],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className="w-1/4 p-2 text-black bg-white rounded-xl">
            <p> Statistiques :</p>
            <Pie data={data} />
        </div>
    )
}