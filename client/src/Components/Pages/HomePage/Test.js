
import React from 'react';
import ReactApexChart from 'react-apexcharts';
//import Chart from 'react-apexcharts'
 // Define a method to simulate data, this is the method of ApexCharts official website
function generateDayWiseTimeSeries(baseval, count, yrange) { 
    	var i = 0;
    	var series = [];
    	while (i < count) {
    		var x = baseval;
    		var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

    		series.push([x, y]);
    		baseval += 86400000;
    		i++;
    	}
    	return series;
    }

class ApexChart extends React.Component {
        constructor(props) {
          super(props);

          this.state = {
          
            series: [
              {
                name: '$APPL',
                data: generateDayWiseTimeSeries(new Date('28 jul 2021 GMT').getTime(), 20, {
                  min: 10,
                  max: 60
                })
              },
              {
                name: '$NEPL',
                data: generateDayWiseTimeSeries(new Date('28 jul 2021 GMT').getTime(), 20, {
                  min: 10,
                  max: 90
                })
              },
              {
                name: '$APED',
                data: generateDayWiseTimeSeries(new Date('28 jul 2021 GMT').getTime(), 20, {
                  min: 25,
                  max: 70
                })
              },
              {
                name: '$OPEK',
                data: generateDayWiseTimeSeries(new Date('28 jul 2021 GMT').getTime(), 20, {
                  min: 10,
                  max: 250
                })
              }
            ],
            options: {
              chart: {
                type: 'area',
                width: '100%',
                height: '100%',
                stacked: true,
                events: {
                  selection: function (chart, e) {
                    console.log(new Date(e.xaxis.min))
                  }
                },
              },
              colors: ['#ffb3ba', '#baffc9', '#bae1ff', 	"#ffdfba", "#f5e1fd"],
              dataLabels: {
                enabled: false
              },
              stroke: {
                curve: 'smooth'
              },
              fill: {
                type: 'gradient',
                gradient: {
                  opacityFrom: 0.6,
                  opacityTo: 0.8,
                }
              },
              legend: {
                position: 'right',
                horizontalAlign: 'center'
              },
              xaxis: {
                type: 'datetime'
              },
              yaxis: {
                labels: {
                  formatter: function (value) { return "$" + value;}
                }
              },
            },
          
          
          };
        } 

      

        render() {
          return (
            <div id="chart">
              <ReactApexChart options={this.state.options} series={this.state.series} type="area" height={400} />
            </div>

          );
        }
      }

      //const domContainer = document.querySelector('#app');
      //ReactDOM.render(React.createElement(ApexChart), domContainer);
    export default ApexChart;