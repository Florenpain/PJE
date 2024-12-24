import Notation from "./Notation";


export default function Tweet(props) {

    return (
        <li
            key={ props.post['id'] }
            className="relative rounded-md p-3 flex flex-row justify-between"
        >
            <div>
                <h3 className="text-sm font-medium leading-5 text-black">
                    {props.post['text']}
                </h3>

                <p className="mt-1 flex space-x-1 text-xs font-normal leading-4 text-gray-500">
                    Tweet partagé le {props.post['created_at'].substring(0, 10)} à {props.post['created_at'].substring(11,19)}
                </p>
            </div>
            <div>
                <Notation post={props.post} urlMotCle={props.urlMotCle}/>
            </div>
        </li>
    )
}