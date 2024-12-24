import {useEffect, useState} from 'react'
import { Tab } from '@headlessui/react'
import Tweet from "./Tweet";

function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

export default function AfficherTweets( props ) {
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



    return (
        <div className="w-2/5 px-2 py-16 sm:px-0">
            <Tab.Group>
                <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1">
                    {Object.keys(categories).map((category) => (
                        <Tab
                            key={category}
                            className={({ selected }) =>
                                classNames(
                                    'w-full rounded-lg py-2.5 text-sm font-medium leading-5 text-blue-700',
                                    'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                                    selected
                                        ? 'bg-white shadow'
                                        : 'text-blue-100 hover:bg-white/[0.12] hover:text-white'
                                )
                            }
                        >
                            {category}
                        </Tab>
                    ))}
                </Tab.List>
                <Tab.Panels className="mt-2">
                    {Object.values(categories).map((posts, idx) => (
                        <Tab.Panel
                            key={idx}
                            className={classNames(
                                'rounded-xl bg-white p-3',
                                'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2'
                            )}
                        >
                            <ul className="max-h-96 overflow-auto ">
                                {posts.map((post) => (
                                    <Tweet post={post} urlMotCle={props.urlMotCle} />
                                ))}
                            </ul>
                        </Tab.Panel>
                    ))}
                </Tab.Panels>
            </Tab.Group>
        </div>
    )
}
