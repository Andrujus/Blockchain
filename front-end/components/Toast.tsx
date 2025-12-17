
import React from 'react';
import { getExplorerLink } from '../lib/eth';

interface ToastProps {
  message: string;
  type: 'info' | 'success' | 'error';
  txHash?: string;
  onClose: () => void;
}

const Toast: React.FC<ToastProps> = ({ message, type, txHash, onClose }) => {
  const bgColors = {
    info: 'bg-blue-600',
    success: 'bg-green-600',
    error: 'bg-red-600'
  };

  return (
    <div className={`fixed bottom-4 right-4 z-50 ${bgColors[type]} text-white px-6 py-4 rounded-lg shadow-xl flex flex-col min-w-[300px] transition-all duration-300 animate-slide-in`}>
      <div className="flex justify-between items-center mb-1">
        <span className="font-bold flex items-center gap-2">
          {type === 'info' && <i className="fas fa-spinner fa-spin"></i>}
          {type === 'success' && <i className="fas fa-check-circle"></i>}
          {type === 'error' && <i className="fas fa-exclamation-triangle"></i>}
          {type.toUpperCase()}
        </span>
        <button onClick={onClose} className="hover:text-gray-200">
          <i className="fas fa-times"></i>
        </button>
      </div>
      <p className="text-sm opacity-90">{message}</p>
      {txHash && (
        <a 
          href={getExplorerLink(txHash)} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="mt-2 text-xs underline hover:no-underline font-mono"
        >
          View on Etherscan: {txHash.substring(0, 10)}...
        </a>
      )}
    </div>
  );
};

export default Toast;
