window.onload = () => {

    window.searchInput = document.getElementById("search-input");
    window.regionSelect = document.getElementById("region-filter");
    window.snowReportContainer = document.getElementById("snow-reports");
    window.snowReportCardTemplate = document.getElementById("snow-report-card-template");
    
    loadSnowData();
    
    const searchBar = new SearchBar(searchInput, snowReportContainer);

    regionSelect.addEventListener("change", () => {
        const selectedRegion = regionSelect.value;

        if(selectedRegion === ""){
            searchBar.setFilter(null);
        } else {
            searchBar.setFilter({
                region: selectedRegion
            });
        }
    });

};

async function loadSnowData(){

    try {
        const response = await fetch("/api/snow_report");

        if(!response.ok)
            throw new Error("Server Error: " + response.statusText);

        const responseData = await response.json();

        if(responseData.success === false)
            throw new Error(responseData.error);
    
        renderSnowData(responseData.resorts);

    } catch (error) {
        const errorElement = document.createElement("div");
        errorElement.classList.add("text-danger", "col-12");
        errorElement.textContent = "Error loading snow data: " + error.message;

        snowReportContainer.innerHTML = "";
        snowReportContainer.appendChild(errorElement);
    }

}

function renderSnowData(resorts){

    const regionsSet = new Set();
    snowReportContainer.innerHTML = "";

    resorts.forEach(function(resort){

        resort.region = resort.region || "Unknown";

        const snowReportCard = snowReportCardTemplate.content.firstElementChild.cloneNode(true);

        snowReportCard.querySelector(".card-title").textContent = resort.resort_name;
        snowReportCard.querySelector(".card-subtitle").textContent = resort.region;
        snowReportCard.querySelector(".snow_valley_cm").textContent = renderSnowDepth(resort.snow_valley_cm);
        snowReportCard.querySelector(".snow_mountain_cm").textContent = renderSnowDepth(resort.snow_mountain_cm);
        snowReportCard.querySelector(".new_snow_cm").textContent = renderSnowDepth(resort.new_snow_cm);
        snowReportCard.querySelector(".lifts_open").textContent = resort.lifts_open;
        snowReportCard.querySelector("a").href = resort.resort_url;

        // Use data attributes for searching/filtering
        snowReportCard.dataset.resortName = resort.resort_name;
        snowReportCard.dataset.region = resort.region;

        regionsSet.add(resort.region);

        snowReportContainer.append(snowReportCard);

    });

    const regions = Array.from(regionsSet).sort();

    regions.forEach(function(region) {
        const option = document.createElement("option");
        option.value = region;
        option.textContent = region;
        regionSelect.append(option);
    });

}

function renderSnowDepth(snowDepth){
    if(snowDepth === null)
        return 'No Data';
    else
        return snowDepth + "cm";
}