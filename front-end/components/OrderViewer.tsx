
import React, { useState } from 'react';
import { ethers } from 'ethers';
import { Order, OrderStatusLabels } from '../types';

interface OrderViewerProps {
  contract: ethers.Contract | null;
  onTx: (promise: Promise<ethers.ContractTransactionResponse>, type: string) => void;
}

const OrderViewer: React.FC<OrderViewerProps> = ({ contract, onTx }) => {
  const [orderId, setOrderId] = useState('');
  const [orderData, setOrderData] = useState<Order | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchOrder = async () => {
    if (!contract || !orderId) return;
    setLoading(true);
    try {
      const result = await contract.getOrder(orderId);
      setOrderData({
        renter: result[0],
        owner: result[1],
        inspector: result[2],
        depositWei: result[3],
        status: Number(result[4]),
        inspectionPassed: result[5],
        createdAt: result[6],
        approvedAt: result[7],
        inspectedAt: result[8],
        closedAt: result[9]
      });
    } catch (err) {
      console.error(err);
      setOrderData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleRelease = async () => {
    if (!contract || !orderId) return;
    const txPromise = contract.releaseDeposit(orderId);
    onTx(txPromise, "Release Deposit");
  };

  const formatDate = (ts: bigint) => {
    if (ts === 0n) return 'N/A';
    return new Date(Number(ts) * 1000).toLocaleString();
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-gray-800">
        <i className="fas fa-search text-gray-500"></i> Track Rental Order
      </h3>
      
      <div className="flex gap-2 mb-6">
        <input 
          type="number" 
          placeholder="Enter Order ID" 
          value={orderId}
          onChange={(e) => setOrderId(e.target.value)}
          className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        />
        <button 
          onClick={fetchOrder}
          className="bg-gray-800 hover:bg-gray-900 text-white font-bold px-6 py-2 rounded-lg transition"
          disabled={loading}
        >
          {loading ? <i className="fas fa-spinner fa-spin"></i> : 'Load'}
        </button>
      </div>

      {orderData && (
        <div className="space-y-4 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="p-3 bg-gray-50 rounded-lg">
              <span className="block text-gray-500 text-xs font-bold uppercase">Renter</span>
              <span className="font-mono text-[10px] break-all md:text-xs">{orderData.renter}</span>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <span className="block text-gray-500 text-xs font-bold uppercase">Owner</span>
              <span className="font-mono text-[10px] break-all md:text-xs">{orderData.owner}</span>
            </div>
            <div className="p-3 bg-gray-50 rounded-lg">
              <span className="block text-gray-500 text-xs font-bold uppercase">Inspector</span>
              <span className="font-mono text-[10px] break-all md:text-xs">{orderData.inspector}</span>
            </div>
            <div className="p-3 bg-blue-50 rounded-lg border border-blue-100">
              <span className="block text-blue-500 text-xs font-bold uppercase">Deposit</span>
              <span className="font-bold text-lg">{ethers.formatEther(orderData.depositWei)} ETH</span>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 py-2">
            <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
              orderData.status === 4 ? 'bg-green-100 text-green-700' : 
              orderData.status === 5 ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
            }`}>
              Status: {OrderStatusLabels[orderData.status]}
            </span>
            <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
              orderData.inspectionPassed ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
            }`}>
              Inspection: {orderData.inspectionPassed ? 'Passed' : 'Not Done/Failed'}
            </span>
          </div>

          <div className="border-t pt-4 grid grid-cols-2 md:grid-cols-4 gap-2 text-[10px]">
            <div><span className="text-gray-400">Created:</span><br/>{formatDate(orderData.createdAt)}</div>
            <div><span className="text-gray-400">Approved:</span><br/>{formatDate(orderData.approvedAt)}</div>
            <div><span className="text-gray-400">Inspected:</span><br/>{formatDate(orderData.inspectedAt)}</div>
            <div><span className="text-gray-400">Closed:</span><br/>{formatDate(orderData.closedAt)}</div>
          </div>

          <div className="mt-4">
            <button 
              onClick={handleRelease}
              disabled={orderData.status !== 3} // Only if inspected
              className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-2 rounded-lg transition disabled:opacity-30"
            >
              Release Deposit
            </button>
            <p className="text-[10px] text-gray-400 text-center mt-1 italic">
              *Can only release if status is INSPECTED
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrderViewer;
