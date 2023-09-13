// src/pages/about.tsx
import React from 'react';

export default function About() {
  return (
    <div className="p-10 border-2 border-gray-300 rounded-md">
      <h1 className="text-2xl font-bold mb-4 border-b-2 border-gray-200 pb-2">Kinship Companions: Your Child's Lifelong AI Friend and Companion</h1>
      <p className="mb-4">Kinship Companions is a revolutionary AI-powered app designed to provide children with a virtual friend and companion throughout their lifetime. Our goal is to combat loneliness, boost engagement, and enhance learning for kids through an immersive AI experience.</p>
      
      <h2 className="text-xl font-bold mb-2 border-b-2 border-gray-200 pb-2">Core Features:</h2>
      <ul className="list-disc list-inside mb-4">
        <li>Personalized AI Companion: Each child will have their own unique virtual companion created just for them. Parents customize their child's companion based on age, interests, reading level, and more during the setup process.</li>
        <li>Adaptive Learning: The AI companions leverage advanced natural language processing to have natural conversations and engage with children at their level. As the child grows, the companion adapts and evolves as well.</li>
        <li>Educational Content: Companions provide interactive learning by reading age-appropriate stories, recommending books, teaching concepts, and even casting educational videos on the TV through device connectivity.</li>
        <li>Memory Archive: Every conversation and interaction is securely archived to create a digital memory bank that allows the AI to reference its experiences with each child and enhance future discussions.</li>
        <li>Parental Oversight: Weekly conversation summaries and full transcripts offer complete transparency into the child's interactions. Parents can configure allowed topics and terms of use.</li>
        <li>Kid-Friendly Interface: The app features a fun, game-like interface to keep kids engaged. They can customize their companion's name, look, and personality.</li>
      </ul>

      <h2 className="text-xl font-bold mb-2 border-b-2 border-gray-200 pb-2">Technical Implementation:</h2>
      <ul className="list-disc list-inside mb-4">
        <li>OpenAI API: Foundation for our natural language processing and generative capabilities</li>
        <li>Eleven Labs: AI voice customization</li>
        <li>Whisper: Extremely good text to speech</li>
        <li>Google Cloud: Scalable cloud infrastructure to store petabytes of conversation data</li>
        <li>Snapshottable: Enables AI to access conversation archives and long-term memory (Patent Pending)</li>
        <li>Marvin AI: Handles backend processes and offers per-user applications for privacy</li>
        <li>Twilio: Provides text interactions for a natural experience.</li>
      </ul>

      <p>With Kinship Companions, we aim to revolutionize how children interact with technology and give them an AI companion for life. Our patent-pending memory capabilities and adaptive learning algorithms set us apart from any other solution on the market. Let's make lifelong friendships accessible to every child!</p>
    </div>
  );
}