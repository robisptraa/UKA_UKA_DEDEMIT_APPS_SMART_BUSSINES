"use client";

import React, { useState, useRef } from "react";
import { 
  Package, 
  Search, 
  Plus, 
  ArrowUpDown, 
  Upload, 
  Trash2, 
  Check, 
  X, 
  Layers, 
  SlidersHorizontal,
  ChevronDown
} from "lucide-react";
import { toast } from "react-hot-toast";

interface Product {
  id: string;
  name: string;
  brand: string;
  category: string;
  price: number;
  stock: number;
  isActive: boolean;
}

export default function ProductsPage() {
  // Mock data produk universal UMKM
  const [products, setProducts] = useState<Product[]>([
    { id: "PROD-1", name: "Paket Nasi Rendang Komplit", brand: "Warung Makan", category: "Kuliner", price: 35000, stock: 20, isActive: true },
    { id: "PROD-2", name: "Baju Batik Solo Motif Parang", brand: "Toko Fashion", category: "Fashion", price: 185000, stock: 3, isActive: true },
    { id: "PROD-3", name: "Keratin Treatment Rambut", brand: "Salon Kecantikan", category: "Kecantikan", price: 350000, stock: 10, isActive: true },
    { id: "PROD-4", name: "Cuci Kering 3kg + Parfum", brand: "Laundry", category: "Jasa Laundry", price: 45000, stock: 50, isActive: true },
    { id: "PROD-5", name: "Beras Premium Pandan Wangi 5kg", brand: "Toko Kelontong", category: "Sembako", price: 75000, stock: 2, isActive: true },
    { id: "PROD-6", name: "Servis Sepeda Motor + Ganti Oli", brand: "Bengkel", category: "Jasa Otomotif", price: 125000, stock: 15, isActive: true },
    { id: "PROD-7", name: "Foto Studio 1 Jam Sesi Privat", brand: "Foto Studio", category: "Jasa Foto", price: 200000, stock: 5, isActive: false },
    { id: "PROD-8", name: "Kue Tart Ulang Tahun Custom", brand: "Bakery", category: "Bakery & Kue", price: 280000, stock: 8, isActive: true },
  ]);

  const [searchQuery, setSearchQuery] = useState("");
  const [filterCategory, setFilterCategory] = useState("all");
  const [sortField, setSortField] = useState<"name" | "price" | "stock">("name");
  const [sortAsc, setSortAsc] = useState(true);

  // Bulk Action State
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newProductName, setNewProductName] = useState("");
  const [newProductBrand, setNewProductBrand] = useState("Warung Makan");
  const [newProductCategory, setNewProductCategory] = useState("Kuliner");
  const [newProductPrice, setNewProductPrice] = useState("");
  const [newProductStock, setNewProductStock] = useState("1");
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle Search & Filter & Sort
  const filteredProducts = products
    .filter(p => {
      const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            p.brand.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCategory = filterCategory === "all" || p.category.toLowerCase() === filterCategory.toLowerCase();
      return matchesSearch && matchesCategory;
    })
    .sort((a, b) => {
      let valA = a[sortField];
      let valB = b[sortField];
      
      if (typeof valA === "string") {
        return sortAsc 
          ? (valA as string).localeCompare(valB as string) 
          : (valB as string).localeCompare(valA as string);
      } else {
        return sortAsc 
          ? (valA as number) - (valB as number) 
          : (valB as number) - (valA as number);
      }
    });

  // Toggle Sort
  const handleSort = (field: "name" | "price" | "stock") => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(true);
    }
  };

  // Checkbox Handler
  const toggleSelect = (id: string) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === filteredProducts.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(filteredProducts.map(p => p.id));
    }
  };

  // Bulk Actions
  const handleBulkToggleActive = (activeState: boolean) => {
    if (selectedIds.length === 0) return;
    setProducts(prev => 
      prev.map(p => selectedIds.includes(p.id) ? { ...p, isActive: activeState } : p)
    );
    setSelectedIds([]);
    toast.success(`Sukses memperbarui status ${selectedIds.length} produk! ⚡`, {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  const handleBulkDelete = () => {
    if (selectedIds.length === 0) return;
    setProducts(prev => prev.filter(p => !selectedIds.includes(p.id)));
    setSelectedIds([]);
    toast.error(`Berhasil menghapus ${selectedIds.length} produk! 🗑️`, {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  // CSV Importer Simulation
  const handleCSVImportClick = () => {
    fileInputRef.current?.click();
  };

  const handleCSVFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      toast.loading("Membaca berkas CSV...", { id: "csv" });
      
      setTimeout(() => {
        const importedProducts: Product[] = [
          { id: `PROD-${Date.now()}-1`, name: "Es Teh Manis Jumbo", brand: "Warung Makan", category: "Kuliner", price: 8000, stock: 100, isActive: true },
          { id: `PROD-${Date.now()}-2`, name: "Jilbab Segi Empat Motif Floral", brand: "Toko Fashion", category: "Fashion", price: 55000, stock: 20, isActive: true },
        ];
        setProducts(prev => [...prev, ...importedProducts]);
        toast.dismiss("csv");
        toast.success("Sukses mengimpor 2 produk UMKM baru dari CSV! 📦", {
          style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
        });
      }, 1500);
    }
  };

  // Simpan produk baru dari modal
  const handleSaveProduct = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProductName || !newProductPrice) {
      toast.error("Mohon isi seluruh data wajib!");
      return;
    }

    const priceNum = parseFloat(newProductPrice) || 0;
    const stockNum = parseInt(newProductStock) || 1;

    const newProd: Product = {
      id: `PROD-${products.length + 1}`,
      name: newProductName,
      brand: newProductBrand,
      category: newProductCategory,
      price: priceNum,
      stock: stockNum,
      isActive: true
    };

    setProducts([newProd, ...products]);
    setIsModalOpen(false);
    
    // Reset Form
    setNewProductName("");
    setNewProductPrice("");
    setNewProductStock("1");
    setImagePreview(null);

    toast.success("Produk baru berhasil disimpan ke katalog! 🎉", {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  return (
    <div className="space-y-8 font-mono text-xs">
      
      {/* HEADER CATALOG */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2 font-sans">
            Katalog Produk & Jasa UMKM <span className="animate-pulse">📦</span>
          </h2>
          <p className="text-[10px] text-zinc-500">Kelola inventori produk & jasa dari semua kategori bisnis — warung, fashion, salon, laundry, bengkel, dan lainnya.</p>
        </div>

        {/* Action CTAs */}
        <div className="flex items-center gap-3">
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleCSVFileChange}
            accept=".csv" 
            className="hidden" 
          />
          <button 
            onClick={handleCSVImportClick}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-900 text-zinc-300 hover:text-white transition-all font-bold"
          >
            <Upload className="w-3.5 h-3.5" /> Import CSV
          </button>
          
          <button 
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-brand hover:bg-brand-dark text-white shadow-lg hover:shadow-brand/20 transition-all font-bold"
          >
            <Plus className="w-3.5 h-3.5" /> + Tambah Produk
          </button>
        </div>
      </header>

      {/* ================= CONTROLS & FILTER SECTION ================= */}
      <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
        
        {/* Search Bar */}
        <div className="md:col-span-2 relative">
          <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-500">
            <Search className="w-4 h-4" />
          </span>
          <input 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Cari nama produk, jasa, atau jenis usaha..."
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-3 pl-10 pr-4 text-zinc-200 focus:outline-none focus:border-brand-light transition-all"
          />
        </div>

        {/* Filter Kategori UMKM Dropdown */}
        <div className="relative">
          <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-500">
            <SlidersHorizontal className="w-4 h-4" />
          </span>
          <select 
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-3 pl-10 pr-10 text-zinc-300 focus:outline-none focus:border-brand-light transition-all appearance-none"
          >
            <option value="all">Semua Kategori</option>
            <option value="kuliner">🍜 Kuliner</option>
            <option value="fashion">👗 Fashion</option>
            <option value="kecantikan">💄 Kecantikan</option>
            <option value="jasa laundry">🧺 Jasa Laundry</option>
            <option value="sembako">🛒 Sembako</option>
            <option value="jasa otomotif">🔧 Jasa Otomotif</option>
            <option value="bakery & kue">🎂 Bakery & Kue</option>
            <option value="jasa foto">📸 Jasa Foto</option>
          </select>
          <span className="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none text-zinc-500">
            <ChevronDown className="w-4 h-4" />
          </span>
        </div>
      </section>

      {/* ================= BULK ACTIONS CONTEXT PANEL ================= */}
      {selectedIds.length > 0 && (
        <div className="p-4 bg-brand/5 border border-brand/20 rounded-2xl flex items-center justify-between animate-fade-in">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-brand animate-pulse" />
            <span className="text-zinc-300 font-bold uppercase">{selectedIds.length} Item Terpilih:</span>
          </div>

          <div className="flex items-center gap-2">
            <button 
              onClick={() => handleBulkToggleActive(true)}
              className="px-3 py-1.5 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-thrift-emerald rounded-lg hover:text-white transition-colors"
            >
              Aktifkan
            </button>
            <button 
              onClick={() => handleBulkToggleActive(false)}
              className="px-3 py-1.5 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-yellow-500 rounded-lg hover:text-white transition-colors"
            >
              Nonaktifkan
            </button>
            <button 
              onClick={handleBulkDelete}
              className="p-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg transition-colors"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* ================= PRODUCTS DATATABLE ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-zinc-800 text-zinc-500 uppercase tracking-wider">
                <th className="py-4 pl-2 pr-4">
                  <input 
                    type="checkbox" 
                    checked={selectedIds.length === filteredProducts.length && filteredProducts.length > 0}
                    onChange={toggleSelectAll}
                    className="accent-brand rounded"
                  />
                </th>
                <th className="py-4">ID</th>
                <th className="py-4 hover:text-white cursor-pointer" onClick={() => handleSort("name")}>
                  PRODUK <ArrowUpDown className="w-3 h-3 inline ml-1" />
                </th>
                <th className="py-4">JENIS USAHA</th>
                <th className="py-4">KATEGORI</th>
                <th className="py-4 text-right hover:text-white cursor-pointer" onClick={() => handleSort("price")}>
                  HARGA <ArrowUpDown className="w-3 h-3 inline ml-1" />
                </th>
                <th className="py-4 text-right hover:text-white cursor-pointer" onClick={() => handleSort("stock")}>
                  STOK <ArrowUpDown className="w-3 h-3 inline ml-1" />
                </th>
                <th className="py-4 pl-6">STATUS</th>
              </tr>
            </thead>
            <tbody>
              {filteredProducts.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-zinc-500">Tidak ada produk/jasa ditemukan. Coba ubah kata kunci pencarian.</td>
                </tr>
              ) : (
                filteredProducts.map((p) => (
                  <tr key={p.id} className="border-b border-zinc-800/50 hover:bg-zinc-950/40 transition-colors">
                    <td className="py-4 pl-2 pr-4">
                      <input 
                        type="checkbox" 
                        checked={selectedIds.includes(p.id)}
                        onChange={() => toggleSelect(p.id)}
                        className="accent-brand rounded"
                      />
                    </td>
                    <td className="py-4 text-zinc-500 font-bold">{p.id}</td>
                    <td className="py-4 text-white font-bold max-w-[200px] truncate">{p.name}</td>
                    <td className="py-4 text-zinc-300">{p.brand}</td>
                    <td className="py-4 text-zinc-400">{p.category}</td>
                    <td className="py-4 text-right text-brand-ghost font-bold">Rp {p.price.toLocaleString("id-ID")}</td>
                    <td className="py-4 text-right font-bold text-zinc-300 pr-2">{p.stock}</td>
                    <td className="py-4 pl-6">
                      <span className={`px-2.5 py-0.5 rounded text-[9px] font-extrabold uppercase ${
                        p.isActive 
                          ? "bg-brand/10 text-brand border border-brand/20" 
                          : "bg-zinc-800 text-zinc-400"
                      }`}>
                        {p.isActive ? "✓ Aktif" : "✕ Nonaktif"}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* ================= MODAL ADD PRODUCT OVERLAY ================= */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="fixed inset-0 bg-black/75 backdrop-blur-sm" onClick={() => setIsModalOpen(false)} />
          
          <div className="w-full max-w-lg bg-zinc-900 border border-zinc-800 rounded-3xl p-6 relative z-50 text-xs font-mono">
            <div className="flex justify-between items-center pb-4 border-b border-zinc-800 mb-6">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                <Package className="w-4 h-4 text-brand-ghost" /> + Tambah Produk Baru
              </h3>
              <button 
                onClick={() => setIsModalOpen(false)}
                className="p-1 rounded-lg text-zinc-500 hover:text-white hover:bg-zinc-800"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveProduct} className="space-y-4">
              <div>
                <label className="text-zinc-500 block mb-1">NAMA PRODUK / JASA *</label>
                <input 
                  type="text" 
                  required
                  placeholder="Contoh: Paket Nasi Ayam Bakar, Cuci Motor, Potong Rambut..."
                  value={newProductName}
                  onChange={(e) => setNewProductName(e.target.value)}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-200 focus:outline-none focus:border-brand-light"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                 <div>
                   <label className="text-zinc-500 block mb-1">JENIS USAHA</label>
                   <select 
                     value={newProductBrand}
                     onChange={(e) => setNewProductBrand(e.target.value)}
                     className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
                   >
                     <option value="Warung Makan">🍜 Warung Makan</option>
                     <option value="Toko Fashion">👗 Toko Fashion</option>
                     <option value="Salon Kecantikan">💄 Salon Kecantikan</option>
                     <option value="Laundry">🧺 Laundry</option>
                     <option value="Toko Kelontong">🛒 Toko Kelontong</option>
                     <option value="Bengkel">🔧 Bengkel</option>
                     <option value="Bakery">🎂 Bakery & Kue</option>
                     <option value="Foto Studio">📸 Foto Studio</option>
                   </select>
                 </div>
                 <div>
                   <label className="text-zinc-500 block mb-1">KATEGORI</label>
                   <select 
                     value={newProductCategory}
                     onChange={(e) => setNewProductCategory(e.target.value)}
                     className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
                   >
                     <option value="Kuliner">Kuliner</option>
                     <option value="Fashion">Fashion</option>
                     <option value="Kecantikan">Kecantikan</option>
                     <option value="Jasa Laundry">Jasa Laundry</option>
                     <option value="Sembako">Sembako</option>
                     <option value="Jasa Otomotif">Jasa Otomotif</option>
                     <option value="Bakery & Kue">Bakery & Kue</option>
                     <option value="Jasa Foto">Jasa Foto</option>
                   </select>
                 </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-zinc-500 block mb-1">HARGA JUAL (RP) *</label>
                  <input 
                    type="number" 
                    required
                    placeholder="250000"
                    value={newProductPrice}
                    onChange={(e) => setNewProductPrice(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-200 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-zinc-500 block mb-1">STOK UTAMA</label>
                  <input 
                    type="number" 
                    value={newProductStock}
                    onChange={(e) => setNewProductStock(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-200 focus:outline-none"
                  />
                </div>
              </div>

              {/* Simulation Photo Upload */}
              <div>
                <label className="text-zinc-500 block mb-1">FOTO PRODUK</label>
                <div 
                  onClick={() => {
                    setImagePreview("https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400&q=80");
                    toast.success("Foto simulasi terunggah!");
                  }}
                  className="w-full border border-dashed border-zinc-800 hover:border-brand/40 rounded-xl h-24 flex flex-col justify-center items-center cursor-pointer text-zinc-500 hover:text-brand-ghost transition-all bg-zinc-950/40 relative overflow-hidden"
                >
                  {imagePreview ? (
                    <div className="absolute inset-0 bg-cover bg-center filter brightness-75" style={{backgroundImage: `url('${imagePreview}')`}} />
                  ) : (
                    <>
                      <Upload className="w-5 h-5 mb-1.5" />
                      <span>Klik untuk simulasi upload foto produk</span>
                    </>
                  )}
                </div>
              </div>

              <div className="pt-4 flex gap-3">
                <button 
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="w-1/2 border border-zinc-800 text-zinc-400 py-3 rounded-xl hover:bg-zinc-850 hover:text-white transition-colors"
                >
                  Batal
                </button>
                <button 
                  type="submit"
                  className="w-1/2 bg-brand text-white py-3 rounded-xl hover:bg-brand-dark shadow-lg transition-colors font-bold"
                >
                  Simpan ke Katalog
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
