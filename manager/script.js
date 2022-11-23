google.charts.load("current", { packages: ["corechart", "line"] });
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {
  var data = new google.visualization.DataTable();
  data.addColumn("number", "X");
  data.addColumn("number", "NoW");

  data.addRows([
    [0, 0],
    [1, 10],
    [2, 23],
    [3, 17],
    [4, 18],
    [5, 9],
    [6, 11],
    [7, 27],
    [8, 13],
    [9, 10],
    [10, 22],
    [11, 25],
    [12, 30],
    [13, 20],
    [14, 22],
    [15, 27],
    [16, 24],
    [17, 28],
    [18, 22],
    [19, 24],
    [20, 22],
    [21, 25],
    [22, 26],
    [23, 27],
    [24, 20],
    [25, 20],
    [26, 22],
    [27, 21],
    [28, 29],
    [29, 23],
    [30, 25],
  ]);

  var options = {
    series: {
      0: { color: "#e2431e" },
    },
    // hAxis: {
    //   title: "Time",
    // },
    width: 700,
    height: 500,
    // vAxis: {
    //   title: "Popularity",
    // },
  };

  var chart = new google.visualization.LineChart(
    document.getElementById("Workers-number")
  );

  chart.draw(data, options);
}
google.charts.load("current", { packages: ["corechart", "line"] });
google.charts.setOnLoadCallback(drawBasic2);
function drawBasic2() {
  var data = new google.visualization.DataTable();
  data.addColumn("number", "X");
  data.addColumn("number", "NoI");

  data.addRows([
    [0, 0],
    [1, 1],
    [2, 2],
    [3, 3],
    [4, 4],
    [5, 5],
    [6, 6],
    [7, 7],
    [8, 8],
    [9, 9],
    [10, 10],
    [11, 11],
    [12, 12],
    [13, 13],
    [14, 14],
    [15, 18],
    [16, 16],
    [17, 17],
    [18, 18],
    [19, 11],
    [20, 20],
    [21, 21],
    [22, 22],
    [23, 30],
    [24, 24],
    [25, 25],
    [26, 26],
    [27, 27],
    [28, 28],
    [29, 29],
    [30, 30],
  ]);

  var options = {
    series: {
      0: { color: "#e7711b" },
    },

    // hAxis: {
    //   title: "Time",
    // },
    width: 700,
    height: 500,
    // vAxis: {
    //   title: "Popularity",
    // },
  };

  var chart = new google.visualization.LineChart(
    document.getElementById("items-number")
  );

  chart.draw(data, options);
}

google.charts.load("current", { packages: ["corechart", "line"] });
google.charts.setOnLoadCallback(drawBasic3);
function drawBasic3() {
  var data = new google.visualization.DataTable();
  data.addColumn("number", "X");
  data.addColumn("number", "SoI");

  data.addRows([
    [0, 0],
    [1, 1],
    [2, 2],
    [3, 3],
    [4, 4],
    [5, 8],
    [6, 6],
    [7, 7],
    [8, 8],
    [9, 9],
    [10, 10],
    [11, 11],
    [12, 12],
    [13, 13],
    [14, 14],
    [15, 8],
    [16, 16],
    [17, 17],
    [18, 18],
    [19, 11],
    [20, 20],
    [21, 21],
    [22, 22],
    [23, 25],
    [24, 24],
    [25, 25],
    [26, 26],
    [27, 27],
    [28, 28],
    [29, 29],
    [30, 30],
  ]);

  var options = {
    series: {
      0: { color: "#f1ca3a" },
    },

    // hAxis: {
    //   title: "Time",
    // },
    width: 700,
    height: 500,

    // vAxis: {
    //   title: "Popularity",
    // },
  };

  var chart = new google.visualization.LineChart(
    document.getElementById("items-size")
  );

  chart.draw(data, options);
}

google.charts.load("current", { packages: ["corechart", "line"] });
google.charts.setOnLoadCallback(drawBasic4);
function drawBasic4() {
  var data = new google.visualization.DataTable();
  data.addColumn("number", "X");
  data.addColumn("number", "RPM");

  data.addRows([
    [0, 0],
    [1, 1],
    [2, 2],
    [3, 3],
    [4, 4],
    [5, 8],
    [6, 6],
    [7, 7],
    [8, 8],
    [9, 9],
    [10, 10],
    [11, 11],
    [12, 9],
    [13, 13],
    [14, 12],
    [15, 8],
    [16, 19],
    [17, 17],
    [18, 20],
    [19, 11],
    [20, 20],
    [21, 21],
    [22, 22],
    [23, 25],
    [24, 24],
    [25, 25],
    [26, 26],
    [27, 27],
    [28, 28],
    [29, 29],
    [30, 30],
  ]);

  var options = {
    // hAxis: {
    //   title: "Time",
    // },
    width: 700,
    height: 500,

    // vAxis: {
    //   title: "Popularity",
    // },
  };

  var chart = new google.visualization.LineChart(
    document.getElementById("requests-number")
  );

  chart.draw(data, options);
}

// Start Miss And Hit Rate
google.charts.load("current", { packages: ["corechart", "line"] });
google.charts.setOnLoadCallback(drawLogScales);

function drawLogScales() {
  var data = new google.visualization.DataTable();
  data.addColumn("number", "X");
  data.addColumn("number", "Miss Rate");
  data.addColumn("number", "Hit Rate");

  data.addRows([
    [0, 0, 0],
    [1, 10, 5],
    [2, 23, 15],
    [3, 17, 9],
    [4, 18, 10],
    [5, 9, 5],
    [6, 11, 3],
    [7, 27, 19],
    [8, 33, 25],
    [9, 40, 32],
    [10, 32, 24],
    [11, 35, 27],
    [12, 30, 22],
    [13, 40, 32],
    [14, 42, 34],
    [15, 47, 39],
    [16, 44, 36],
    [17, 48, 40],
    [18, 52, 44],
    [19, 54, 46],
    [20, 42, 34],
    [21, 55, 47],
    [22, 56, 48],
    [23, 57, 49],
    [24, 60, 52],
    [25, 50, 42],
    [26, 52, 44],
    [27, 51, 43],
    [28, 49, 41],
    [29, 53, 45],
    [30, 55, 47],
  ]);

  var options = {
    hAxis: {
      title: "Time",
      logScale: false,
    },
    // width: 900,
    height: 500,
    vAxis: {
      //   title: "Popularity",
      logScale: false,
    },
    colors: ["#a52714", "#097138"],
  };

  var chart = new google.visualization.LineChart(
    document.getElementById("miss-hit")
  );
  chart.draw(data, options);
}
// End Miss And Hit Rate
