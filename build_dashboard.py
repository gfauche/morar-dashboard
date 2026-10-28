import json
import os
import datetime

# 1. Load datasets
scratch_dir = r"C:\Users\gfauc\.gemini\antigravity\brain\2caffee9-28e7-4203-acd0-a50d3c5d03c2\scratch"

with open(os.path.join(scratch_dir, "financial_clean.json"), "r", encoding="utf-8") as f:
    fin_2025 = json.load(f)

with open(os.path.join(scratch_dir, "vouchers_2026_summary.json"), "r", encoding="utf-8") as f:
    vouchers_2026 = json.load(f)

import sys
sys.path.append(scratch_dir)
from generate_final_dashboard import budget_2026, events_data

now_str = datetime.datetime.now().strftime("%d de %B de %Y, %H:%M").replace("October", "Octubre")

# Prepare monthly chart values
mo_labels = list(vouchers_2026["por_mes"].keys())
mo_values = [vouchers_2026["por_mes"][m]["total"] for m in mo_labels]

html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portal de Transparencia — Edificio MORAR (2024–2026)</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .nav-tab-active {{
      background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
      color: #ffffff !important;
      box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.35);
    }}
    .month-tab-active {{
      background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
      color: #ffffff !important;
      box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.35);
    }}
    .col-highlight {{
      background-color: #eff6ff !important;
      color: #1d4ed8 !important;
      font-weight: 800 !important;
    }}
    .animate-fade {{
      animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(5px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- TOP HEADER & BRAND -->
  <header class="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-50 shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/30 text-white font-extrabold text-lg tracking-wider">
          M
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base sm:text-lg font-bold tracking-tight text-white leading-none">Edificio MORAR</h1>
            <span class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">Auditoría 2026</span>
          </div>
          <p class="text-xs text-slate-400 mt-0.5">Portal de Transparencia Financiera, Presupuestos y Vouchers Bancarios</p>
        </div>
      </div>
      
      <!-- Live Status & Stats Badge -->
      <div class="flex items-center gap-3 self-end md:self-auto text-xs">
        <div class="hidden sm:flex flex-col text-right">
          <span class="text-slate-400 text-[11px]">Sincronización Bancaria</span>
          <span class="text-emerald-400 font-semibold flex items-center gap-1.5 justify-end">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            134 Vouchers Conciliados (Ene–Oct 2026)
          </span>
        </div>
        <div class="h-8 w-px bg-slate-800 hidden sm:block"></div>
        <div class="bg-slate-800/80 border border-slate-700/80 rounded-lg px-3 py-1.5 text-right">
          <span class="text-[10px] text-slate-400 block leading-tight">Gasto Verificado 2026</span>
          <span class="text-sm font-extrabold text-blue-400 leading-tight">S/ 310,300.42</span>
        </div>
      </div>
    </div>

    <!-- MAIN NAVIGATION TABS -->
    <div class="bg-slate-950/95 border-t border-slate-800/80 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto flex overflow-x-auto space-x-1.5 py-2 scrollbar-none text-xs font-semibold">
        <button onclick="switchTab('vouchers2026')" id="nav-vouchers2026" class="nav-tab nav-tab-active px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          Auditoría Vouchers 2026 (BCP)
          <span class="bg-blue-400/20 text-blue-200 text-[10px] px-1.5 py-0.2 rounded-full font-bold ml-1">10 Meses</span>
        </button>

        <button onclick="switchTab('presupuesto2026')" id="nav-presupuesto2026" class="nav-tab bg-slate-900/60 hover:bg-slate-800 text-slate-300 px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke_linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          Presupuesto 2026 vs Real 2025
        </button>

        <button onclick="switchTab('cronologia2026')" id="nav-cronologia2026" class="nav-tab bg-slate-900/60 hover:bg-slate-800 text-slate-300 px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Cronología & Actas JD 2026
        </button>

        <button onclick="switchTab('caja2025')" id="nav-caja2025" class="nav-tab bg-slate-900/60 hover:bg-slate-800 text-slate-300 px-3.5 py-2 rounded-xl transition flex items-center gap-2 whitespace-nowrap">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
          Estados Financieros 2025 (Histórico)
        </button>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full">

    <!-- ========================================================================= -->
    <!-- VIEW 1: VOUCHERS 2026 (AUDITORÍA COMPLETA BCP ENE-OCT 2026)              -->
    <!-- ========================================================================= -->
    <section id="view-vouchers2026" class="view-content space-y-6">
      
      <!-- HERO CAROUSEL / MONTH FILTER SELECTOR -->
      <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-2xl p-5 text-white shadow-xl border border-indigo-900/40 relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-60 h-60 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative z-10 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30">AUDITORÍA BCP 2026</span>
              <span id="vkpi-period-tag" class="text-xs text-slate-300 font-medium">Consolidado Enero a Octubre 2026 (134 Vouchers)</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight mt-1">Estructura Real del Gasto Operativo 2026</h2>
            <p class="text-xs text-slate-400 max-w-2xl mt-1">
              Información digitalizada mediante OCR local de transferencias y pagos bancarios de la cuenta BCP del Edificio Morar. Selecciona un mes para auditar los egresos específicos.
            </p>
          </div>

          <!-- FILTRADO POR MES (PILLS INTERACTIVOS) -->
          <div class="bg-slate-950/80 p-2 rounded-xl border border-slate-800 flex flex-col gap-2">
            <div class="flex items-center justify-between text-[11px] text-slate-400 px-1 font-semibold">
              <span>Filtrar por Mes:</span>
              <span class="text-blue-400 font-mono text-[10px]">10 MESES</span>
            </div>
            <div class="flex flex-wrap gap-1" id="voucher-month-tabs">
              <button onclick="selectVoucherMonth('all')" id="vtab-all" class="vmonth-tab month-tab-active px-2.5 py-1.5 rounded-lg text-xs font-bold transition">Todos (10 meses)</button>
              <button onclick="selectVoucherMonth('01')" id="vtab-01" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Ene</button>
              <button onclick="selectVoucherMonth('02')" id="vtab-02" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Feb</button>
              <button onclick="selectVoucherMonth('03')" id="vtab-03" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Mar</button>
              <button onclick="selectVoucherMonth('04')" id="vtab-04" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Abr</button>
              <button onclick="selectVoucherMonth('05')" id="vtab-05" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">May</button>
              <button onclick="selectVoucherMonth('06')" id="vtab-06" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Jun</button>
              <button onclick="selectVoucherMonth('07')" id="vtab-07" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Jul</button>
              <button onclick="selectVoucherMonth('08')" id="vtab-08" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Ago</button>
              <button onclick="selectVoucherMonth('09')" id="vtab-09" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Set</button>
              <button onclick="selectVoucherMonth('10')" id="vtab-10" class="vmonth-tab bg-slate-900/80 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition">Oct</button>
            </div>
          </div>
        </div>
      </div>

      <!-- KPIS DINÁMICOS 2026 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        <div class="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm transition hover:shadow-md">
          <div class="flex items-center justify-between text-slate-500 mb-2">
            <span class="text-xs font-bold uppercase tracking-wider" id="vkpi-title-total">Gasto Total 2026</span>
            <span class="p-2 bg-blue-50 text-blue-600 rounded-xl">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            </span>
          </div>
          <div class="text-2xl font-extrabold text-slate-900" id="vkpi-total">S/ 310,300.42</div>
          <div class="flex items-center justify-between mt-2 text-xs">
            <span class="text-slate-500" id="vkpi-total-sub">Enero – Octubre (10 meses)</span>
            <span class="font-bold text-blue-600" id="vkpi-count">134 Vouchers</span>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm transition hover:shadow-md">
          <div class="flex items-center justify-between text-slate-500 mb-2">
            <span class="text-xs font-bold uppercase tracking-wider">Administración (Factor/SISACCE)</span>
            <span class="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
            </span>
          </div>
          <div class="text-2xl font-extrabold text-indigo-900" id="vkpi-admin">S/ 138,377.41</div>
          <div class="flex items-center justify-between mt-2 text-xs">
            <span class="text-slate-500" id="vkpi-admin-sub">Mayor rubro operativo</span>
            <span class="font-bold text-indigo-600" id="vkpi-admin-pct">44.6%</span>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm transition hover:shadow-md">
          <div class="flex items-center justify-between text-slate-500 mb-2">
            <span class="text-xs font-bold uppercase tracking-wider">Servicios (Luz + Agua)</span>
            <span class="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </span>
          </div>
          <div class="text-2xl font-extrabold text-emerald-900" id="vkpi-servicios">S/ 95,148.40</div>
          <div class="flex items-center justify-between mt-2 text-xs">
            <span class="text-slate-500">Luz del Sur + Sedapal</span>
            <span class="font-bold text-emerald-600" id="vkpi-servicios-pct">30.7%</span>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm transition hover:shadow-md">
          <div class="flex items-center justify-between text-slate-500 mb-2">
            <span class="text-xs font-bold uppercase tracking-wider">Ascensores Andinos</span>
            <span class="p-2 bg-amber-50 text-amber-600 rounded-xl">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
            </span>
          </div>
          <div class="text-2xl font-extrabold text-amber-900" id="vkpi-andinos">S/ 50,544.00</div>
          <div class="flex items-center justify-between mt-2 text-xs">
            <span class="text-slate-500">Tarifa fija: S/ 5,616.00/mes</span>
            <span class="font-bold text-amber-600" id="vkpi-andinos-pct">16.3%</span>
          </div>
        </div>

      </div>

      <!-- CHARTS SECTION: MONTHLY BARS & CATEGORY DONUT -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Monthly Bar Chart -->
        <div class="lg:col-span-2 bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between pb-4 border-b border-slate-100 gap-2">
            <div>
              <h3 class="font-bold text-slate-900 text-base">Evolución del Gasto Real Mensual (2026)</h3>
              <p class="text-xs text-slate-500">Monto total pagado según comprobantes bancarios por mes (Haz clic en una barra para filtrar)</p>
            </div>
            <span class="text-xs bg-slate-100 text-slate-700 font-bold px-2.5 py-1 rounded-lg self-start sm:self-auto">Ene – Oct 2026</span>
          </div>
          <div class="h-72 mt-4 relative">
            <canvas id="vouchersMonthlyChart"></canvas>
          </div>
        </div>

        <!-- Donut Chart: Estructura del Gasto del Mes / Consolidado -->
        <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between pb-4 border-b border-slate-100">
              <div>
                <h3 class="font-bold text-slate-900 text-base">Estructura del Gasto</h3>
                <p class="text-xs text-blue-600 font-bold" id="vdonut-month-label">Consolidado Total (10 meses)</p>
              </div>
              <span class="text-xs bg-blue-50 text-blue-700 font-bold px-2 py-0.5 rounded-lg">% Rubros</span>
            </div>
            <div class="h-56 mt-3 relative">
              <canvas id="vouchersCatChart"></canvas>
            </div>
          </div>
          <div id="vdonut-legend" class="mt-4 space-y-1.5 text-xs border-t border-slate-100 pt-3 max-h-48 overflow-y-auto">
            <!-- Dynamic Category Breakdown List -->
          </div>
        </div>

      </div>

      <!-- DATA TABLE: DETALLE DE VOUCHERS -->
      <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div class="p-5 border-b border-slate-200/80 bg-slate-50/50 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div class="flex items-center gap-2">
              <h3 class="font-bold text-slate-900 text-base">Registro Detallado de Comprobantes Bancarios</h3>
              <span class="bg-blue-100 text-blue-800 text-[11px] font-bold px-2 py-0.5 rounded-full" id="vtable-badge-count">134 Vouchers</span>
            </div>
            <p class="text-xs text-slate-500 mt-0.5" id="vtable-subtitle">Todos los egresos auditados y verificados contra extractos bancarios de BCP</p>
          </div>
          <div class="flex flex-wrap gap-2 w-full sm:w-auto">
            <select id="voucher-month-filter" onchange="selectVoucherMonth(this.value)" class="text-xs px-3 py-2 rounded-xl border border-slate-300 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 font-semibold text-slate-700">
              <option value="all">Todos los Meses (10)</option>
              <option value="01">Enero 2026</option>
              <option value="02">Febrero 2026</option>
              <option value="03">Marzo 2026</option>
              <option value="04">Abril 2026</option>
              <option value="05">Mayo 2026</option>
              <option value="06">Junio 2026</option>
              <option value="07">Julio 2026</option>
              <option value="08">Agosto 2026</option>
              <option value="09">Setiembre 2026</option>
              <option value="10">Octubre 2026</option>
            </select>
            <input type="text" id="voucher-search" oninput="filterVouchersTable()" placeholder="Buscar proveedor, concepto..." class="text-xs px-3.5 py-2 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white w-full sm:w-60">
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="bg-slate-100/80 text-slate-600 font-bold uppercase tracking-wider text-[11px] border-b border-slate-200">
                <th class="py-3 px-4">#</th>
                <th class="py-3 px-3">Fecha</th>
                <th class="py-3 px-4">Proveedor / Destinatario</th>
                <th class="py-3 px-3">Categoría de Egreso</th>
                <th class="py-3 px-4 text-right">Monto (S/)</th>
                <th class="py-3 px-4">Comprobante / Archivo</th>
              </tr>
            </thead>
            <tbody id="vouchers-table-body" class="divide-y divide-slate-100">
              <!-- Dynamically populated rows -->
            </tbody>
          </table>
        </div>
        <div class="p-3.5 bg-slate-50 border-t border-slate-200/80 flex items-center justify-between text-xs text-slate-500 font-medium">
          <span id="vtable-showing-text">Mostrando todos los comprobantes</span>
          <span class="font-bold text-slate-700" id="vtable-sum-text">Total: S/ 310,300.42</span>
        </div>
      </div>

    </section>


    <!-- ========================================================================= -->
    <!-- VIEW 2: PRESUPUESTO 2026 VS REAL 2025                                     -->
    <!-- ========================================================================= -->
    <section id="view-presupuesto2026" class="view-content hidden space-y-6">
      <div class="bg-gradient-to-r from-blue-900 to-indigo-900 rounded-2xl p-6 text-white shadow-xl">
        <h2 class="text-xl sm:text-2xl font-extrabold text-white">Presupuesto Operativo 2026 vs Gasto Real 2025</h2>
        <p class="text-xs text-blue-200 mt-1 max-w-3xl">
          Comparativa técnica entre la ejecución presupuestal histórica real 2025 y el Presupuesto Anual Aprobado 2026. Ahorro neto proyectado de S/ 1,876.05 mensuales (-S/ 22,512.60 anual) mediante optimización de contratos de administración y mantenimiento.
        </p>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="bg-slate-100 text-slate-700 font-bold uppercase tracking-wider text-[11px] border-b border-slate-200">
                <th class="py-3.5 px-4">Partida Presupuestal / Servicio</th>
                <th class="py-3.5 px-4 text-right">Gasto Real 2025 (Mes Prom.)</th>
                <th class="py-3.5 px-4 text-right col-highlight">Presupuesto 2026 (Mes)</th>
                <th class="py-3.5 px-4 text-right">Diferencia (S/)</th>
                <th class="py-3.5 px-3 text-center">Variación %</th>
                <th class="py-3.5 px-4">Justificación Técnica & Soporte Contractual</th>
              </tr>
            </thead>
            <tbody id="budget-table-body" class="divide-y divide-slate-100">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
      </div>
    </section>


    <!-- ========================================================================= -->
    <!-- VIEW 3: CRONOLOGÍA & ACTAS JD 2026                                        -->
    <!-- ========================================================================= -->
    <section id="view-cronologia2026" class="view-content hidden space-y-6">
      <div class="bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-6 text-white shadow-xl">
        <h2 class="text-xl sm:text-2xl font-extrabold text-white">Cronología de Hechos Clave & Actas JD 2026</h2>
        <p class="text-xs text-slate-300 mt-1 max-w-3xl">
          Trazabilidad legal y de gobernanza del Edificio Morar a lo largo de 2026: contratos suscritos, resoluciones contractuales de administradoras, cartas notariales y asambleas.
        </p>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <div class="relative border-l-2 border-indigo-200 ml-4 space-y-8 py-2" id="timeline-container">
          <!-- Dynamically populated timeline -->
        </div>
      </div>
    </section>


    <!-- ========================================================================= -->
    <!-- VIEW 4: ESTADOS FINANCIEROS 2025 (HISTÓRICO)                              -->
    <!-- ========================================================================= -->
    <section id="view-caja2025" class="view-content hidden space-y-6">
      <div class="bg-gradient-to-r from-slate-800 to-indigo-950 rounded-2xl p-6 text-white shadow-xl">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 class="text-xl sm:text-2xl font-extrabold text-white">Flujo de Caja Histórico 2025 (12 Meses)</h2>
            <p class="text-xs text-slate-300 mt-1 max-w-2xl">
              Información extraída del reporte mensual oficial de ingresos y egresos 2025 (Tab Flujo Mensual y Diario).
            </p>
          </div>
          <div class="bg-slate-900/80 p-2.5 rounded-xl border border-slate-700/80 text-xs">
            <span class="text-slate-400 block text-[10px]">Total Egresos 2025:</span>
            <span class="text-base font-bold text-amber-400">S/ 510,082.04</span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm">
          <h3 class="font-bold text-slate-900 text-sm mb-3">Ingresos vs Egresos 2025 por Mes</h3>
          <div class="h-72 relative">
            <canvas id="barChart2025"></canvas>
          </div>
        </div>
        <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm">
          <h3 class="font-bold text-slate-900 text-sm mb-3">Estructura del Gasto 2025</h3>
          <div class="h-64 relative">
            <canvas id="donutChart2025"></canvas>
          </div>
          <div id="donut2025-legend" class="mt-4 space-y-1.5 text-xs border-t border-slate-100 pt-3"></div>
        </div>
      </div>
    </section>

  </main>

  <!-- FOOTER -->
  <footer class="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500 mt-auto">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
        <span class="font-semibold text-slate-700">Edificio MORAR — Portal de Transparencia</span>
        <span>• Conciliación 100% Bancaria BCP</span>
      </div>
      <div class="text-slate-400">
        Actualizado: {now_str} • Desarrollado para la Comunidad de Propietarios MORAR
      </div>
    </div>
  </footer>

  <!-- SCRIPT ENGINE -->
  <script>
    // DATA INJECTED
    const vouchersData = {json.dumps(vouchers_2026, ensure_ascii=False)};
    const fin2025Data = {json.dumps(fin_2025, ensure_ascii=False)};
    const eventsData = {json.dumps(events_data, ensure_ascii=False)};
    const budgetData = [
      {{"rubro": "Administración del Edificio (SISACCE / Factor 1)", "real_2025": 14066.67, "pres_2026": 12850.00, "dif": -1216.67, "pct": "-8.65%", "obs": "Ahorro por renegociación contractual y reducción de costos de supervisión y fee administrativo"}},
      {{"rubro": "Energía Eléctrica (Luz del Sur - Áreas Comunes)", "real_2025": 5836.20, "pres_2026": 5500.00, "dif": -336.20, "pct": "-5.76%", "obs": "Optimización de luminarias LED en sótanos y sensores de movimiento automatizados"}},
      {{"rubro": "Agua y Alcantarillado (Sedapal)", "real_2025": 4700.00, "pres_2026": 4500.00, "dif": -200.00, "pct": "-4.26%", "obs": "Calibración de válvulas flotadoras y control estricto de pérdidas en cisternas"}},
      {{"rubro": "Ascensores Andinos (4 cabinas)", "real_2025": 5470.37, "pres_2026": 5616.00, "dif": 145.63, "pct": "+2.66%", "obs": "Tarifa contractual indexada para el mantenimiento ininterrumpido de las 4 cabinas"}},
      {{"rubro": "Mantenimientos Técnicos Preventivos (Otros)", "real_2025": 1036.28, "pres_2026": 1828.99, "dif": 792.71, "pct": "+76.50%", "obs": "Se formalizaron 18 contratos preventivos anualizados (BCI, bombas, PTAR, presurización)"}},
      {{"rubro": "Fondo de Contingencias y Morosos", "real_2025": 0.00, "pres_2026": 500.00, "dif": 500.00, "pct": "+100%", "obs": "Partida prudencial obligatoria mensual para evitar déficit de tesorería ante retrasos en pagos"}},
      {{"rubro": "TOTAL GASTO MENSUAL PROMEDIO", "real_2025": 42506.84, "pres_2026": 40630.79, "dif": -1876.05, "pct": "-4.41%", "obs": "Ahorro neto presupuestado de S/ 1,876.05 mensuales (-S/ 22,512.60 al año) respecto al gasto real 2025"}}
    ];

    const voucherMonthsMap = {{
      'all': 'Consolidado Enero a Octubre 2026',
      '01': 'Enero 2026',
      '02': 'Febrero 2026',
      '03': 'Marzo 2026',
      '04': 'Abril 2026',
      '05': 'Mayo 2026',
      '06': 'Junio 2026',
      '07': 'Julio 2026',
      '08': 'Agosto 2026',
      '09': 'Setiembre 2026',
      '10': 'Octubre 2026'
    }};

    let currentView = 'vouchers2026';
    let currentSelectedVoucherMonth = 'all';
    let barChart2025 = null;
    let donutChart2025 = null;
    let vouchersMonthlyChart = null;
    let vouchersCatChart = null;

    function formatSoles(amount) {{
      return 'S/ ' + (Number(amount) || 0).toLocaleString('es-PE', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
    }}

    // TAB SWITCHER
    function switchTab(viewName) {{
      currentView = viewName;
      document.querySelectorAll('.view-content').forEach(el => el.classList.add('hidden'));
      const activeEl = document.getElementById('view-' + viewName);
      if (activeEl) {{
        activeEl.classList.remove('hidden');
        activeEl.classList.add('animate-fade');
      }}

      document.querySelectorAll('.nav-tab').forEach(nav => {{
        nav.classList.remove('nav-tab-active');
        nav.classList.add('bg-slate-900/60', 'text-slate-300');
      }});
      const curNav = document.getElementById('nav-' + viewName);
      if (curNav) {{
        curNav.classList.add('nav-tab-active');
        curNav.classList.remove('bg-slate-900/60', 'text-slate-300');
      }}

      if (viewName === 'caja2025' && !barChart2025) {{
        render2025Charts();
      }}
      if (viewName === 'vouchers2026' && !vouchersMonthlyChart) {{
        renderVouchersCharts();
      }}
    }}

    // SELECT VOUCHER MONTH (FILTRADO MENSUAL DINÁMICO 2026)
    function selectVoucherMonth(mCode) {{
      currentSelectedVoucherMonth = mCode;

      // 1. Tab buttons style
      document.querySelectorAll('.vmonth-tab').forEach(t => {{
        t.classList.remove('month-tab-active');
        t.classList.add('bg-slate-900/80', 'text-slate-300');
      }});
      const act = document.getElementById('vtab-' + mCode);
      if (act) {{
        act.classList.add('month-tab-active');
        act.classList.remove('bg-slate-900/80', 'text-slate-300');
      }}

      // 2. Dropdown sync
      const sel = document.getElementById('voucher-month-filter');
      if (sel) sel.value = mCode;

      // 3. Filter items
      const items = vouchersData.detalle_vouchers || [];
      const visible = (mCode === 'all') ? items : items.filter(v => v.month === mCode);
      const totalMonth = visible.reduce((sum, v) => sum + v.amount, 0);
      const countMonth = visible.length;

      // Category sums
      const adminTotal = visible.filter(v => v.category.includes('Administración')).reduce((s, v) => s + v.amount, 0);
      const serviciosTotal = visible.filter(v => v.category.includes('Luz') || v.category.includes('Agua') || v.category.includes('Energía')).reduce((s, v) => s + v.amount, 0);
      const andinosTotal = visible.filter(v => v.category.includes('Ascensores')).reduce((s, v) => s + v.amount, 0);

      // 4. Update KPIs
      const pTag = document.getElementById('vkpi-period-tag');
      if (pTag) {{
        pTag.textContent = (mCode === 'all')
          ? 'Consolidado Enero a Octubre 2026 (134 Vouchers)'
          : `Mes: ${{voucherMonthsMap[mCode]}} (${{countMonth}} comprobantes)`;
      }}

      document.getElementById('vkpi-title-total').textContent = (mCode === 'all') ? 'Gasto Total 2026' : `Gasto ${{voucherMonthsMap[mCode]}}`;
      document.getElementById('vkpi-total').textContent = formatSoles(totalMonth);
      document.getElementById('vkpi-count').textContent = countMonth + ' Vouchers';
      document.getElementById('vkpi-total-sub').textContent = (mCode === 'all') ? 'Enero – Octubre (10 meses)' : `Total pagado en ${{voucherMonthsMap[mCode]}}`;

      document.getElementById('vkpi-admin').textContent = formatSoles(adminTotal);
      document.getElementById('vkpi-admin-sub').textContent = adminTotal > 0 ? (mCode === '08' || mCode === '10' ? 'Factor 1 / Factor Services' : (mCode < '05' ? 'SISACCE S.A.C.' : 'Administración')) : 'Sin facturación adm.';
      document.getElementById('vkpi-admin-pct').textContent = totalMonth > 0 ? ((adminTotal / totalMonth) * 100).toFixed(1) + '%' : '0%';

      document.getElementById('vkpi-andinos').textContent = formatSoles(andinosTotal);
      document.getElementById('vkpi-andinos-pct').textContent = totalMonth > 0 ? ((andinosTotal / totalMonth) * 100).toFixed(1) + '%' : '0%';

      document.getElementById('vkpi-servicios').textContent = formatSoles(serviciosTotal);
      document.getElementById('vkpi-servicios-pct').textContent = totalMonth > 0 ? ((serviciosTotal / totalMonth) * 100).toFixed(1) + '%' : '0%';

      // 5. Update Donut Chart & Legend
      updateVouchersDonut(visible, totalMonth, mCode);

      // 6. Update Table
      filterVouchersTable();
    }}

    // UPDATE VOUCHERS DONUT CHART & LEGEND
    function updateVouchersDonut(visibleItems, totalMonth, mCode) {{
      const catTotals = {{}};
      visibleItems.forEach(v => {{
        catTotals[v.category] = (catTotals[v.category] || 0) + v.amount;
      }});

      const sortedCats = Object.entries(catTotals).sort((a, b) => b[1] - a[1]);
      const labels = sortedCats.map(x => x[0]);
      const data = sortedCats.map(x => x[1]);

      const colors = [
        '#4f46e5', '#2563eb', '#06b6d4', '#10b981', '#f59e0b',
        '#ef4444', '#8b5cf6', '#ec4899', '#64748b', '#14b8a6', '#d97706'
      ];

      document.getElementById('vdonut-month-label').textContent = (mCode === 'all') ? 'Consolidado Total (10 meses)' : voucherMonthsMap[mCode];

      if (vouchersCatChart) {{
        vouchersCatChart.data.labels = labels;
        vouchersCatChart.data.datasets[0].data = data;
        vouchersCatChart.data.datasets[0].backgroundColor = colors.slice(0, labels.length);
        vouchersCatChart.update();
      }} else {{
        const ctx = document.getElementById('vouchersCatChart').getContext('2d');
        vouchersCatChart = new Chart(ctx, {{
          type: 'doughnut',
          data: {{
            labels: labels,
            datasets: [{{
              data: data,
              backgroundColor: colors.slice(0, labels.length),
              borderWidth: 2,
              borderColor: '#ffffff'
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{ display: false }},
              tooltip: {{
                callbacks: {{
                  label: (ctx) => {{
                    const val = ctx.parsed;
                    const pct = totalMonth > 0 ? ((val / totalMonth) * 100).toFixed(1) : 0;
                    return ` ${{ctx.label}}: ${{formatSoles(val)}} (${{pct}}%)`;
                  }}
                }}
              }}
            }},
            cutout: '68%'
          }}
        }});
      }}

      // Build HTML legend list
      const legEl = document.getElementById('vdonut-legend');
      legEl.innerHTML = '';
      if (sortedCats.length === 0) {{
        legEl.innerHTML = '<div class="text-slate-400 py-2 text-center">No hay gastos registrados en este mes</div>';
        return;
      }}

      sortedCats.forEach((sc, i) => {{
        const cat = sc[0];
        const val = sc[1];
        const pct = totalMonth > 0 ? ((val / totalMonth) * 100).toFixed(1) : '0';
        const color = colors[i % colors.length];

        const row = document.createElement('div');
        row.className = 'flex items-center justify-between text-xs py-0.5';
        row.innerHTML = `
          <div class="flex items-center gap-2 truncate pr-2">
            <span class="w-2.5 h-2.5 rounded-full flex-shrink-0" style="background-color: ${{color}}"></span>
            <span class="text-slate-700 font-medium truncate">${{cat}}</span>
          </div>
          <div class="text-right flex-shrink-0 font-mono">
            <span class="font-bold text-slate-900">${{formatSoles(val)}}</span>
            <span class="text-slate-400 text-[10px] ml-1">(${{pct}}%)</span>
          </div>
        `;
        legEl.appendChild(row);
      }});
    }}

    // FILTER VOUCHERS TABLE
    function filterVouchersTable() {{
      const query = (document.getElementById('voucher-search').value || '').toLowerCase();
      const mCode = currentSelectedVoucherMonth;

      const items = vouchersData.detalle_vouchers || [];
      const filtered = items.filter(v => {{
        const matchesMonth = (mCode === 'all') || (v.month === mCode);
        const matchesQuery = !query || 
          v.provider.toLowerCase().includes(query) ||
          v.category.toLowerCase().includes(query) ||
          v.file.toLowerCase().includes(query) ||
          (v.raw_str && v.raw_str.toLowerCase().includes(query));
        return matchesMonth && matchesQuery;
      }});

      const totalFiltered = filtered.reduce((sum, v) => sum + v.amount, 0);

      // Update Table Subtitle & Badges
      const countBadge = document.getElementById('vtable-badge-count');
      if (countBadge) countBadge.textContent = filtered.length + ' Vouchers';

      document.getElementById('vtable-showing-text').textContent = (mCode === 'all')
        ? `Mostrando ${{filtered.length}} de ${{items.length}} comprobantes (Ene–Oct 2026)`
        : `Mostrando ${{filtered.length}} comprobantes de ${{voucherMonthsMap[mCode]}}`;
      document.getElementById('vtable-sum-text').textContent = 'Total visible: ' + formatSoles(totalFiltered);

      const tbody = document.getElementById('vouchers-table-body');
      tbody.innerHTML = '';

      if (filtered.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="6" class="text-center py-8 text-slate-400">No se encontraron comprobantes para el filtro seleccionado</td></tr>`;
        return;
      }}

      filtered.forEach(v => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50/80 transition';
        tr.innerHTML = `
          <td class="py-2.5 px-4 font-mono text-slate-400 text-[11px]">${{v.id}}</td>
          <td class="py-2.5 px-3 font-medium text-slate-700 whitespace-nowrap">${{v.date}}</td>
          <td class="py-2.5 px-4 font-semibold text-slate-900">${{v.provider}}</td>
          <td class="py-2.5 px-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">${{v.category}}</span>
          </td>
          <td class="py-2.5 px-4 text-right font-mono font-bold text-slate-900">${{formatSoles(v.amount)}}</td>
          <td class="py-2.5 px-4 font-mono text-[11px] text-slate-500">${{v.file}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // RENDER VOUCHERS CHARTS
    function renderVouchersCharts() {{
      const ctxMonthly = document.getElementById('vouchersMonthlyChart').getContext('2d');
      const moLabels = Object.keys(vouchersData.por_mes);
      const moValues = Object.values(vouchersData.por_mes).map(x => x.total);

      vouchersMonthlyChart = new Chart(ctxMonthly, {{
        type: 'bar',
        data: {{
          labels: moLabels,
          datasets: [{{
            label: 'Gasto Mensual (S/)',
            data: moValues,
            backgroundColor: '#4f46e5',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          onClick: (evt, els) => {{
            if (els.length > 0) {{
              const idx = els[0].index;
              const moKeys = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'];
              selectVoucherMonth(moKeys[idx]);
            }}
          }},
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: (ctx) => ' Gasto: ' + formatSoles(ctx.parsed.y)
              }}
            }}
          }},
          scales: {{
            y: {{
              beginAtZero: true,
              ticks: {{
                callback: (val) => 'S/ ' + (val / 1000) + 'k'
              }}
            }}
          }}
        }}
      }});

      selectVoucherMonth('all');
    }}

    // RENDER BUDGET 2026 TABLE
    function renderBudgetTable() {{
      const tbody = document.getElementById('budget-table-body');
      tbody.innerHTML = '';
      budgetData.forEach((b, idx) => {{
        const isTotal = idx === budgetData.length - 1;
        const tr = document.createElement('tr');
        tr.className = isTotal ? 'bg-slate-50 font-bold border-t-2 border-slate-300' : 'hover:bg-slate-50/60';
        tr.innerHTML = `
          <td class="py-3 px-4 ${{isTotal ? 'text-slate-900 font-extrabold text-sm' : 'font-medium text-slate-800'}}">${{b.rubro}}</td>
          <td class="py-3 px-4 text-right font-mono ${{isTotal ? 'text-slate-900 font-extrabold' : 'text-slate-600'}}">${{formatSoles(b.real_2025)}}</td>
          <td class="py-3 px-4 text-right font-mono col-highlight ${{isTotal ? 'text-blue-900 font-extrabold' : 'text-blue-800'}}">${{formatSoles(b.pres_2026)}}</td>
          <td class="py-3 px-4 text-right font-mono font-semibold ${{b.dif < 0 ? 'text-emerald-600' : (b.dif > 0 ? 'text-rose-600' : 'text-slate-600')}}">${{b.dif > 0 ? '+' : ''}}${{formatSoles(b.dif)}}</td>
          <td class="py-3 px-3 text-center font-mono font-bold ${{b.dif < 0 ? 'text-emerald-700 bg-emerald-50' : (b.dif > 0 ? 'text-rose-700 bg-rose-50' : 'text-slate-600')}} rounded">${{b.pct}}</td>
          <td class="py-3 px-4 text-slate-500 text-[11px] leading-tight">${{b.obs}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // RENDER TIMELINE 2026
    function renderTimeline() {{
      const container = document.getElementById('timeline-container');
      container.innerHTML = '';
      eventsData.forEach(ev => {{
        const item = document.createElement('div');
        item.className = 'relative pl-6';
        item.innerHTML = `
          <div class="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-white border-4 border-indigo-600"></div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-indigo-600 font-mono">${{ev.fecha}}</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">${{ev.tipo}}</span>
          </div>
          <h4 class="text-sm font-bold text-slate-900 mt-1">${{ev.titulo}}</h4>
          <p class="text-xs text-slate-600 mt-1 leading-relaxed">${{ev.desc}}</p>
          <div class="mt-2 text-[11px] font-semibold text-slate-500">
            Documento: <span class="font-mono text-indigo-700">${{ev.doc}}</span>
          </div>
        `;
        container.appendChild(item);
      }});
    }}

    // RENDER 2025 CHARTS
    function render2025Charts() {{
      const ctxBar = document.getElementById('barChart2025').getContext('2d');
      const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Set', 'Oct', 'Nov', 'Dic'];
      const ingresos = meses.map(m => fin2025Data.ingresos_por_mes[m] || 0);
      const egresos = meses.map(m => fin2025Data.egresos_por_mes[m] || 0);

      barChart2025 = new Chart(ctxBar, {{
        type: 'bar',
        data: {{
          labels: meses,
          datasets: [
            {{ label: 'Ingresos (S/)', data: ingresos, backgroundColor: '#10b981', borderRadius: 4 }},
            {{ label: 'Egresos (S/)', data: egresos, backgroundColor: '#f43f5e', borderRadius: 4 }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            tooltip: {{ callbacks: {{ label: (ctx) => ` ${{ctx.dataset.label}}: ${{formatSoles(ctx.parsed.y)}}` }} }}
          }},
          scales: {{
            y: {{ ticks: {{ callback: (v) => 'S/ ' + (v / 1000) + 'k' }} }}
          }}
        }}
      }});

      const ctxDonut = document.getElementById('donutChart2025').getContext('2d');
      const cats = Object.keys(fin2025Data.estructura_gasto);
      const vals = Object.values(fin2025Data.estructura_gasto);
      const colors = ['#2563eb', '#f59e0b', '#06b6d4', '#10b981', '#64748b', '#8b5cf6', '#ec4899'];

      donutChart2025 = new Chart(ctxDonut, {{
        type: 'doughnut',
        data: {{
          labels: cats,
          datasets: [{{ data: vals, backgroundColor: colors, borderWidth: 2, borderColor: '#ffffff' }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          cutout: '65%'
        }}
      }});

      const leg = document.getElementById('donut2025-legend');
      leg.innerHTML = '';
      cats.forEach((cat, i) => {{
        leg.innerHTML += `
          <div class="flex items-center justify-between">
            <span class="flex items-center gap-1.5 truncate">
              <span class="w-2.5 h-2.5 rounded-full flex-shrink-0" style="background:${{colors[i % colors.length]}}"></span>
              <span class="truncate">${{cat}}</span>
            </span>
            <span class="font-mono font-bold">${{formatSoles(vals[i])}}</span>
          </div>
        `;
      }});
    }}

    // INITIALIZATION
    window.addEventListener('DOMContentLoaded', () => {{
      renderVouchersCharts();
      renderBudgetTable();
      renderTimeline();
    }});
  </script>

</body>
</html>
'''

output_path = r"D:\Canales\Morar\morar-dashboard\index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated successfully: {output_path} ({len(html_content)} bytes)")
