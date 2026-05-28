import { ThriftGrade, ProductCategory, OrderStatus, PaymentMethod } from "./constants";

/**
 * UKA-UKA: Shared TypeScript Interfaces
 * Language: TypeScript
 * Naming Convention: camelCase for properties, PascalCase for Interfaces
 */

// User / Owner Entity
export interface User {
  id: string;
  email: string;
  businessName: string;
  ownerName: string;
  phoneNumber: string;
  createdAt: string;
}

// Thrift Product / Item Entity
export interface Product {
  id: string;
  title: string;
  description: string;
  brand: string;
  grade: ThriftGrade;
  category: ProductCategory;
  originalPriceEstimated?: number; // Estimated original market price
  sellingPrice: number;            // Selling price in IDR
  capitalPrice: number;            // Capital price / Harga modal
  imageUrl?: string;
  status: "available" | "sold" | "reserved";
  createdAt: string;
  updatedAt: string;
}

// Customer details for checkout
export interface Customer {
  name: string;
  phoneNumber: string;
  telegramUsername?: string;
  address?: string;
}

// Transaction Order Entity
export interface Order {
  id: string;
  orderNumber: string;
  products: {
    productId: string;
    price: number;
  }[];
  totalAmount: number;
  status: OrderStatus;
  customer: Customer;
  paymentMethod?: PaymentMethod;
  midtransTransactionId?: string;
  createdAt: string;
  updatedAt: string;
}

// Midtrans Payment Response Structure
export interface PaymentResponse {
  snapToken: string;
  redirectUrl: string;
  transactionId: string;
  orderId: string;
}

// AI Price & Description Analysis Output
export interface AiAnalysisResult {
  estimatedBrand: string;
  estimatedGrade: ThriftGrade;
  estimatedMarketPrice: number;
  recommendedSellingPrice: number;
  recommendedDescription: string;
  suggestedTags: string[];
  confidenceScore: number;
}
