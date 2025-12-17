
import React, { useState } from 'react';
import { ethers } from 'ethers';
import { isValidAddress } from '../lib/eth';

interface RenterPanelProps {
  contract: ethers.Contract | null;
  onTx: (promise: Promise<ethers.ContractTransactionResponse>, type: string) => void;
}

const RenterPanel: React.FC<RenterPanelProps> = ({ contract, onTx }) => {
  const [owner, setOwner] = useState('');
  const [inspector, setInspector] = useState('');
  const [deposit, setDeposit] = useState('0.001');
  const [orderIdToCancel, setOrderIdToCancel] = useState('');

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contract) return;
    if (!isValidAddress(owner) || !isValidAddress(inspector)) {
      alert("Invalid address provided.");
      return;
    }

    try {
      const txPromise = contract.rentProperty(owner, inspector, { 
        value: ethers.parseEther(deposit) 
      });
      onTx(txPromise, "Create Rental Order");
    } catch (err) {
      console.error(err);
    }
  };

  const handleCancel = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contract || !orderIdToCancel) return;
    const txPromise = contract.cancelRental(orderIdToCancel);
    onTx(txPromise, "Cancel Rental");
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <i className="fas fa-plus-circle text-blue-500"></i> Create Rental Order
        </h3>
        <form onSubmit={handleCreateOrder} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Owner Address</label>
            <input 
              type="text" 
              placeholder="0x..." 
              value={owner}
              onChange={(e) => setOwner(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              required
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Inspector Address</label>
            <input 
              type="text" 
              placeholder="0x..." 
              value={inspector}
              onChange={(e) => setInspector(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              required
            />
          </div>
          <div className="md:col-span-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">Deposit (ETH)</label>
            <input 
              type="number" 
              step="0.0001" 
              placeholder="0.01" 
              value={deposit}
              onChange={(e) => setDeposit(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              required
            />
          </div>
          <div className="md:col-span-1 flex items-end">
            <button 
              type="submit"
              disabled={!contract}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-lg transition disabled:opacity-50"
            >
              Rent Property
            </button>
          </div>
        </form>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <i className="fas fa-times-circle text-red-500"></i> Cancel Rental
        </h3>
        <form onSubmit={handleCancel} className="flex gap-4">
          <input 
            type="number" 
            placeholder="Order ID" 
            value={orderIdToCancel}
            onChange={(e) => setOrderIdToCancel(e.target.value)}
            className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-red-500 outline-none"
            required
          />
          <button 
            type="submit"
            disabled={!contract}
            className="bg-red-600 hover:bg-red-700 text-white font-bold px-6 py-2 rounded-lg transition disabled:opacity-50"
          >
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
};

export default RenterPanel;
