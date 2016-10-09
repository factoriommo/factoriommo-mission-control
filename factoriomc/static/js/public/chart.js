$(function() {

    Chart.defaults.global.elements.line.borderWidth = 1;
    Chart.defaults.global.legend.position = 'right';

    // var PlayersChart = new Chart($("#playersChart"), {
    //     type: 'line',
    //     data: {
    //         // labels: ["Science"],
    //         datasets: [{
    //             label: "Trees",
    //             borderColor: "#00cc00",
    //             backgroundColor: "rgba(0,0,0,0)",
    //             data: []
    //         }, {
    //             label: "Aliens",
    //             borderColor: "#9F00FF",
    //             backgroundColor: "rgba(0,0,0,0)",
    //             data: []
    //         }, {
    //             label: "Differential",
    //             borderColor: "orange",
    //             backgroundColor: "rgba(0,0,0,0)",
    //             data: []
    //         }]
    //     },
    //     options: {
    //         scales: {
    //             xAxes: [{
    //                 type: 'linear',
    //                 position: 'bottom'
    //             }]
    //         }
    //     }
    // });

    /**
     * Controller
     */

    var ChartController = function() {
        this._charts = {}
        this._charts.science = {};
        // this._charts.players = this.getChartModel(3, PlayersChart);
    }

    ChartController.prototype.getChartModel = function(length, chart) {
        var model = {
            data: [],
            chart: chart,
            startTime: 0
        }

        for (var i = 0; i < length; i++) {
            model.data.push([]);
        }

        return model;
    }

    ChartController.prototype.updateAllChart = function(name, server_name) {
      var chart = this._charts[name][server_name];
        for (var i = 0; i < chart.data.length; i++) {
            this.updateChart(name, i, server_name)
        }
    }

    ChartController.prototype.updateChart = function(name, type, server_name) {
        var controller = this;
        var obj = this._charts[name][server_name],
            points = obj.data[type],
            chart = obj.chart;


        points.forEach(function(p) {
            if (p.timestamp < obj.startTime || obj.startTime == 0) {
                obj.startTime = p.timestamp;
                controller.updateAllChart(name, server_name);
                return
            }
        })

        points = _.map(points, function(p) {
            return {
                x: (p.timestamp - obj.startTime) / 60,
                y: p.value
            }
        });
        points.sort(function(a, b) {
            return a.x - b.x
        })
        chart.data.datasets[type].data = points;

        chart.update()
    }

    ChartController.prototype.buildPlayersData = function(data, team) {
        var controller = this,
            players = controller._charts.players[team],
            insert_index = -1,
            join_sign = data.type == 'player_joined' ? 1 : -1;

        // Find point to start working on
        for (var i = players.length - 1; i >= 0 && insert_index < 0; i--) {
            if (players[i].timestamp < data.timestamp) {
                insert_index = i + 1;
            }
        }

        for (var i = insert_index; i < players.length; i++) {
            players[i] += join_sign
        }

        // TODO push data point @ insert_index
        // TODO add differential entry

        return players;
    }

    ChartController.prototype.createScienceChart = function(server_name){
      var chart_canvas = $('<canvas class="server_'+server_name+'" width="400" height="200"></canvas>')
      $('#scienceCharts').append(chart_canvas)

      var ScienceChart = new Chart(chart_canvas, {
          type: 'line',
          data: {
              // labels: ["Science"],
              datasets: [{
                  label: "Red Science",
                  borderColor: "#FF0000",
                  backgroundColor: "rgba(0,0,0,0)",
                  borderCapStyle: 'butt',
                  data: []
              }, {
                  label: "Green Science",
                  borderColor: "#00cc00",
                  backgroundColor: "rgba(0,0,0,0)",
                  data: []
              }, {
                  label: "Blue Science",
                  borderColor: "#4997D0",
                  backgroundColor: "rgba(0,0,0,0)",
                  data: []
              }, {
                  label: "Alien Science",
                  borderColor: "#9F00FF",
                  backgroundColor: "rgba(0,0,0,0)",
                  data: []
              }]
          },
          options: {
              scales: {
                  xAxes: [{
                      type: 'linear',
                      position: 'bottom',
                      scaleLabel: {
                        display: true,
                        labelString: "minutes"
                      }
                  }]
              },
              title: {
                display: true,
                text: server_name,
                fullWidth: false,
                fontSize: 18
              },
          },
      });

      this._charts.science[server_name] = this.getChartModel(4, ScienceChart);
    }

    ChartController.prototype.receiveMessage = function(data) {
        var controller = this;
        switch (true) {
            case /science-pack/.test(data.type):
                if(typeof this._charts.science[data.server] !== 'object'){
                  controller.createScienceChart(data.server)
                }

                // TODO: discern between production/consumption
                if (data.namespace === 'consumption') {
                    var science_type = data.type.slice(-1);
                    if (!parseInt(science_type)) {
                        if (/alien/.test(data.type.slice(0, 5))) {
                            science_type = 4;
                        } else {
                            break;
                        }
                    }
                    this._charts.science[data.server].data[science_type - 1].push(data.data);
                    this.updateChart('science', science_type - 1, data.server);
                }
                break;
            case /players/.test(data.type):
                var team = 'team'
                    // TODO: Validate teams before moving on && event type (i.e player_joined/player_left)
                controller._charts.players.data[team] = controller.buildPlayersData(data.data, team)
                    // TODO build differential
                this.updateChart('players', team)

            default:

        }
    }

    var CC = new ChartController();

    /**
     * WebSocket listener
     */

    var url = WEBSOCKET_BASEURL + "/public/";
    var ws = new WebSocket(url);
    ws.onmessage = function(e) {
        var data = JSON.parse(e.data);

        CC.receiveMessage(data);
        // console.log(e);
    }

});
