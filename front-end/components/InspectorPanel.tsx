import React, { useState } from "react";
import { ethers } from "ethers";

interface InspectorPanelProps {
  contract: ethers.Contract | null;
  account: string;
  onTx: (
    promise: Promise<ethers.ContractTransactionResponse>,
    type: string
  ) => void;
}

const InspectorPanel: React.FC<InspectorPanelProps> = ({
  contract,
  account,
  onTx,
}) => {
  const [orderId, setOrderId] = useState("");
  const [passed, setPassed] = useState(true);
  const [targetInspector, setTargetInspector] = useState<string | null>(null);
  const [orderStatus, setOrderStatus] = useState<string | null>(null);
  const [orderInfo, setOrderInfo] = useState<string>("");

  const STATUS_NAMES = [
    "NONE",
    "PENDING",
    "APPROVED",
    "INSPECTED",
    "RELEASED",
    "CANCELLED",
  ];

  const checkOrder = async () => {
    if (!contract || !orderId) return;
    try {
      const order = await contract.getOrder(orderId);
      const inspector = order[2].toLowerCase();
      const status = Number(order[4]);
      const statusName = STATUS_NAMES[status] || "UNKNOWN";

      setTargetInspector(inspector);
      setOrderStatus(statusName);

      // Build diagnostic info
      const info = `Inspector: ${inspector.substring(
        0,
        10
      )}... | Status: ${statusName} | Your account: ${account
        .toLowerCase()
        .substring(0, 10)}...`;
      setOrderInfo(info);
    } catch (e: any) {
      setTargetInspector(null);
      setOrderStatus(null);
      setOrderInfo(`Error: ${e.message || "Order not found"}`);
    }
  };

  const handleInspect = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contract || !orderId) return;
    const txPromise = contract.inspectProperty(orderId, passed);
    onTx(txPromise, "Inspect Property");
  };

  const isAuthorized =
    targetInspector === null || targetInspector === account.toLowerCase();
  const canInspect = isAuthorized && orderStatus === "APPROVED";

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-emerald-600">
        <i className="fas fa-clipboard-check"></i> Inspector Property Review
      </h3>
      <form onSubmit={handleInspect} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Order ID
          </label>
          <input
            type="number"
            placeholder="Order ID"
            value={orderId}
            onChange={(e) => setOrderId(e.target.value)}
            onBlur={checkOrder}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none"
            required
          />
        </div>

        {orderInfo && (
          <div className="p-3 bg-blue-50 text-blue-700 rounded-lg text-xs border border-blue-200 font-mono">
            {orderInfo}
          </div>
        )}

        {orderStatus && orderStatus !== "APPROVED" && (
          <div className="p-3 bg-yellow-50 text-yellow-700 rounded-lg text-sm border border-yellow-200">
            <i className="fas fa-exclamation-triangle mr-2"></i>
            Order must be in APPROVED status. Current status:{" "}
            <strong>{orderStatus}</strong>
            {orderStatus === "PENDING" && " (Owner needs to confirm first)"}
            {orderStatus === "INSPECTED" && " (Already inspected)"}
          </div>
        )}

        <div className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg">
          <input
            type="checkbox"
            id="passed"
            checked={passed}
            onChange={(e) => setPassed(e.target.checked)}
            className="w-5 h-5 text-emerald-600 rounded focus:ring-emerald-500"
          />
          <label
            htmlFor="passed"
            className="text-sm font-semibold text-gray-700"
          >
            Inspection Passed
          </label>
        </div>

        {targetInspector && !isAuthorized && (
          <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm border border-red-200">
            <i className="fas fa-warning mr-2"></i>
            Warning: You are not the inspector assigned to this order.
          </div>
        )}

        <button
          type="submit"
          disabled={!contract || !canInspect}
          className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-lg transition disabled:opacity-50"
        >
          Submit Inspection
        </button>
      </form>
    </div>
  );
};

export default InspectorPanel;
