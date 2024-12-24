import './App.css';
import SelectionMotCle from "./components/SelectionMotCle";
import NombreTweets from "./components/NombreTweets";
import ChoixClassifieur from "./components/ChoixClassifieur";
import AfficherTweets from "./components/AfficherTweets";
import Statistiques from "./components/Statistiques";
import ChoixLangue from "./components/ChoixLangue";
import React, {useEffect, useState} from 'react'

const motsCles = [
    { id: 1, name: 'Equipe de France', urlCSV: 'ressources/Equipe_de_France.csv' },
    { id: 2, name: 'Présidentielles', urlCSV: 'ressources/Presidentielles.csv' },
    { id: 3, name: 'Anneaux de pouvoir', urlCSV: 'ressources/anneaux_de_pouvoir.csv' },
    { id: 4, name: 'Elon Musk', urlCSV: 'ressources/elon_musk.csv' },
    { id: 5, name: 'World Cup', urlCSV: 'ressources/world_cup.csv' },
]

const classifieurs = [
    { name: 'Naïf' },
    { name: 'KNN' },
    { name: 'Bayesien V1' },
    { name: 'Bayesien V2' },
]

const langues = [
    { name: 'Francais', code: 'fr' },
    { name: 'Anglais', code: 'en' },
]

function App() {

    const [motCle, setMotCle] = useState(motsCles[0]);
    const [langue, setLangue] = useState(langues[0]);
    const [classifieur, setClassifieur] = useState(classifieurs[0]);
    const [nombreVoisins, setNombreVoisins] = useState(2);
    const [nombreTweets, setNombreTweets] = useState(20);
    const [tweetsRecuperes, setTweetsRecuperes] = useState([]);

    const [motCleAffichage, setMotCleAffichage] = useState(motsCles[0]);
    const [tempsExecution, setTempsExecution] = useState(0);

    /*
    const testAPI = () => {
        fetch('http://127.0.0.1:8000/test', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => console.log(data));
    }
     */

    const recuperer_tweets = async () => {
        var start = new Date().getTime();
        const response = await fetch('http://localhost:8000/recent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "mot_cle": motCle.name,
                "url": motCle.urlCSV,
                "nombre_tweets": nombreTweets,
                "classifieur": classifieur.name,
                "langue": langue.code,
                "nombre_voisins": nombreVoisins,
            }),
            AccessControlAllowOrigin: 'no-cors',
        })
        const data = await response.json()
        const parseData = JSON.parse(data)
        setTweetsRecuperes(parseData)
        setMotCleAffichage(motCle)
        var end = new Date().getTime();
        setTempsExecution(end - start);

    }

  return (
    <div className="App min-h-screen bg-gray-500">
      <header className="App-header bg-black text-white">
        <h1>Opi'Twitter</h1>
        <strong>Développé par Corentin Duvivier et Florentin Bugnon</strong>
      </header>

      <main className="text-white min-h-fit">
        <div className="flex flex-col items-center justify-center">
            <div className="flex flex-col items-center justify-center">
                <p> Temps d'éxécution du classifieur : <strong> {tempsExecution} </strong> ms</p>
            </div>
          <div className=" flex flex-row " >
              <SelectionMotCle motCle={motCle} setMotCle={setMotCle} motsCles={motsCles}/>
              <NombreTweets nombreTweets={ nombreTweets} setNombreTweets={setNombreTweets}/>
              <ChoixClassifieur classifieur={classifieur} setClassifieur={setClassifieur} classifieurs={classifieurs} nombreVoisins={nombreVoisins} setNombreVoisins={setNombreVoisins} />
              <ChoixLangue langue={langue} setLangue={setLangue} langues={langues}/>
          </div>
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={recuperer_tweets}> lancer </button>
        </div>
      <div className="m-2 flex flex-wrap items-center justify-around">
            <AfficherTweets tweets_recuperes={tweetsRecuperes} urlMotCle={motCleAffichage.urlCSV}/>
            <Statistiques tweets_recuperes={tweetsRecuperes}/>
      </div>
      </main>

    </div>
  );
}

export default App;
