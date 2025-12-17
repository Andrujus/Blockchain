
export enum OrderStatus {
  NONE = 0,
  PENDING = 1,
  APPROVED = 2,
  INSPECTED = 3,
  RELEASED = 4,
  CANCELLED = 5
}

export const OrderStatusLabels: Record<OrderStatus, string> = {
  [OrderStatus.NONE]: 'None',
  [OrderStatus.PENDING]: 'Pending',
  [OrderStatus.APPROVED]: 'Approved',
  [OrderStatus.INSPECTED]: 'Inspected',
  [OrderStatus.RELEASED]: 'Released',
  [OrderStatus.CANCELLED]: 'Cancelled'
};

export interface Order {
  renter: string;
  owner: string;
  inspector: string;
  depositWei: bigint;
  status: OrderStatus;
  inspectionPassed: boolean;
  createdAt: bigint;
  approvedAt: bigint;
  inspectedAt: bigint;
  closedAt: bigint;
}

export interface TransactionRecord {
  hash: string;
  type: string;
  status: 'pending' | 'success' | 'error';
  timestamp: number;
}

export type Role = 'renter' | 'owner' | 'inspector' | 'viewer';
