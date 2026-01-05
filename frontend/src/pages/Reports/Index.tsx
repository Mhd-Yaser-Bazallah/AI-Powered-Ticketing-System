import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";
import toast from "react-hot-toast";
import { APIInstance } from "../../services/APIs/Reports";
import { Users, CheckCircle2, AlertTriangle, BarChart, Download } from "lucide-react";

const Dashboard = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchReports = async () => {
    try {
      const company_id = sessionStorage.getItem("company_id");
      if (!company_id) {
        console.error("No company ID found in sessionStorage");
        return;
      }

      setLoading(true);
      const response = await APIInstance.Get(company_id);
      setData(response);
    } catch (error) {
      console.error("Error fetching reports:", error);
      toast.error("Failed to fetch data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  if (loading || !data) return <DashboardSkeleton />;


 const downloadExcel = async (type: "status" | "priority" | "teams" | "companies") => {
  try {
    let response: any;

    switch (type) {
      case "status":
        response = await APIInstance.GetReportingTicketsStatus();
        break;
      case "priority":
        response = await APIInstance.GetReportingTicketsPriority();
        break;
      case "teams":
        response = await APIInstance.GetReportingTeamsPerformance();
        break;
      case "companies":
        response = await APIInstance.GetReportingCompaniesTickets();
        break;
    }

    if (!response || !response.download_url) {
      toast.success("file downloaded");
      return;
    }

    const baseUrl = import.meta.env.VITE_BASEURL 
    const fullUrl = response?.data?.download_url.startsWith("http")
      ? response?.data?.download_url
      : `${baseUrl}${response?.data?.download_url}`;

    const a = document.createElement("a");
    a.href = fullUrl;
    a.download = `${type}-report.xlsx`; 
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    toast.success("File downloaded successfully 🎉");
  } catch (error) {
    console.error("❌ Download error:", error);
    toast.error("Failed to download file");
  }
};

  

  const ticketsByStatusOption = {
    tooltip: { trigger: "item" },
    legend: {
      bottom: 0,
      textStyle: { color: "var(--color-text-main)", fontSize: 13 },
      itemWidth: 16,
      itemHeight: 10,
    },
    series: [
      {
        name: "Tickets by Status",
        type: "pie",
        radius: ["45%", "70%"],
        label: {
          show: true,
          position: "center",
          fontSize: 18,
          fontWeight: "bold",
          formatter: `{d}%`,
        },
        emphasis: { label: { show: true, fontSize: 22, fontWeight: "bold" } },
        labelLine: { show: false },
        data: data?.data?.tickets_by_status?.length
          ? data?.data?.tickets_by_status.map((item: any, i: number) => ({
              value: item.count || 0,
              name: item.status || "Unknown",
              itemStyle: {
                color: ["#22c55e", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6"][i % 7],
              },
            }))
          : [],
      },
    ],
  };
  
  const assignedVsUnassignedOption = {
    tooltip: { trigger: "item" },
    legend: {
      bottom: 0,
      textStyle: { color: "var(--color-text-main)", fontSize: 13 },
      itemWidth: 16,
      itemHeight: 10,
    },
    series: [
      {
        name: "Assignment Status",
        type: "pie",
        radius: ["45%", "70%"],
        avoidLabelOverlap: false,
        label: {
          show: true,
          position: "center",
          fontSize: 18,
          fontWeight: "bold",
          formatter: `{d}%`,
        },
        emphasis: { label: { show: true, fontSize: 22, fontWeight: "bold" } },
        labelLine: { show: false },
        data: [
          {
            value: data?.data?.assigned_vs_unassigned?.assigned || 0,
            name: "Assigned",
            itemStyle: { color: "#10b981" },
          },
          {
            value: data?.data?.assigned_vs_unassigned?.unassigned || 0,
            name: "Unassigned",
            itemStyle: { color: "#f87171" },
          },
        ],
      },
    ],
  };
  
  const ticketsByTeamOption = {
    tooltip: { trigger: "axis" },
    xAxis: {
      type: "category",
      data: data?.data?.tickets_by_team?.length
        ? data?.data?.tickets_by_team?.map((t: any) => t.Team__category || "Unknown")
        : [],
      axisLabel: { rotate: 30, color: "var(--color-text-main)" },
    },
    yAxis: { type: "value", axisLabel: { color: "var(--color-text-main)" } },
    series: [
      {
        data: data?.data?.tickets_by_team?.length
          ? data?.data?.tickets_by_team.map((t: any) => t.count || 0)
          : [],
        type: "bar",
        itemStyle: {
          borderRadius: [8, 8, 0, 0],
        },
      },
    ],
  };
  

  return (
    <div className="min-h-screen space-y-10 bg-mainBg p-6">
      <div>
        <h1 className="text-3xl font-bold text-textMain">🎫 Tickets Dashboard</h1>
        <p className="mt-1 text-gray-400">Statistics overview for your support system</p>
      </div>

      <div className="flex flex-wrap gap-4 mb-6">
        <button
          onClick={() => downloadExcel("status")}
          className="flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        >
          <Download className="w-5 h-5 mr-2" /> Download Status
        </button>
        <button
          onClick={() => downloadExcel("priority")}
          className="flex items-center px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition"
        >
          <Download className="w-5 h-5 mr-2" /> Download Priority
        </button>
        <button
          onClick={() => downloadExcel("teams")}
          className="flex items-center px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
        >
          <Download className="w-5 h-5 mr-2" /> Download Teams
        </button>
        <button
          onClick={() => downloadExcel("companies")}
          className="flex items-center px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition"
        >
          <Download className="w-5 h-5 mr-2" /> Download Companies
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        <CardGradient
          icon={<BarChart className="w-10 h-10 mb-2" />}
          title="Total Tickets"
          value={data?.data?.total_tickets}
          gradient="from-blue-500 to-blue-700"
        />
        <CardGradient
          icon={<Users className="w-10 h-10 mb-2" />}
          title="Teams"
          value={data?.data?.tickets_by_team?.length}
          gradient="from-indigo-500 to-indigo-400"
        />
        <CardGradient
          icon={<CheckCircle2 className="w-10 h-10 mb-2" />}
          title="Assigned"
          value={data?.data?.assigned_vs_unassigned?.assigned}
          gradient="from-green-400 to-green-600"
        />
        <CardGradient
          icon={<AlertTriangle className="w-10 h-10 mb-2" />}
          title="Unassigned"
          value={data?.data?.assigned_vs_unassigned?.unassigned}
          gradient="from-pink-400 to-pink-600"
        />
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <ChartCard title="Tickets by Status" option={ticketsByStatusOption} />
        <ChartCard title="Assigned vs Unassigned" option={assignedVsUnassignedOption} />
        <ChartCard title="Tickets by Team" option={ticketsByTeamOption} />
      </div>
    </div>
  );
};

const Counter = ({ value, duration = 600 }: { value: number; duration?: number }) => {
  const [count, setCount] = useState(0);
  useEffect(() => {
    let start = 0;
    const increment = value / (duration / 16);
    const interval = setInterval(() => {
      start += increment;
      if (start >= value) {
        setCount(value);
        clearInterval(interval);
      } else {
        setCount(Math.floor(start));
      }
    }, 16);
    return () => clearInterval(interval);
  }, [value, duration]);
  return <span>{count}</span>;
};

const CardGradient = ({ icon, title, value, gradient }: any) => (
  <div
    className={`relative bg-gradient-to-br ${gradient} rounded-3xl shadow-2xl p-6 text-white overflow-hidden transform transition hover:scale-105`}
  >
    <div className="absolute w-24 h-24 rounded-full -top-6 -right-6 bg-white/20 animate-pulse"></div>
    <div className="absolute w-24 h-24 rounded-full -bottom-6 -left-6 bg-white/20 animate-pulse"></div>
    <div className="flex flex-col items-center">
      {icon}
      <h2 className="text-lg font-semibold text-center">{title}</h2>
      <Counter value={value} />
    </div>
  </div>
);

const ChartCard = ({ title, option }: any) => (
  <div className="p-6 transition border shadow-xl bg-tableBg rounded-2xl border-border hover:shadow-2xl">
    <h3 className="mb-4 text-lg font-semibold text-textMain">{title}</h3>
    <ReactECharts option={option} style={{ height: 300 }} />
  </div>
);

const DashboardSkeleton = () => (
  <div className="min-h-screen p-8 space-y-10 bg-mainBg">
    <div className="space-y-2">
      <div className="w-64 h-8 bg-gray-300 rounded animate-pulse"></div>
      <div className="h-4 bg-gray-200 rounded w-96 animate-pulse"></div>
    </div>
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      {[...Array(4)]?.map((_, i) => (
        <div key={i} className="h-40 bg-gray-300 rounded-3xl animate-pulse"></div>
      ))}
    </div>
    <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
      {[...Array(3)]?.map((_, i) => (
        <div key={i} className="bg-gray-300 h-80 rounded-2xl animate-pulse"></div>
      ))}
    </div>
  </div>
);

export default Dashboard;
