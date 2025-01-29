import React, { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

const GaugeChart = ({ label, value, color }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext("2d");
    chartInstance.current = new Chart(ctx, {
      type: "doughnut",
      data: {
        datasets: [
          {
            data: [value, 100 - value],
            backgroundColor: [color, "#EAEAEA"],
            borderWidth: 0,
            cutout: "80%",
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          tooltip: { enabled: false },
          legend: { display: false },
        },
        circumference: 180,
        rotation: 270,
      },
    });

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [value, color]);

  return (
    <div className="gauge-chart">
      <canvas ref={chartRef} width="120" height="120"></canvas>
      <div className="gauge-label">
        <p>{value}%</p>
        <span>{label}</span>
      </div>
    </div>
  );
};

export default GaugeChart;
