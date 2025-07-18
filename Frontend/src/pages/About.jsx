import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

const About = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const teamMembers = [
    {
      name: "Yashodip More",
      role: "Team Lead & Full Stack Developer",
      email: "yashodipmore2004@gmail.com",
      avatar: "YM",
      skills: ["React", "Node.js", "MongoDB", "Express","Python"]
    },
    {
      name: "Komal Kumavat",
      role: "Frontend Developer & UI/UX Designer",
      email: "komalkumavat025@gmail.com",
      avatar: "KK",
      skills: ["React", "Tailwind CSS", "JavaScript", "UI/UX"]
    },
    {
      name: "Bibaswan Das",
      role: "AI/ML Engineer & Computer Vision",
      email: "bibaswand04@gmail.com",
      avatar: "BD",
      skills: ["Python", "TensorFlow", "Computer Vision", "OpenCV"]
    },
    {
      name: "Barun Saha",
      role: "AI/ML Engineer & Data Processing",
      email: "barun.vsaha@gmail.com",
      avatar: "BS",
      skills: ["Python", "PyTorch", "Machine Learning", "Data Analysis"]
    },
    {
      name: "S.M. Sakthivel",
      role: "Database Developer",
      email: "m.sakthivelofficial@gmail.com",
      avatar: "SS",
      skills: ["Firebase", "SQLlite", "PL/SQL", "MongoDB","AWS"]
    }
  ];

  const mentor = {
    name: "Dr. Niranjan Deshpande",
    role: "Project Mentor",
    qualification: "PhD in Autonomous Driving & Robotics",
    email: "niranjan.deshpande@college.edu",
    avatar: "ND",
    expertise: ["Autonomous Systems", "Robotics", "AI Research", "Computer Vision"]
  };

  const techStack = {
    frontend: [
      { name: "React 18", description: "Modern UI library with hooks" },
      { name: "Tailwind CSS", description: "Utility-first CSS framework" },
      { name: "JavaScript ES6+", description: "Modern JavaScript features" },
      { name: "i18next", description: "Internationalization support" }
    ],
    backend: [
      { name: "Python", description: "Core backend language" },
      { name: "FastAPI", description: "High-performance API framework" },
      { name: "TensorFlow", description: "Machine learning framework" },
      { name: "OpenCV", description: "Computer vision library" }
    ],
    database: [
      { name: "MongoDB", description: "NoSQL document database" },
      { name: "Redis", description: "In-memory data store" },
      { name: "AWS S3", description: "Cloud file storage" },
      { name: "PostgreSQL", description: "Relational database" }
    ],
    tools: [
      { name: "Docker", description: "Containerization platform" },
      { name: "Git", description: "Version control system" },
      { name: "VS Code", description: "Development environment" },
      { name: "Postman", description: "API testing tool" }
    ]
  };

  const projectStats = [
    { value: "95%", key: "accuracy" },
    { value: "4", key: "coreModules" },
    { value: "3", key: "languagesSupported" },
    { value: "5", key: "teamMembers" },
    { value: "24/7", key: "availability" },
    { value: "100%", key: "ecoFriendly" }
  ];

  const hackathonInfo = {
    name: "Anan.ai Hackathon 2025",
    theme: "Sustainable Agriculture Technology",
    focus: "AI-driven solutions for environmental challenges",
    duration: "48 hours",
    participants: "100+ teams nationwide"
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 font-['Poppins',sans-serif]">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-100/20 to-pink-100/20"></div>
      <div className="absolute top-20 left-20 w-64 h-64 bg-indigo-200/30 rounded-full blur-3xl"></div>
      <div className="absolute bottom-20 right-20 w-80 h-80 bg-pink-200/30 rounded-full blur-3xl"></div>
      
      <div className="relative z-10 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="text-center mb-16">
              <div className="inline-flex items-center bg-white/80 backdrop-blur-sm rounded-full px-6 py-2 mb-6 shadow-lg">
                <span className="w-2 h-2 bg-purple-500 rounded-full mr-2 animate-pulse"></span>
                <span className="text-purple-700 font-medium">{t('about.badge')}</span>
              </div>
              
              <h1 className="text-6xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-6">
                {t('about.title')}
              </h1>
              <p className="text-2xl text-gray-600 max-w-4xl mx-auto">
                {t('about.subtitle')}
              </p>
            </div>

            {/* Project Stats */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-16">
              {projectStats.map((stat, index) => (
                <div key={index} className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 text-center shadow-xl transform hover:scale-105 transition-all duration-300">
                  <div className="text-3xl font-bold text-indigo-600 mb-1">{stat.value}</div>
                  <div className="text-sm text-gray-600">{t(`about.achievements.${stat.key}`)}</div>
                </div>
              ))}
            </div>

            {/* Hackathon Information */}
            <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-2xl p-8 text-center text-white mb-16">
              <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-8">
                <h2 className="text-3xl font-bold mb-4">{t('aboutPage.hackathonTitle')}</h2>
                <div className="grid md:grid-cols-2 gap-6 text-left">
                  <div>
                    <h3 className="text-xl font-semibold mb-3">{t('aboutPage.eventDetails')}</h3>
                    <div className="space-y-2">
                      <p><span className="font-medium">{t('aboutPage.event')}:</span> {hackathonInfo.name}</p>
                      <p><span className="font-medium">{t('aboutPage.theme')}:</span> {hackathonInfo.theme}</p>
                      <p><span className="font-medium">{t('aboutPage.duration')}:</span> {hackathonInfo.duration}</p>
                      <p><span className="font-medium">{t('aboutPage.participants')}:</span> {hackathonInfo.participants}</p>
                    </div>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-3">{t('aboutPage.projectFocus')}</h3>
                    <p className="mb-4">{hackathonInfo.focus}</p>
                    <div className="flex flex-wrap gap-2">
                      {['Innovation', 'Sustainability', 'AI/ML', 'Agriculture', 'Environment', 'Technology'].map((tag, index) => (
                        <span key={index} className="bg-white/30 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium">
                          {t(`aboutPage.tags.${tag.toLowerCase()}`)}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Project Description */}
            <div className="grid md:grid-cols-2 gap-8 mb-16">
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-gray-100">
                <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                  <svg className="w-8 h-8 text-indigo-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  {t('about.mission.title')}
                </h2>
                <p className="text-gray-600 leading-relaxed mb-4">
                  {t('about.mission.description1')}
                </p>
                <p className="text-gray-600 leading-relaxed">
                  {t('about.mission.description2')}
                </p>
              </div>

              <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-gray-100">
                <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                  <svg className="w-8 h-8 text-purple-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {t('about.vision.title')}
                </h2>
                <p className="text-gray-600 leading-relaxed mb-4">
                  {t('about.vision.description1')}
                </p>
                <p className="text-gray-600 leading-relaxed">
                  {t('about.vision.description2')}
                </p>
              </div>
            </div>

            {/* Features */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 mb-16 border border-gray-100">
              <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">{t('aboutPage.keyFeatures')}</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="text-center group">
                  <div className="w-16 h-16 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-2xl flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-800 mb-2">{t('aboutPage.aiImageRecognition')}</h3>
                  <p className="text-gray-600 text-sm">{t('aboutPage.aiImageRecognitionDesc')}</p>
                </div>

                <div className="text-center group">
                  <div className="w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-2xl flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-800 mb-2">{t('aboutPage.smartRecommendations')}</h3>
                  <p className="text-gray-600 text-sm">{t('aboutPage.smartRecommendationsDesc')}</p>
                </div>

                <div className="text-center group">
                  <div className="w-16 h-16 bg-gradient-to-br from-purple-400 to-indigo-500 rounded-2xl flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-800 mb-2">{t('aboutPage.environmentalImpact')}</h3>
                  <p className="text-gray-600 text-sm">{t('aboutPage.environmentalImpactDesc')}</p>
                </div>

                <div className="text-center group">
                  <div className="w-16 h-16 bg-gradient-to-br from-pink-400 to-red-500 rounded-2xl flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                    </svg>
                  </div>
                  <h3 className="font-bold text-gray-800 mb-2">{t('aboutPage.carbonCredits')}</h3>
                  <p className="text-gray-600 text-sm">{t('aboutPage.carbonCreditsDesc')}</p>
                </div>
              </div>
            </div>

            {/* Team Section */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 mb-16 border border-gray-100">
              <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">{t('about.team.title')}</h2>
              
              {/* Mentor */}
              <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-6 mb-8">
                <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">{t('aboutPage.projectMentor')}</h3>
                <div className="text-center">
                  <div className="bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl p-6 max-w-sm mx-auto">
                    <div className="text-6xl mb-4">{mentor.avatar}</div>
                    <h4 className="font-bold text-gray-800 mb-2">{mentor.name}</h4>
                    <p className="text-indigo-600 font-medium mb-2">{mentor.qualification}</p>
                    <p className="text-purple-600 font-medium mb-3">{mentor.role}</p>
                    <div className="flex flex-wrap justify-center gap-2 mb-4">
                      {mentor.expertise.map((skill, skillIndex) => (
                        <span key={skillIndex} className="bg-white px-2 py-1 rounded-full text-xs text-gray-600">
                          {skill}
                        </span>
                      ))}
                    </div>
                    <div className="text-sm text-purple-600 break-words">
                      {mentor.email}
                    </div>
                  </div>
                </div>
              </div>

              {/* Team Members */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                {teamMembers.map((member, index) => (
                  <div key={index} className="text-center group">
                    <div className="bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
                      <div className="text-6xl mb-4">{member.avatar}</div>
                      <h3 className="font-bold text-gray-800 mb-2">{member.name}</h3>
                      <p className="text-indigo-600 font-medium mb-3">{member.role}</p>
                      <div className="flex flex-wrap justify-center gap-2 mb-4">
                        {member.skills.map((skill, skillIndex) => (
                          <span key={skillIndex} className="bg-white px-2 py-1 rounded-full text-xs text-gray-600">
                            {skill}
                          </span>
                        ))}
                      </div>
                      <div className="text-sm text-purple-600 break-words">
                        {member.email}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Technology Stack */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 mb-16 border border-gray-100">
              <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">{t('aboutPage.technologyStack')}</h2>
              
              {/* Frontend */}
              <div className="mb-8">
                <h3 className="text-xl font-bold text-indigo-600 mb-4 flex items-center">
                  <span className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></span>
                  {t('aboutPage.frontendTechnologies')}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {techStack.frontend.map((tech, index) => (
                    <div key={index} className="bg-gradient-to-br from-indigo-50 to-blue-50 rounded-xl p-4 text-center hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                      <span className="font-medium text-gray-700 block mb-1">{tech.name}</span>
                      <span className="text-xs text-gray-500">{tech.description}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Backend */}
              <div className="mb-8">
                <h3 className="text-xl font-bold text-purple-600 mb-4 flex items-center">
                  <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                  {t('aboutPage.backendAI')}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {techStack.backend.map((tech, index) => (
                    <div key={index} className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 text-center hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                      <span className="font-medium text-gray-700 block mb-1">{tech.name}</span>
                      <span className="text-xs text-gray-500">{tech.description}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Database */}
              <div className="mb-8">
                <h3 className="text-xl font-bold text-emerald-600 mb-4 flex items-center">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full mr-2"></span>
                  {t('aboutPage.databaseStorage')}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {techStack.database.map((tech, index) => (
                    <div key={index} className="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl p-4 text-center hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                      <span className="font-medium text-gray-700 block mb-1">{tech.name}</span>
                      <span className="text-xs text-gray-500">{tech.description}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Tools */}
              <div>
                <h3 className="text-xl font-bold text-orange-600 mb-4 flex items-center">
                  <span className="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
                  {t('aboutPage.developmentTools')}
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {techStack.tools.map((tech, index) => (
                    <div key={index} className="bg-gradient-to-br from-orange-50 to-red-50 rounded-xl p-4 text-center hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                      <span className="font-medium text-gray-700 block mb-1">{tech.name}</span>
                      <span className="text-xs text-gray-500">{tech.description}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Call to Action */}
            <div className="text-center">
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-gray-100">
                <h2 className="text-3xl font-bold text-gray-800 mb-4">{t('aboutPage.readyToTransform')}</h2>
                <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
                  {t('aboutPage.joinFarmers')}
                </p>
                <div className="flex flex-wrap justify-center gap-4">
                  <button 
                    onClick={() => navigate('/input')}
                    className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-8 py-3 rounded-xl font-semibold hover:shadow-lg transform hover:scale-105 transition-all duration-300"
                  >
                    {t('aboutPage.startAnalysis')}
                  </button>
                  <button 
                    onClick={() => navigate('/register')}
                    className="bg-white text-indigo-600 border-2 border-indigo-600 px-8 py-3 rounded-xl font-semibold hover:bg-indigo-50 transform hover:scale-105 transition-all duration-300"
                  >
                    {t('aboutPage.createAccount')}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
