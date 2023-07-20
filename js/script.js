/**
 * @author Andrew Kim
 * @version 1.0.0
 * @description knob functionality for RiverSentinel Metrics
*/


// default knob values
const lineWidth = 160;
const startAngle = 0.75 * Math.PI;
const endAngle = 0.25 * Math.PI;
const defaultColor = "#d3d3d3";


// knob GUI manager
class Knob {
    constructor(pName, pColor, pValue, pMin, pMax) {
        // knob values
        this.color = pColor;
        this.min = pMin;
        this.max = pMax;

        // canvas values
        this.canvas = document.getElementById(pName);
        this.width = this.canvas.offsetWidth * 8;
        this.canvas.width = this.width;
        this.canvas.height = this.width;
        
        // ctx values
        this.ctx = this.canvas.getContext("2d");
        this.radius = this.width / 3;
        this.center = this.width / 2;

        // draw knob
        this.draw(pValue);
    }

    getValueAngle(value) {
        let proportion = value / this.max;
        let angleProportion = 1.5 * Math.PI * proportion;
        let valueAngle = startAngle + angleProportion;
        return valueAngle;
    }

    draw(value) {
        // clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // draw knob backdrop
        this.ctx.beginPath();
        this.ctx.strokeStyle = defaultColor;
        this.ctx.lineWidth = lineWidth;
        this.ctx.arc(this.center, this.center, this.radius, startAngle, endAngle);
        this.ctx.stroke();

        // draw primary knob
        this.ctx.beginPath();
        this.ctx.strokeStyle = this.color;
        this.ctx.arc(this.center, this.center, this.radius, startAngle, this.getValueAngle(value));
        this.ctx.stroke();
    }
}



// general metric manager
class Metric {
    constructor(pName, pUnit, pColor, pValue, pMin, pMax) {
        this.name = pName;
        this.unit = pUnit;
        this.value = pValue;
        this.min = pMin;
        this.max = pMax;
        this.knob = new Knob(pName, pColor, pValue, pMin, pMax);

        this.knobValue = document.getElementById(this.name + "-value");
        this.message = document.getElementById(this.name + "-message");

        this.updateValue(pValue);
    }

    updateValue(newValue) {
        if(newValue >= this.min && newValue <= this.max) {
            this.value = newValue;
            this.knob.draw(newValue);
            this.knobValue.innerHTML = newValue + this.unit;
            this.message.innerHTML = "probe working";
        }else {
            this.knob.draw(this.min);
            this.knobValue.innerHTML = "N/A";
            this.message.innerHTML = "probe not working";
        }

    }
}


let pH = new Metric("pH", "", "#03045e", 7, 0, 14);
let tds = new Metric("tds", "PPM", "#023e8a", 0, 0, 500);
let turbidity = new Metric("turbidity", "NTU", "#0077b6", 0, 0, 3000);
let temperature = new Metric("temperature", "°", "#0096c7", 7, 0, 100);

function updateReadings() {
    fetch('/api/gpio_values')
        .then(response => response.json())
        .then(data => {
            const readings = data.readings_dict;
            pH.updateValue(readings[0]);
            tds.updateValue(readings[1]);
            turbidity.updateValue(readings[2])
            temperature.updateValue(readings[3])
        })
        .catch(error => console.error("Error fetching GPIO readings", error))
}

updateReadings();

setInterval(updateReadings, 1000);