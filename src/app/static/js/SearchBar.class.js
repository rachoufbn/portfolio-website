class SearchBar {
    constructor(searchInput, resultsContainer, filter = null) {
        this.searchInput = searchInput;
        this.resultsContainer = resultsContainer;
        this.filter = filter;
        this.initialize();
    }

    initialize() {
        this.searchInput.addEventListener("input", () => this.onChange());
        this.onChange();
    }

    onChange(){
        
        const query = this.normalizeString(this.searchInput.value);
        const resultElements = Array.from(this.resultsContainer.children);

        // Only show resultElements that have at least one dataset value matching the query
        resultElements.forEach(el => {

            // Show by default
            el.style.display = "";

            // Hide if any filter does not match
            if(this.filter){
                for(const [key, value] of Object.entries(this.filter)){
                    if(el.dataset[key] !== value){
                        el.style.display = "none";
                        return;
                    }
                }
            }

            // Hide if no dataset value matches the query
            if(query !== ""){

                const atLeastOneMatch = Object.values(el.dataset).some(value => {
                    return this.normalizeString(value).includes(query);
                });

                if(!atLeastOneMatch)
                    el.style.display = "none";

            }

        });

    }

    setFilter(filter) {
        this.filter = filter;
        this.onChange();
    }

    normalizeString(str) {
        return str.trim().toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, '');
    }

}