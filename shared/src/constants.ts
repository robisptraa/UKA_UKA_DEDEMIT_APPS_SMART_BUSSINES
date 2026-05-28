/**
 * UKA-UKA: Shared Constants
 * Language: TypeScript
 * Naming Convention: camelCase for variables/exports
 */

// Thrift Streetwear Product Grades
export const thriftGrades = {
  gradeSSS: "SSS (Brand New With Tag / Like New)",
  gradeSS: "SS (Perfect Condition, no flaws)",
  gradeS: "S (Very Good Condition, minor wear)",
  gradeA: "A (Good Condition, slight fading/cracking)",
  gradeB: "B (Fair Condition, small visible flaws/stains)",
  gradeC: "C (Worn Out / Vintage faded heavily)"
} as const;

export type ThriftGrade = keyof typeof thriftGrades;

// Popular Streetwear / Thrift Categories in Indonesia
export const productCategories = [
  "tshirt",      // Kaos Vintage/Streetwear
  "hoodie",      // Hoodie/Pullover
  "crewneck",    // Sweater Crewneck
  "jacket",      // Jaket Bomber/Varsity/Windbreaker
  "pants",       // Celana Cargo/Jeans/Chino
  "sneakers",    // Sepatu Streetwear
  "accessories"  // Topi, Tas, Aksesoris lainnya
] as const;

export type ProductCategory = typeof productCategories[number];

// Transaction & Order Statuses
export const orderStatuses = {
  pending: "Pending Payment",
  paid: "Paid & Processing",
  packed: "Packed & Ready to Ship",
  shipped: "Shipped out with Courier",
  completed: "Completed / Finished",
  cancelled: "Cancelled / Expired"
} as const;

export type OrderStatus = keyof typeof orderStatuses;

// Midtrans Indonesia Payment Methods supported
export const paymentMethods = {
  qris: "QRIS (Gopay, OVO, Dana, LinkAja, ShopeePay)",
  gopay: "GoPay Direct",
  shopeepay: "ShopeePay Direct",
  bankTransferBca: "BCA Virtual Account",
  bankTransferMandiri: "Mandiri Bill Payment",
  bankTransferBni: "BNI Virtual Account",
  bankTransferBri: "BRI Virtual Account"
} as const;

export type PaymentMethod = keyof typeof paymentMethods;

// AI Processing Configurations
export const aiConfig = {
  defaultModel: "gemini-1.5-flash",
  fallbackModel: "claude-3-5-sonnet",
  maxTokens: 1024,
  temperature: 0.2
} as const;

// Currency Code
export const currencyCode = "IDR";
