
import React, { useState } from 'react';
import { ethers } from 'ethers';

interface OwnerPanelProps {
  contract: ethers.Contract | null;
  account: string;
  onTx: (promise: Promise<ethers.ContractTransactionResponse>, type: string) => void;
}

const OwnerPanel: React.FC<OwnerPanelProps> = ({ contract, account, onTx }) => {
  const [orderId, setOrderId] = useState('');
  const [targetOwner, setTargetOwner] = useState<string | null>(null);

  const checkOrder = async () => {
    if (!contract || !orderId) return;
    try {
      const order = await contract.getOrder(orderId);
      setTargetOwner(order[1].toLowerCase());
    } catch (e) {
      setTargetOwner(null);
    }
  };

  const handleConfirm = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contract || !orderId) return;
    const txPromise = contract.confirmRental(orderId);
    onTx(txPromise, "Confirm Rental");
  };

  const isAuthorized = targetOwner === null || targetOwner === account.toLowerCase();

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-indigo-600">
        <i className="fas fa-handshake"></i> Owner Approval
      </h3>
      <form onSubmit={handleConfirm} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Order ID to Approve</label>
          <div className="flex gap-2">
            <input 
              type="number" 
              placeholder="Order ID" 
              value={orderId}
              onChange={(e) => setOrderId(e.target.value)}
              onBlur={checkOrder}
              className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
              required
            />
          </div>
        </div>

        {targetOwner && !isAuthorized && (
          <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm border border-red-200">
            <i className="fas fa-warning mr-2"></i>
            Warning: You are not the owner assigned to this order.
          </div>
        )}

        <button 
          type="submit"
          disabled={!contract || !isAuthorized}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-lg transition disabled:opacity-50"
        >
          Confirm Rental
        </button>
      </form>
    </div>
  );
};

export default OwnerPanel;
