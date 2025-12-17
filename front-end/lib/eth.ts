
import { ethers } from 'ethers';

// Add declaration for window.ethereum to resolve TypeScript errors
declare global {
  interface Window {
    ethereum?: any;
  }
}

export const SEPOLIA_CHAIN_ID = '0xaa36a7'; // 11155111

export const switchNetwork = async () => {
  if (!window.ethereum) return;
  try {
    await window.ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: SEPOLIA_CHAIN_ID }],
    });
  } catch (switchError: any) {
    // This error code indicates that the chain has not been added to MetaMask.
    if (switchError.code === 4902) {
      try {
        await window.ethereum.request({
          method: 'wallet_addEthereumChain',
          params: [
            {
              chainId: SEPOLIA_CHAIN_ID,
              chainName: 'Sepolia Test Network',
              nativeCurrency: { name: 'Sepolia Ether', symbol: 'ETH', decimals: 18 },
              rpcUrls: ['https://rpc.sepolia.org'],
              blockExplorerUrls: ['https://sepolia.etherscan.io'],
            },
          ],
        });
      } catch (addError) {
        console.error("Failed to add Sepolia network", addError);
      }
    }
  }
};

export const getExplorerLink = (hash: string) => `https://sepolia.etherscan.io/tx/${hash}`;

export const isValidAddress = (addr: string) => ethers.isAddress(addr);
