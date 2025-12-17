import React, { useState, useEffect, useCallback } from "react";
import { ethers } from "ethers";
import { RentalEscrowABI } from "./abi/RentalEscrow";
import { RentalEscrowBytecode } from "./abi/RentalEscrowBytecode";
// Fix: Added getExplorerLink to imports
import {
  SEPOLIA_CHAIN_ID,
  switchNetwork,
  isValidAddress,
  getExplorerLink,
} from "./lib/eth";
import { Role, TransactionRecord } from "./types";
import Toast from "./components/Toast";
import RenterPanel from "./components/RenterPanel";
import OwnerPanel from "./components/OwnerPanel";
import InspectorPanel from "./components/InspectorPanel";
import OrderViewer from "./components/OrderViewer";

const App: React.FC = () => {
  const [account, setAccount] = useState<string>("");
  const [chainId, setChainId] = useState<string>("");
  const [balance, setBalance] = useState<string>("0");
  const [contractAddress, setContractAddress] = useState<string>("");
  const [contract, setContract] = useState<ethers.Contract | null>(null);
  const [activeRole, setActiveRole] = useState<Role>("renter");
  const [transactions, setTransactions] = useState<TransactionRecord[]>([]);
  const [toast, setToast] = useState<{
    message: string;
    type: "info" | "success" | "error";
    txHash?: string;
  } | null>(null);

  const updateWalletInfo = useCallback(
    async (provider: ethers.BrowserProvider) => {
      try {
        const signer = await provider.getSigner();
        const address = await signer.getAddress();
        const network = await provider.getNetwork();
        const bal = await provider.getBalance(address);

        const chainIdHex = "0x" + network.chainId.toString(16);
        console.log("Network info:", {
          chainId: network.chainId,
          chainIdHex,
          expected: SEPOLIA_CHAIN_ID,
          matches: chainIdHex === SEPOLIA_CHAIN_ID,
        });

        setAccount(address);
        setChainId(chainIdHex);
        setBalance(ethers.formatEther(bal));
      } catch (err) {
        console.error("Wallet update error", err);
      }
    },
    []
  );

  const connectWallet = async () => {
    // Fix: window.ethereum is now globally declared in lib/eth.ts
    if (!window.ethereum) {
      alert("Please install MetaMask!");
      return;
    }
    try {
      await window.ethereum.request({ method: "eth_requestAccounts" });
      const provider = new ethers.BrowserProvider(window.ethereum);
      updateWalletInfo(provider);
    } catch (err) {
      console.error(err);
    }
  };

  const switchAccount = async () => {
    if (!window.ethereum) {
      alert("Please install MetaMask!");
      return;
    }
    try {
      await window.ethereum.request({
        method: "wallet_requestPermissions",
        params: [{ eth_accounts: {} }],
      });
      const provider = new ethers.BrowserProvider(window.ethereum);
      updateWalletInfo(provider);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    // Fix: window.ethereum is now globally declared in lib/eth.ts
    if (window.ethereum) {
      const provider = new ethers.BrowserProvider(window.ethereum);
      window.ethereum.on("accountsChanged", () => updateWalletInfo(provider));
      window.ethereum.on("chainChanged", () => updateWalletInfo(provider));

      // Auto-connect if already authorized
      provider.listAccounts().then((accounts) => {
        if (accounts.length > 0) updateWalletInfo(provider);
      });
    }
  }, [updateWalletInfo]);

  const loadContract = () => {
    if (!isValidAddress(contractAddress)) {
      alert("Invalid contract address");
      return;
    }
    // Fix: window.ethereum is now globally declared in lib/eth.ts
    if (!window.ethereum) return;

    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      provider.getSigner().then(async (signer) => {
        const code = await provider.getCode(contractAddress);
        if (!code || code === "0x") {
          setToast({
            message: "Address is not a deployed contract",
            type: "error",
          });
          return;
        }

        const instance = new ethers.Contract(
          contractAddress,
          RentalEscrowABI,
          signer
        );
        setContract(instance);
        setToast({ message: "Contract loaded successfully", type: "success" });
      });
    } catch (err) {
      console.error(err);
      setToast({ message: "Failed to load contract", type: "error" });
    }
  };

  const deployContract = async () => {
    if (!window.ethereum) {
      alert("Please install MetaMask!");
      return;
    }
    if (!account || !isSepolia) {
      alert("Please connect to Sepolia network first");
      return;
    }

    try {
      setToast({ message: "Deploying contract...", type: "info" });
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();

      const factory = new ethers.ContractFactory(
        RentalEscrowABI,
        RentalEscrowBytecode,
        signer
      );

      const contract = await factory.deploy();
      await contract.waitForDeployment();

      const address = await contract.getAddress();
      setContractAddress(address);
      setContract(contract);

      setToast({
        message: `Contract deployed at ${address}`,
        type: "success",
      });
    } catch (err: any) {
      console.error(err);
      const errorMsg = err.reason || err.message || "Deployment failed";
      setToast({ message: `Error: ${errorMsg}`, type: "error" });
    }
  };

  const handleTransaction = async (
    txPromise: Promise<ethers.ContractTransactionResponse>,
    type: string
  ) => {
    try {
      setToast({ message: `Initiating ${type}...`, type: "info" });
      const tx = await txPromise;

      const newTx: TransactionRecord = {
        hash: tx.hash,
        type,
        status: "pending",
        timestamp: Date.now(),
      };
      setTransactions((prev) => [newTx, ...prev].slice(0, 5));
      setToast({
        message: `Transaction pending: ${type}`,
        type: "info",
        txHash: tx.hash,
      });

      const receipt = await tx.wait();

      if (receipt?.status === 1) {
        setTransactions((prev) =>
          prev.map((t) =>
            t.hash === tx.hash ? { ...t, status: "success" } : t
          )
        );

        // Specific logic for rentProperty to find OrderID
        let extraInfo = "";
        if (type === "Create Rental Order") {
          const iface = new ethers.Interface(RentalEscrowABI);
          receipt.logs.forEach((log) => {
            try {
              const parsed = iface.parseLog(log);
              if (parsed?.name === "OrderCreated") {
                extraInfo = ` - Order ID: ${parsed.args[0]}`;
              }
            } catch (e) {}
          });
        }

        setToast({
          message: `${type} successful!${extraInfo}`,
          type: "success",
          txHash: tx.hash,
        });
      } else {
        throw new Error("Transaction reverted");
      }
    } catch (err: any) {
      console.error(err);
      const errorMsg =
        err.reason || err.message || "User rejected or contract error";
      setToast({ message: `Error: ${errorMsg}`, type: "error" });
    }
  };

  const isSepolia = chainId === SEPOLIA_CHAIN_ID;

  return (
    <div className="min-h-screen pb-12">
      {/* Header / Top Bar */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40 backdrop-blur-md bg-white/80">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
              R
            </div>
            <h1 className="font-bold text-xl hidden sm:block">RentalEscrow</h1>
          </div>

          <div className="flex items-center gap-4">
            {account ? (
              <>
                <div className="hidden md:flex flex-col items-end text-right">
                  <span className="text-xs font-bold text-gray-400">
                    Account
                  </span>
                  <span className="text-sm font-mono">
                    {account.substring(0, 6)}...{account.substring(38)}
                  </span>
                </div>
                <button
                  onClick={switchAccount}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-4 py-2 rounded-full font-bold transition text-sm"
                  title="Switch MetaMask Account"
                >
                  Switch Account
                </button>
              </>
            ) : (
              <button
                onClick={connectWallet}
                className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-full font-bold transition text-sm"
              >
                Connect Wallet
              </button>
            )}

            {account && (
              <div className="px-3 py-1 bg-gray-100 rounded-full flex items-center gap-2 border border-gray-200">
                <div
                  className={`w-2 h-2 rounded-full ${
                    isSepolia ? "bg-green-500" : "bg-red-500"
                  }`}
                ></div>
                <span className="text-xs font-bold">
                  {isSepolia ? "Sepolia" : "Wrong Network"}
                </span>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Network Warning */}
      {account && !isSepolia && (
        <div className="bg-red-600 text-white py-3 px-4 flex justify-between items-center animate-pulse">
          <span className="text-sm font-bold">
            Please switch your network to Sepolia to interact with the contract.
          </span>
          <button
            onClick={switchNetwork}
            className="bg-white text-red-600 px-4 py-1 rounded-full text-xs font-bold"
          >
            Switch to Sepolia
          </button>
        </div>
      )}

      <main className="max-w-6xl mx-auto px-4 mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Connection & Setup */}
        <div className="lg:col-span-1 space-y-6">
          <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
              <i className="fas fa-wallet text-gray-400"></i> Wallet Status
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between border-b pb-2 text-sm">
                <span className="text-gray-500">Balance</span>
                <span className="font-bold">
                  {parseFloat(balance).toFixed(4)} ETH
                </span>
              </div>
              <div className="flex justify-between border-b pb-2 text-sm">
                <span className="text-gray-500">Chain ID</span>
                <span className="font-mono">
                  {parseInt(chainId, 16) || "None"}
                </span>
              </div>
            </div>
          </section>

          <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
              <i className="fas fa-file-contract text-gray-400"></i> Contract
              Setup
            </h2>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Contract Address (0x...)"
                value={contractAddress}
                onChange={(e) => setContractAddress(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm font-mono"
              />
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={loadContract}
                  disabled={!account || !isSepolia}
                  className="bg-gray-900 hover:bg-black text-white font-bold py-2 rounded-lg transition disabled:opacity-30 text-sm"
                >
                  Load Contract
                </button>
                <button
                  onClick={deployContract}
                  disabled={!account || !isSepolia}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-lg transition disabled:opacity-30 text-sm"
                >
                  Deploy New
                </button>
              </div>
            </div>
          </section>

          <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
              <i className="fas fa-history text-gray-400"></i> Recent Activity
            </h2>
            <div className="space-y-3">
              {transactions.length === 0 ? (
                <p className="text-gray-400 text-xs text-center py-4">
                  No recent transactions
                </p>
              ) : (
                transactions.map((tx) => (
                  <div
                    key={tx.hash}
                    className="text-xs p-3 border rounded-lg hover:bg-gray-50 transition"
                  >
                    <div className="flex justify-between mb-1">
                      <span className="font-bold">{tx.type}</span>
                      <span
                        className={`capitalize font-bold ${
                          tx.status === "success"
                            ? "text-green-500"
                            : tx.status === "pending"
                            ? "text-blue-500"
                            : "text-red-500"
                        }`}
                      >
                        {tx.status}
                      </span>
                    </div>
                    {/* Fix: getExplorerLink is now imported */}
                    <a
                      href={getExplorerLink(tx.hash)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-400 font-mono block truncate hover:underline"
                    >
                      {tx.hash}
                    </a>
                  </div>
                ))
              )}
            </div>
          </section>
        </div>

        {/* Right Column: Interaction Panels */}
        <div className="lg:col-span-2 space-y-6">
          {/* Role Navigation */}
          <div className="flex p-1 bg-gray-200 rounded-xl">
            {(["renter", "owner", "inspector", "viewer"] as Role[]).map(
              (role) => (
                <button
                  key={role}
                  onClick={() => setActiveRole(role)}
                  className={`flex-1 py-2 text-sm font-bold rounded-lg transition-all capitalize ${
                    activeRole === role
                      ? "bg-white shadow-md text-blue-600"
                      : "text-gray-500 hover:text-gray-700"
                  }`}
                >
                  {role}
                </button>
              )
            )}
          </div>

          {!contract && activeRole !== "viewer" ? (
            <div className="bg-blue-50 border border-blue-100 p-8 rounded-2xl text-center">
              <i className="fas fa-info-circle text-blue-400 text-4xl mb-4"></i>
              <h3 className="text-lg font-bold text-blue-800">
                Contract Not Loaded
              </h3>
              <p className="text-blue-600 text-sm mt-2">
                Please provide a contract address and click "Load Contract" to
                start interacting.
              </p>
            </div>
          ) : (
            <div className="transition-all duration-300">
              {activeRole === "renter" && (
                <RenterPanel contract={contract} onTx={handleTransaction} />
              )}
              {activeRole === "owner" && (
                <OwnerPanel
                  contract={contract}
                  account={account}
                  onTx={handleTransaction}
                />
              )}
              {activeRole === "inspector" && (
                <InspectorPanel
                  contract={contract}
                  account={account}
                  onTx={handleTransaction}
                />
              )}
              {(activeRole === "viewer" ||
                activeRole === "renter" ||
                activeRole === "owner" ||
                activeRole === "inspector") && (
                <div className={activeRole === "viewer" ? "" : "mt-8"}>
                  <OrderViewer contract={contract} onTx={handleTransaction} />
                </div>
              )}
            </div>
          )}
        </div>
      </main>

      {/* Toast Notification */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          txHash={toast.txHash}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default App;
