// Example data from database
const deskActivit = {
    up: [0.5], // Hours standing up
    down: [1, 1, 1, 1, 1], // Hours sitting down
  };
  
  // Chart.js setup
  const ctx = document.getElementById("activity-chart").getContext("2d");
  const chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["8 AM", "10 AM", "12 PM", "2 PM", "4 PM"],
      datasets: [
        {
          label: "Standing (Up)",
          data: deskActivit.up,
          backgroundColor: "rgba(75, 192, 192, 0.6)",
        },
        {
          label: "Sitting (Down)",
          data: deskActivit.down,
          backgroundColor: "rgba(255, 99, 132, 0.6)",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
      },
    },
  });
  
  // Health tips generation
  
  document.getElementById("save-btn").addEventListener("click", () => {
    const age = document.getElementById("age").value;
    const tips = generateHealthTips(age, deskActivit);
    document.getElementById("tips").innerText = tips;
  }); 
  
  
  function generateHealthTips(age, activity) {
    let standingHours = activity.up.length;
    let sittingHours = activity.down.length;
  
    if (standingHours >= 2) {
      return `Great job maintaining your activity! Aim for 2-4 hours standing daily.`;
    } else {
      return `Consider standing more often during work, for at least 2 hours a day.`;
    }
  }
  