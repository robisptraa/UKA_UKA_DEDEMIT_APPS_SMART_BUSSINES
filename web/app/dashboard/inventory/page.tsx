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
  ChevronDown,
  Download,
  Filter,
  Eye,
  FileSpreadsheet
} from "lucide-react";
import { toast } from "react-hot-toast";

interface CatalogItem {
  id: string;
  name: string;
  category: string;
  type: "product" | "service";
  price: number;
  stock: number | null; // null for service
  unit: string;
  imageUrl: string;
  isActive: boolean;
}

export default function InventoryPage() {
  // Mock data universal UMKM
  const [items, setItems] = useState<CatalogItem[]>([
    { id: "ITEM-101", name: "Kopi Aren Melted Latte", category: "Kuliner", type: "product", price: 22000, stock: 120, unit: "cup", imageUrl: "https://images.unsplash.com/photo-1541167760496-1628856ab772?w=400&q=80", isActive: true },
    { id: "ITEM-102", name: "T-Shirt Oversized Streetwear Noir", category: "Fashion", type: "product", price: 185000, stock: 15, unit: "pcs", imageUrl: "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=400&q=80", isActive: true },
    { id: "ITEM-103", name: "Hair Treatment + Creambath Herbal", category: "Kecantikan", type: "service", price: 250000, stock: null, unit: "sesi", imageUrl: "https://images.unsplash.com/photo-1562322140-8baeececf3df?w=400&q=80", isActive: true },
    { id: "ITEM-104", name: "Layanan Cuci Kering Kilat 5kg", category: "Laundry", type: "service", price: 45000, stock: null, unit: "order", imageUrl: "https://images.unsplash.com/photo-1545173168-9f18d8219973?w=400&q=80", isActive: true },
    { id: "ITEM-105", name: "Beras Premium Pandan Wangi 5kg", category: "Sembako", type: "product", price: 75000, stock: 2, unit: "pack", imageUrl: "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&q=80", isActive: true },
    { id: "ITEM-106", name: "Servis Sepeda Motor Honda Beat", category: "Bengkel", type: "service", price: 95000, stock: null, unit: "sesi", imageUrl: "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400&q=80", isActive: true },
    { id: "ITEM-107", name: "Biji Kopi House Blend Arabica 1kg", category: "Kuliner", type: "product", price: 165000, stock: 4, unit: "pack", imageUrl: "https://images.unsplash.com/photo-1498804103079-a6351b050096?w=400&q=80", isActive: false },
    { id: "ITEM-108", name: "Croissant Almond Premium", category: "Kuliner", type: "product", price: 25000, stock: 24, unit: "pcs", imageUrl: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400&q=80", isActive: true },
  ]);

  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState<"all" | "product" | "service">("all");
  const [filterCategory, setFilterCategory] = useState("all");
  const [filterStatus, setFilterStatus] = useState<"all" | "active" | "inactive">("all");
  const [sortField, setSortField] = useState<"name" | "price" | "stock">("name");
  const [sortAsc, setSortAsc] = useState(true);

  // Bulk Action State
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<"add" | "edit">("add");
  const [editItemId, setEditItemId] = useState<string | null>(null);

  // Form Fields
  const [name, setName] = useState("");
  const [category, setCategory] = useState("Kuliner");
  const [type, setType] = useState<"product" | "service">("product");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("10");
  const [unit, setUnit] = useState("pcs");
  const [imageUrl, setImageUrl] = useState("");
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Filtered & Sorted list
  const filteredItems = items
    .filter(item => {
      const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            item.category.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesType = filterType === "all" || item.type === filterType;
      const matchesCategory = filterCategory === "all" || item.category === filterCategory;
      const matchesStatus = filterStatus === "all" || 
                            (filterStatus === "active" && item.isActive) || 
                            (filterStatus === "inactive" && !item.isActive);
      return matchesSearch && matchesType && matchesCategory && matchesStatus;
    })
    .sort((a, b) => {
      let valA = a[sortField];
      let valB = b[sortField];
      
      if (valA === null) valA = -1;
      if (valB === null) valB = -1;

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

  // Selection handlers
  const toggleSelect = (id: string) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === filteredItems.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(filteredItems.map(item => item.id));
    }
  };

  // Bulk Actions
  const handleBulkToggleActive = (activeState: boolean) => {
    if (selectedIds.length === 0) return;
    setItems(prev => 
      prev.map(item => selectedIds.includes(item.id) ? { ...item, isActive: activeState } : item)
    );
    setSelectedIds([]);
    toast.success(`Sukses memperbarui status ${selectedIds.length} item! ⚡`, {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  const handleBulkDelete = () => {
    if (selectedIds.length === 0) return;
    setItems(prev => prev.filter(item => !selectedIds.includes(item.id)));
    setSelectedIds([]);
    toast.error(`Berhasil menghapus ${selectedIds.length} item dari katalog! 🗑️`, {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  // CSV Simulators
  const handleCSVImportClick = () => {
    fileInputRef.current?.click();
  };

  const handleCSVFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      toast.loading("Membaca berkas CSV...", { id: "csv" });
      
      setTimeout(() => {
        const imported: CatalogItem[] = [
          { id: `ITEM-${Date.now()}-1`, name: "Es Teh Manis Selasih", category: "Kuliner", type: "product", price: 8000, stock: 150, unit: "cup", imageUrl: "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&q=80", isActive: true },
          { id: `ITEM-${Date.now()}-2`, name: "Jasa Lipat Gosok Premium 1kg", category: "Laundry", type: "service", price: 12000, stock: null, unit: "kg", imageUrl: "https://images.unsplash.com/photo-1545173168-9f18d8219973?w=400&q=80", isActive: true },
        ];
        setItems(prev => [...prev, ...imported]);
        toast.dismiss("csv");
        toast.success("Sukses mengimpor 2 item baru dari CSV! 📦", {
          style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
        });
      }, 1500);
    }
  };

  const downloadCSVTemplate = () => {
    toast.success("Mendownload dedemit_inventory_template.csv! 📄", {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  // Form submit handler
  const handleSaveItem = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !price) {
      toast.error("Nama dan harga wajib diisi!");
      return;
    }

    const priceNum = parseFloat(price) || 0;
    const stockNum = type === "product" ? parseInt(stock) || 0 : null;

    if (modalMode === "add") {
      const newItem: CatalogItem = {
        id: `ITEM-${100 + items.length + 1}`,
        name,
        category,
        type,
        price: priceNum,
        stock: stockNum,
        unit,
        imageUrl: imagePreview || "https://images.unsplash.com/photo-1541167760496-1628856ab772?w=400&q=80",
        isActive: true
      };
      setItems([newItem, ...items]);
      toast.success("Item baru berhasil ditambahkan! 🎉");
    } else {
      setItems(prev => prev.map(item => 
        item.id === editItemId 
          ? { 
              ...item, 
              name, 
              category, 
              type, 
              price: priceNum, 
              stock: stockNum, 
              unit, 
              imageUrl: imagePreview || item.imageUrl 
            } 
          : item
      ));
      toast.success("Item berhasil diperbarui! 📝");
    }

    setIsModalOpen(false);
    resetForm();
  };

  const handleEditItem = (item: CatalogItem) => {
    setModalMode("edit");
    setEditItemId(item.id);
    setName(item.name);
    setCategory(item.category);
    setType(item.type);
    setPrice(item.price.toString());
    setStock(item.stock?.toString() || "0");
    setUnit(item.unit);
    setImagePreview(item.imageUrl);
    setIsModalOpen(true);
  };

  const resetForm = () => {
    setName("");
    setCategory("Kuliner");
    setType("product");
    setPrice("");
    setStock("10");
    setUnit("pcs");
    setImagePreview(null);
    setEditItemId(null);
  };

  return (
    <div className="space-y-8 font-mono text-xs">
      {/* HEADER INVENTORY */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2 font-sans">
            Katalog Inventori UMKM <span className="animate-pulse">📦</span>
          </h2>
          <p className="text-[10px] text-zinc-500">Kelola terpadu produk fisik (barang) maupun paket jasa. Tipe jasa otomatis menonaktifkan penghitung stok.</p>
        </div>

        {/* Action CTAs */}
        <div className="flex flex-wrap items-center gap-3">
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleCSVFileChange}
            accept=".csv" 
            className="hidden" 
          />
          <button 
            onClick={downloadCSVTemplate}
            className="flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-950 text-zinc-400 hover:text-white transition-all font-bold"
          >
            <Download className="w-3.5 h-3.5" /> Template
          </button>
          
          <button 
            onClick={handleCSVImportClick}
            className="flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-900 text-zinc-300 hover:text-white transition-all font-bold"
          >
            <Upload className="w-3.5 h-3.5" /> Impor CSV
          </button>
          
          <button 
            onClick={() => { setModalMode("add"); resetForm(); setIsModalOpen(true); }}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-brand hover:bg-brand-dark text-white shadow-lg hover:shadow-brand/20 transition-all font-bold font-sans text-xs"
          >
            <Plus className="w-4 h-4" /> + Tambah Item
          </button>
        </div>
      </header>

      {/* ================= CONTROLS & FILTER SECTION ================= */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search Bar */}
        <div className="lg:col-span-1 relative">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-zinc-500">
            <Search className="w-3.5 h-3.5" />
          </span>
          <input 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Cari nama item/kategori..."
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-2.5 pl-9 pr-3 text-zinc-200 focus:outline-none focus:border-brand-light transition-all"
          />
        </div>

        {/* Filter Type */}
        <div className="relative">
          <select 
            value={filterType}
            onChange={(e) => setFilterType(e.target.value as any)}
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none focus:border-brand-light transition-all appearance-none"
          >
            <option value="all">Semua Tipe (Barang & Jasa)</option>
            <option value="product">📦 Produk Fisik</option>
            <option value="service">🛠️ Jasa / Layanan</option>
          </select>
          <span className="absolute inset-y-0 right-3 flex items-center pointer-events-none text-zinc-500">
            <ChevronDown className="w-3.5 h-3.5" />
          </span>
        </div>

        {/* Filter Kategori */}
        <div className="relative">
          <select 
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none focus:border-brand-light transition-all appearance-none"
          >
            <option value="all">Semua Sektor UMKM</option>
            <option value="Kuliner">🍜 Kuliner</option>
            <option value="Fashion">👗 Fashion</option>
            <option value="Kecantikan">💄 Kecantikan</option>
            <option value="Laundry">🧺 Laundry</option>
            <option value="Sembako">🛒 Sembako</option>
            <option value="Bengkel">🔧 Bengkel</option>
          </select>
          <span className="absolute inset-y-0 right-3 flex items-center pointer-events-none text-zinc-500">
            <ChevronDown className="w-3.5 h-3.5" />
          </span>
        </div>

        {/* Filter Status */}
        <div className="relative">
          <select 
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value as any)}
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none focus:border-brand-light transition-all appearance-none"
          >
            <option value="all">Semua Status</option>
            <option value="active">Aktif</option>
            <option value="inactive">Nonaktif</option>
          </select>
          <span className="absolute inset-y-0 right-3 flex items-center pointer-events-none text-zinc-500">
            <ChevronDown className="w-3.5 h-3.5" />
          </span>
        </div>
      </section>

      {/* ================= BULK ACTIONS PANEL ================= */}
      {selectedIds.length > 0 && (
        <div className="p-4 bg-brand/5 border border-brand/20 rounded-2xl flex items-center justify-between animate-fade-in">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-brand animate-pulse" />
            <span className="text-zinc-300 font-bold uppercase">{selectedIds.length} Item Terpilih:</span>
          </div>

          <div className="flex items-center gap-2">
            <button 
              onClick={() => handleBulkToggleActive(true)}
              className="px-3 py-1.5 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-brand rounded-lg hover:text-white transition-colors font-bold"
            >
              Aktifkan
            </button>
            <button 
              onClick={() => handleBulkToggleActive(false)}
              className="px-3 py-1.5 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-yellow-500 rounded-lg hover:text-white transition-colors font-bold"
            >
              Nonaktifkan
            </button>
            <button 
              onClick={handleBulkDelete}
              className="p-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* ================= INVENTORY DATATABLE ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-zinc-800 text-zinc-500 uppercase tracking-wider">
                <th className="py-4 pl-2 pr-4 w-10">
                  <input 
                    type="checkbox" 
                    checked={selectedIds.length === filteredItems.length && filteredItems.length > 0}
                    onChange={toggleSelectAll}
                    className="accent-brand rounded"
                  />
                </th>
                <th className="py-4 w-16">FOTO</th>
                <th className="py-4 hover:text-white cursor-pointer" onClick={() => handleSort("name")}>
                  ITEM <ArrowUpDown className="w-3 h-3 inline ml-1" />
                </th>
                <th className="py-4">KATEGORI</th>
                <th className="py-4">TIPE</th>
                <th className="py-4 text-right hover:text-white cursor-pointer" onClick={() => handleSort("price")}>
                  HARGA <ArrowUpDown className="w-3 h-3 inline ml-1" />
                </th>
                <th className="py-4 text-right hover:text-white cursor-pointer" onClick={() => handleSort("stock")}>
                  STOK <ArrowUpDown className="w-3 h-3 inline ml-1" />
                </th>
                <th className="py-4 pl-6 w-24">STATUS</th>
                <th className="py-4 text-center w-20">AKSI</th>
              </tr>
            </thead>
            <tbody>
              {filteredItems.length === 0 ? (
                <tr>
                  <td colSpan={9} className="py-8 text-center text-zinc-500">Tidak ada produk/jasa ditemukan. Coba ubah kata kunci pencarian.</td>
                </tr>
              ) : (
                filteredItems.map((p) => (
                  <tr key={p.id} className="border-b border-zinc-800/50 hover:bg-zinc-950/40 transition-colors">
                    <td className="py-4 pl-2 pr-4">
                      <input 
                        type="checkbox" 
                        checked={selectedIds.includes(p.id)}
                        onChange={() => toggleSelect(p.id)}
                        className="accent-brand rounded"
                      />
                    </td>
                    <td className="py-2">
                      <div className="w-10 h-10 rounded-lg overflow-hidden border border-zinc-800 bg-zinc-950 flex items-center justify-center">
                        {p.imageUrl ? (
                          <img src={p.imageUrl} alt={p.name} className="w-full h-full object-cover" />
                        ) : (
                          <Package className="w-4 h-4 text-zinc-600" />
                        )}
                      </div>
                    </td>
                    <td className="py-4">
                      <span className="text-white font-bold block max-w-[200px] truncate">{p.name}</span>
                      <span className="text-[9px] text-zinc-500 font-mono">{p.id}</span>
                    </td>
                    <td className="py-4 text-zinc-400">{p.category}</td>
                    <td className="py-4">
                      <span className={`px-2 py-0.5 rounded text-[8px] font-extrabold uppercase font-mono ${
                        p.type === "product" ? "bg-teal-500/10 text-teal-400" : "bg-purple-500/10 text-purple-400"
                      }`}>
                        {p.type === "product" ? "Barang" : "Jasa"}
                      </span>
                    </td>
                    <td className="py-4 text-right text-brand-ghost font-bold">Rp {p.price.toLocaleString("id-ID")}</td>
                    <td className="py-4 text-right font-bold pr-2">
                      {p.stock !== null ? (
                        <span className={p.stock <= 2 ? "text-red-400 animate-pulse font-extrabold" : "text-zinc-300"}>
                          {p.stock} <span className="text-[9px] text-zinc-500 font-normal">{p.unit}</span>
                        </span>
                      ) : (
                        <span className="text-zinc-600 font-normal italic">s.d (Unlimited)</span>
                      )}
                    </td>
                    <td className="py-4 pl-6">
                      <span className={`px-2.5 py-0.5 rounded text-[9px] font-extrabold uppercase ${
                        p.isActive 
                          ? "bg-brand/10 text-brand border border-brand/20" 
                          : "bg-zinc-800 text-zinc-400"
                      }`}>
                        {p.isActive ? "✓ Aktif" : "✕ Nonaktif"}
                      </span>
                    </td>
                    <td className="py-4 text-center">
                      <button 
                        onClick={() => handleEditItem(p)}
                        className="px-2 py-1 bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 rounded-lg text-brand-ghost transition-colors inline-flex items-center gap-1 font-bold"
                      >
                        Edit
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* ================= MODAL ADD/EDIT ITEM OVERLAY ================= */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="fixed inset-0 bg-black/75 backdrop-blur-sm" onClick={() => setIsModalOpen(false)} />
          
          <div className="w-full max-w-lg bg-zinc-900 border border-zinc-800 rounded-3xl p-6 relative z-50 text-xs font-mono">
            <div className="flex justify-between items-center pb-4 border-b border-zinc-800 mb-5">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-1.5 font-sans">
                <Package className="w-4 h-4 text-brand-ghost" /> {modalMode === "add" ? "+ Tambah Item Baru" : "📝 Edit Detail Item"}
              </h3>
              <button 
                onClick={() => setIsModalOpen(false)}
                className="p-1 rounded-lg text-zinc-500 hover:text-white hover:bg-zinc-800"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveItem} className="space-y-4">
              <div>
                <label className="text-zinc-500 block mb-1">NAMA ITEM CATALOG *</label>
                <input 
                  type="text" 
                  required
                  placeholder="Contoh: Kopi Aren Gula Semut, Potong Rambut Undercut..."
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-200 focus:outline-none focus:border-brand-light"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                 <div>
                   <label className="text-zinc-500 block mb-1">TIPE KATALOG</label>
                   <select 
                     value={type}
                     onChange={(e) => setType(e.target.value as any)}
                     className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
                   >
                     <option value="product">📦 Produk Fisik (Stok Dihitung)</option>
                     <option value="service">🛠️ Jasa / Layanan (Stok Unlimited)</option>
                   </select>
                 </div>
                 <div>
                   <label className="text-zinc-500 block mb-1">KATEGORI SEKTOR</label>
                   <select 
                     value={category}
                     onChange={(e) => setCategory(e.target.value)}
                     className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
                   >
                     <option value="Kuliner">Kuliner</option>
                     <option value="Fashion">Fashion</option>
                     <option value="Kecantikan">Kecantikan</option>
                     <option value="Laundry">Laundry</option>
                     <option value="Sembako">Sembako</option>
                     <option value="Bengkel">Bengkel</option>
                   </select>
                 </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-zinc-500 block mb-1">HARGA JUAL (RP) *</label>
                  <input 
                    type="number" 
                    required
                    placeholder="25000"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-200 focus:outline-none"
                  />
                </div>
                
                {type === "product" ? (
                  <div>
                    <label className="text-zinc-500 block mb-1">STOK & SATUAN</label>
                    <div className="flex gap-2">
                      <input 
                        type="number" 
                        value={stock}
                        onChange={(e) => setStock(e.target.value)}
                        className="w-2/3 bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-200 focus:outline-none"
                      />
                      <input 
                        type="text" 
                        placeholder="cup/pcs"
                        value={unit}
                        onChange={(e) => setUnit(e.target.value)}
                        className="w-1/3 bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none text-center"
                      />
                    </div>
                  </div>
                ) : (
                  <div>
                    <label className="text-zinc-500 block mb-1">SATUAN JASA</label>
                    <input 
                      type="text" 
                      placeholder="sesi/jam"
                      value={unit}
                      onChange={(e) => setUnit(e.target.value)}
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none text-center"
                    />
                  </div>
                )}
              </div>

              {/* Simulation Photo Upload */}
              <div>
                <label className="text-zinc-500 block mb-1">SIMULASI UNGGAH FOTO</label>
                <div 
                  onClick={() => {
                    setImagePreview("https://images.unsplash.com/photo-1541167760496-1628856ab772?w=400&q=80");
                    toast.success("Foto kopi arending berhasil disimulasikan!");
                  }}
                  className="w-full border border-dashed border-zinc-800 hover:border-brand/40 rounded-xl h-20 flex flex-col justify-center items-center cursor-pointer text-zinc-500 hover:text-brand-ghost transition-all bg-zinc-950/40 relative overflow-hidden"
                >
                  {imagePreview ? (
                    <div className="absolute inset-0 bg-cover bg-center filter brightness-75 animate-fade-in" style={{backgroundImage: `url('${imagePreview}')`}} />
                  ) : (
                    <>
                      <Upload className="w-4 h-4 mb-1" />
                      <span>Klik untuk simulasi upload foto produk/jasa</span>
                    </>
                  )}
                </div>
              </div>

              <div className="pt-2 flex gap-3">
                <button 
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="w-1/2 border border-zinc-800 text-zinc-400 py-3 rounded-xl hover:bg-zinc-850 hover:text-white transition-colors font-bold"
                >
                  Batal
                </button>
                <button 
                  type="submit"
                  className="w-1/2 bg-brand text-white py-3 rounded-xl hover:bg-brand-dark shadow-lg transition-colors font-bold"
                >
                  {modalMode === "add" ? "Simpan ke Katalog" : "Perbarui Item"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
