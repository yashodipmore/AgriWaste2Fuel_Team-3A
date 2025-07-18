import React from 'react';

const ResultCard = ({ title, value, icon }) => {
  return (
    <div className="bg-white shadow-lg rounded-lg p-6 hover:shadow-xl transition-shadow duration-300">
      <div className="flex items-center mb-2">
        {icon && <span className="text-2xl mr-2">{icon}</span>}
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      </div>
      <p className="text-2xl font-bold text-green-600">{value}</p>
    </div>
  );
};

export default ResultCard;
