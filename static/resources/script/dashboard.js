(function() {
var YEAR = new Date().getFullYear();

var CO2_EMISSIONS_PER_MILLISECOND = 567000000 / (365 * 24 * 60 * 60 * 1000);
var EQUIVALENCE_FLIGHT_PARIS_NY = 1.7;

var ELECTRICITY_CONSUMPTION_PER_MILLISECOND = 1183000000 / (365 * 24 * 60 * 60 * 1000);
var EQUIVALENCE_FRENCH_PERSON = 2223;

var SMARTPHONE_SALES_PER_MILLISECOND = 1500000000 / (365 * 24 * 60 * 60 * 1000);
var WATER_PER_SMARTPHONE = 900;

var PC_SALES_PER_MILLISECOND = 259500000 / (365 * 24 * 60 * 60 * 1000);
var WATER_PER_PC = 1500;

var E_WASTE_PER_MILLISECOND = 59000000 / (365 * 24 * 60 * 60 * 1000);
var E_WASTE_RECYCLING = 0.174;

var COPPER_PER_MILLISECOND = 0.2 * 5180000 / (365 * 24 * 60 * 60 * 1000);
var ORE_GRADE = 0.006;

var BITCOIN_ELEC_PER_MILLISECOND = 160000000 / (365 * 24 * 60 * 60 * 1000);
var EQUIVALENCE_VISA = 740000000000 / 3600;

var GPT_REQUEST_NUMBER_PER_MILLISECOND = 3650000000 / (365 * 24 * 60 * 60 * 1000);
var GPT_CONSUMPTION_PER_REQUEST = 2.9;
var EQUIVALENCE_GOOGLE_REQUEST = 0.3;

var AMAZON_ORDER_US_PER_MILLISECOND = 4500000000 / (365 * 24 * 60 * 60 * 1000);
var SHEIN_ORDER_PER_MILLISECOND = 320000000 / (365 * 24 * 60 * 60 * 1000);

var CLOUD_NEW_SERVER_PER_MILLISECOND = 120 * 5000 / (365 * 24 * 60 * 60 * 1000);
var CLOUD_TOTAL_SERVER = (992 * 5000);
if (YEAR - 2024 > 0) CLOUD_TOTAL_SERVER = CLOUD_TOTAL_SERVER + (120 * 5000 * (YEAR - 2024));

function getMillisecondsSinceNewYear() {
  var now = new Date();
  var startOfYear = new Date(now.getFullYear(), 0, 1);
  return now - startOfYear;
}

function calculateCumulativeMetrics(milliseconds) {
  var cumulativeCO2 = CO2_EMISSIONS_PER_MILLISECOND * milliseconds;
  var flightEquivalence = cumulativeCO2 / EQUIVALENCE_FLIGHT_PARIS_NY;
  var cumulativeElectricity = ELECTRICITY_CONSUMPTION_PER_MILLISECOND * milliseconds;
  var personEquivalence = cumulativeElectricity / EQUIVALENCE_FRENCH_PERSON;
  var cumulativeSmartphone = SMARTPHONE_SALES_PER_MILLISECOND * milliseconds;
  var cumulativeSmartphoneWater = cumulativeSmartphone * WATER_PER_SMARTPHONE;
  var cumulativePC = PC_SALES_PER_MILLISECOND * milliseconds;
  var cumulativePCWater = cumulativePC * WATER_PER_PC;
  var cumulativeEWaste = E_WASTE_PER_MILLISECOND * milliseconds;
  var cumulativeEWasteNonRecycled = cumulativeEWaste * (1 - E_WASTE_RECYCLING);
  var cumulativeCopper = COPPER_PER_MILLISECOND * milliseconds;
  var cumulativeCopperOre = cumulativeCopper * (1 / ORE_GRADE);
  var cumulativeElectricityBitcoin = BITCOIN_ELEC_PER_MILLISECOND * milliseconds;
  var visaEquivalence = cumulativeElectricityBitcoin / EQUIVALENCE_VISA;
  var cumulativeChatGPTRequest = GPT_REQUEST_NUMBER_PER_MILLISECOND * milliseconds;
  var cumulativeChatGPTElectricity = cumulativeChatGPTRequest * GPT_CONSUMPTION_PER_REQUEST;
  var googleEquivalence = cumulativeChatGPTRequest * EQUIVALENCE_GOOGLE_REQUEST;
  var cumulativeAmazon = AMAZON_ORDER_US_PER_MILLISECOND * milliseconds;
  var cumulativeShein = SHEIN_ORDER_PER_MILLISECOND * milliseconds;
  var cumulativeNewServer = CLOUD_NEW_SERVER_PER_MILLISECOND * milliseconds;
  var totalServer = CLOUD_TOTAL_SERVER + cumulativeNewServer;

  return {
    cumulativeCO2: Math.round(cumulativeCO2).toLocaleString(),
    flightEquivalence: Math.round(flightEquivalence).toLocaleString(),
    cumulativeElectricity: Math.round(cumulativeElectricity).toLocaleString(),
    personEquivalence: Math.round(personEquivalence).toLocaleString(),
    cumulativeSmartphone: Math.round(cumulativeSmartphone).toLocaleString(),
    cumulativeSmartphoneWater: Math.round(cumulativeSmartphoneWater).toLocaleString(),
    cumulativePC: Math.round(cumulativePC).toLocaleString(),
    cumulativePCWater: Math.round(cumulativePCWater).toLocaleString(),
    cumulativeEWaste: Math.round(cumulativeEWaste).toLocaleString(),
    cumulativeEWasteNonRecycled: Math.round(cumulativeEWasteNonRecycled).toLocaleString(),
    cumulativeCopper: Math.round(cumulativeCopper).toLocaleString(),
    cumulativeCopperOre: Math.round(cumulativeCopperOre).toLocaleString(),
    cumulativeElectricityBitcoin: Math.round(cumulativeElectricityBitcoin).toLocaleString(),
    visaEquivalence: visaEquivalence.toFixed(1),
    cumulativeChatGPTRequest: Math.round(cumulativeChatGPTRequest).toLocaleString(),
    cumulativeChatGPTElectricity: Math.round(cumulativeChatGPTElectricity).toLocaleString(),
    googleEquivalence: Math.round(googleEquivalence).toLocaleString(),
    cumulativeAmazon: Math.round(cumulativeAmazon).toLocaleString(),
    cumulativeShein: Math.round(cumulativeShein).toLocaleString(),
    cumulativeNewServer: Math.round(cumulativeNewServer).toLocaleString(),
    totalServer: Math.round(totalServer).toLocaleString()
  };
}

var spanYear = document.getElementById("year");
var stat1 = document.getElementById("stat1");
var stat2 = document.getElementById("stat2");
var stat3 = document.getElementById("stat3");
var stat4 = document.getElementById("stat4");
var stat5 = document.getElementById("stat5");
var stat6 = document.getElementById("stat6");
var stat7 = document.getElementById("stat7");
var stat8 = document.getElementById("stat8");
var stat9 = document.getElementById("stat9");
var stat10 = document.getElementById("stat10");

if (spanYear) spanYear.innerHTML = YEAR;

function getRandomDelay(delayed) {
  return delayed ? Math.random() * 1000 : 0;
}

function updateDisplay(delayed) {
  if (!stat1) return;
  var ms = getMillisecondsSinceNewYear();
  var m = calculateCumulativeMetrics(ms);
  setTimeout(function() { stat1.innerHTML = "CO2 Emissions: " + m.cumulativeCO2 + " tons<br>Equivalent to " + m.flightEquivalence + " Paris-NY flight tickets"; }, getRandomDelay(delayed));
  setTimeout(function() { stat2.innerHTML = "Electricity Consumption: " + m.cumulativeElectricity + " kWh<br>Equivalent to the annual consumption of " + m.personEquivalence + " french people"; }, getRandomDelay(delayed));
  setTimeout(function() { stat3.innerHTML = "E-Waste produced: " + m.cumulativeEWaste + " tons<br>Including " + m.cumulativeEWasteNonRecycled + " tons not recycled (" + Math.round((1 - E_WASTE_RECYCLING) * 100) + "%)"; }, getRandomDelay(delayed));
  setTimeout(function() { stat4.innerHTML = "Smartphones Sold: " + m.cumulativeSmartphone + " units<br>Using " + m.cumulativeSmartphoneWater + " liters of water"; }, getRandomDelay(delayed));
  setTimeout(function() { stat5.innerHTML = "Laptops and PCs Sold: " + m.cumulativePC + " units<br>Using " + m.cumulativePCWater + " liters of water"; }, getRandomDelay(delayed));
  setTimeout(function() { stat6.innerHTML = "Ore mined for copper in ICT : " + m.cumulativeCopperOre + " tons<br>Producing " + m.cumulativeCopper + " tons of Copper"; }, getRandomDelay(delayed));
  setTimeout(function() { stat7.innerHTML = "The bitcoin network consumed: " + m.cumulativeElectricityBitcoin + " kWh<br>Equivalent to " + m.visaEquivalence + " times the Visa network"; }, getRandomDelay(delayed));
  setTimeout(function() { stat8.innerHTML = m.cumulativeChatGPTRequest + " requests were made to ChatGPT<br>Consuming " + m.cumulativeChatGPTElectricity + " kWh<br>The Google requests equivalent would be " + m.googleEquivalence + " kWh"; }, getRandomDelay(delayed));
  setTimeout(function() { stat9.innerHTML = "In the US alone, " + m.cumulativeAmazon + " orders were passed to Amazon<br>In the mean time, " + m.cumulativeShein + " orders were passed to Shein"; }, getRandomDelay(delayed));
  setTimeout(function() { stat10.innerHTML = "This year, " + m.cumulativeNewServer + " new servers were installed in Cloud datacenters<br>On a total of " + m.totalServer + " servers"; }, getRandomDelay(delayed));
}

updateDisplay(false);
setInterval(function() { updateDisplay(true); }, 2000);
})();
