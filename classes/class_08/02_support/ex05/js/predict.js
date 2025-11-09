function indexOfMax(arr) {
  if (arr.length === 0) {
      return -1;
  }

  var max = arr[0];
  var maxIndex = 0;

  for (var i = 1; i < arr.length; i++) {
      if (arr[i] > max) {
          maxIndex = i;
          max = arr[i];
      }
  }

  return maxIndex;
}

class TSM {
  constructor(w, h, min, max) {
    this.w = w;
    this.h = h;
    this.min = min;
    this.max = max;
    this.ts = 0;
    this.probs = [];
    this.previous_value = null;
    this.total = 0;
    for (let i = 0; i < w; i++) {
      this.probs[i] = [];
      for (let j = 0; j < h; j++) {
        this.probs[i][j] = []
        for (let k = 0; k < h; k++) {
          this.probs[i][j][k] = 0;
        }
      }
    }
  }

  get width() {
    return this.w;
  }

  get height() {
    return this.h;
  }

  value_bin(value) {
    let range = this.max - this.min;
    let inc = range / this.h;
    let idx = 0;

    for (let i = this.min; (i + inc) < value; i += inc) {
      ++idx;
    }

    return idx;
  }

  average_value(k) {
    let range = this.max - this.min;
    let inc = range / this.h;
    let rv = this.min;

    for (let i = 0; i < k; i += 1) {
      rv += inc;
    }

    return rv + (inc / 2.0);
  }

  learn(value) {
    // Update the max and min variables
    if (value > this.max) {
      this.max = value;
    } else if (value < this.min) {
      this.min = value;
    }

    // compute right bin
    let idx = this.value_bin(value);
    if (this.previous_value != null) {
      this.probs[this.ts][this.previous_value][idx]++;
      //console.log('learn v2 = '+this.probs[this.ts][this.previous_value][idx]);
      this.ts = (this.ts + 1) % this.w;
      this.total++;
    }

    // update time for next point
    this.previous_value = idx;
  }

  predict() {
    let i = this.ts;
    let j = this.previous_value;
    let k = indexOfMax(this.probs[i][j]); //.reduce((iMax, x, i, this.probs[i][j]) => x > this.probs[i][j][iMax] ? i : iMax, 0);
    return this.average_value(k);
  }

  toString() {
    let str = '';
    // Header
    str += 'W = ' + this.w + ' H = ' + this.h + ' Min = ' + this.min + ' Max = ' + this.max + '\n';
    // Probs
    for (let i = 0; i < this.w; i++) {
      for (let j = 0; j < this.h; j++) {
        for (let k = 0; k < this.h; k++) {
          let v = 0;
          if (this.total > 0) {
            v = this.probs[i][j][k] / this.total;
          }
          str += 'Probs[' + i + '][' + j + '][' + k + '] = ' + v.toFixed(2) + '\n';
        }
      }
    }

    return str;
  }
}

function setupHighcharts(w, tsm) {
  Highcharts.setOptions({ global: { useUTC: false } });
  let today = new Date();
  let chart = Highcharts.chart('container', {
    chart: {
      type: 'spline'
    },
    title: {
      text: 'Humidity'
    },
    xAxis: {
      type: 'datetime',
      tickPixelInterval: 150
    },
    yAxis: {
        min: 0,
        max: 100,
        labels: {
          format: '{value}%',
          style: {
            color: '#7cb5ec'
          }
        },
        title: {
          text: 'Humidity',
          style: {
            color: '#7cb5ec'
          }
        }
      },
    legend: {
      enabled: false
    },
    exporting: {
      enabled: false
    },
    series: [
      {
        name: 'Humidity',
        type: 'spline',
        yAxis: 0,
        color: '#7cb5ec',
        data: (function () {
          let data = [], time = today.getTime(), i;
          for (i = 0; i < w; i += 1) {
            data.push({ x: (time - ((w - i) * 1000)), y: 50 });
          }
          return data;
        }())
      }]
  });

  let predicted = Highcharts.chart('container_predicted', {
    chart: {
      type: 'spline'
    },
    title: {
      text: 'Predicted Humidity'
    },
    xAxis: {
      type: 'datetime',
      tickPixelInterval: 150
    },
    yAxis: {
        min: 0,
        max: 100,
        labels: {
          format: '{value}%',
          style: {
            color: '#7cb5ec'
          }
        },
        title: {
          text: 'Humidity',
          style: {
            color: '#7cb5ec'
          }
        }
      },
    legend: {
      enabled: false
    },
    exporting: {
      enabled: false
    },
    series: [
      {
        name: 'Humidity',
        type: 'spline',
        yAxis: 0,
        color: '#7cb5ec',
        data: (function () {
          
          let data = [], time = today.getTime(), i;
          for (i = 0; i < w; i += 1) {
            data.push({ x: (time - ((w - i) * 1000)), y: 50 });
          }
          return data;
        }())
      }]
  });

  for (let i = 0; i < w; i += 1) {
    tsm.learn(50);
  }

  predicted.series[0].addPoint([today.getTime(), tsm.predict()], true, true)
  return [chart, predicted];
}

function setupWS(charts, tsm) {
  let mqtt = new Paho.MQTT.Client('localhost', 9001, 'clientjs');
      
  // set callback handlers
  mqtt.onConnectionLost = onConnectionLost;
  mqtt.onMessageArrived = onMessageArrived;
      
  let options = {timeout:3, onSuccess: onConnect};
  mqtt.connect(options);
    
  function onConnect(){
    console.log('Connected...');
    mqtt.subscribe('esp/hum');
  }

    // called when the client loses its connection
    function onConnectionLost(responseObject) {
      if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost: "+responseObject.errorMessage);
      }
    }

    // called when a message arrives
    function onMessageArrived(message) {
      let today = new Date();
      let time = today.getTime();
    
      console.log("onMessageArrived("+message.destinationName+"):"+message.payloadString);
      humidity = parseFloat(message.payloadString);

      charts[0].series[0].addPoint([time, humidity], true, true);
      tsm.learn(humidity);
      charts[1].series[0].addPoint([time, tsm.predict()], true, true);
    }
}

function checkHC(tsm) {
  if (typeof Highcharts == 'undefined') {
    setTimeout(function () { checkHC(tsm) }, 1000);
  } else {
    setupWS(setupHighcharts(10, tsm), tsm);
  }
}

function setup() {
  checkHC(new TSM(3, 20, 0, 100));
}
