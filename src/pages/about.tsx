import React from 'react';
import "@/app/globals.css";
import Image from 'next/image';


export default function About() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between bg-gray-900 px-6 py-24 shadow-2xl sm:px-24 xl:py-32">
      <div className="w-full max-w-2xl mx-auto text-center text-4xl font-medium text-white sm:text-5xl">
        <h1 className="font-bold mb-4 border-b-2 border-gray-200 pb-2">Kinship Companions: Your Child&apos;s Lifelong AI Friend and Companion</h1>
          <p className="mx-auto mt-4 max-w-xl text-center text-xl leading-8 text-slate-400">Kinship Companions is a revolutionary AI-powered app designed to provide children with a virtual friend and companion throughout their lifetime. Our goal is to combat loneliness, boost engagement, and enhance learning for kids through an immersive AI experience.</p>
          <div className='m-4'></div>
          <h2 className="font-bold mb-2 border-b-2 border-gray-200 pb-2">Core Features:</h2>
          <ul className="mx-auto mt-4 max-w-xl text-center text-xl leading-8 text-slate-400">
            <li className='mb-6'><span className="font-bold my-3">Personalized AI Companion:</span> Each child will have their own unique virtual companion created just for them. Parents customize their child&apos;s companion based on age, interests, reading level, and more during the setup process.</li>
            <li className="mb-6"><span className="font-bold my-3">Adaptive Learning:</span> The AI companions leverage advanced natural language processing to have natural conversations and engage with children at their level. As the child grows, the companion adapts and evolves as well.</li>
            <li className='mb-6'><span className="font-bold my-3">Educational Content:</span> Companions provide interactive learning by reading age-appropriate stories, recommending books, teaching concepts, and even casting educational videos on the TV through device connectivity.</li>
            <li className='mb-6'><span className="font-bold my-3">Memory Archive:</span> Every conversation and interaction is securely archived to create a digital memory bank that allows the AI to reference its experiences with each child and enhance future discussions.</li>
            <li className='mb-6'><span className="font-bold my-3">Parental Oversight:</span> Weekly conversation summaries and full transcripts offer complete transparency into the child&apos;s interactions. Parents can configure allowed topics and terms of use.</li>
            <li className='mb-6'><span className="font-bold my-3">Kid-Friendly Interface:</span> The app features a fun, game-like interface to keep kids engaged. They can customize their companion&apos;s name, look, and personality.</li>
          </ul>

          <div className='m-4'></div><div className='m-4'></div>
          <h2 className="font-bold mb-2 border-b-2 border-gray-200 pb-2">Founder</h2>
          <Image className="rounded-full" src="/headshot.png" alt="Connor Duffy" width={500} height={500} />
          <h3 className="font-medium mb-2">Connor Duffy</h3>

      </div>
    </main>
  );
}