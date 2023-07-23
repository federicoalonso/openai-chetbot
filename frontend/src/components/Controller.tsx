import { useState } from 'react'
import Title from './Title';
import RecordMessage from './RecordMessage';
import axios from 'axios';

function Controller() {
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState<any[]>([]);

    const createBlobUrl = (data: any) => {
        const blob = new Blob([data], { type: 'audio/mpeg' });
        const url = window.URL.createObjectURL(blob);
        return url;
    };

    const handleStop = async (blobUrl: string) => {
        setIsLoading(true);

        const myMessage = {
            sender: "me",
            url: blobUrl,
        };
        const messageArr = [...messages, myMessage];

        // convert blob url to blob object
        fetch(blobUrl)
            .then((res) => res.blob())
            .then(async (blob) => {

                // construct audio to send file
                const formData = new FormData();
                formData.append("file", blob, "myFile.wav");

                // send file
                await axios.post("http://localhost:8000/post-audio", formData, {
                    headers: {
                        "Content-Type": "audio/mpeg",
                    },
                    responseType: "arraybuffer",
                }).then((res: any) => {
                    const blob = res.data;
                    const audio = new Audio();
                    audio.src = createBlobUrl(blob);

                    const bellaMessage = {
                        sender: "Bella",
                        url: audio.src,
                    };
                    messageArr.push(bellaMessage);
                    setMessages(messageArr);

                    // play audio

                    setIsLoading(false);
                    audio.play();
                }).catch((err: any) => {
                    console.log(err.message);
                    setIsLoading(false);
                });

            });
    };

    return (
        <div className='h-screen overflow-y-hidden'>
            <Title setMessages={setMessages} />
            <div className='felx flex-col justify-between h-full overflow-y-scroll pb-96'>
                { /* Messages */}
                <div className='mt-5 px-5'>
                    {messages.slice().reverse().map((audio, index) => {
                        return <div key={index + audio.sender} className={'flex flex-col ' + (audio.sender == "Bella" && "flex items-end")}>
                            {/* Sender */}
                            <div className='mt-4'>
                                <p className={audio.sender == "Bella" ? "text-right mr-2 italic text-green-500" : "ml-2 italic text-blue-500"}>
                                    {audio.sender}
                                </p>

                                {/* Audio */}
                                <audio src={audio.url} className='appearence-none' controls />
                            </div>
                        </div>
                    })}

                    {messages.length == 0 && !isLoading && (
                        <div className='text-center font-light italic mt-10'>
                            Send Bella a message...
                        </div>
                    )}

                    {isLoading && (
                        <div className='text-center font-light italic mt-10 animate-pulse'>
                            Give me a second...
                        </div>
                    )}
                </div>

                { /* Recorder */}
                <div className='fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500'>
                    <div className='flex justify-center items-center w-full'>
                        <RecordMessage handleStop={handleStop} />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Controller