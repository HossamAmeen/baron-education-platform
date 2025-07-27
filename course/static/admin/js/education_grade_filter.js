document.addEventListener('DOMContentLoaded', function() {
    // Get the country and education stage select elements
    // const countrySelect = document.querySelector('select[name$="country"]');
    const educationStageSelect = document.querySelector('select[name$="education_stage"]');
    // const countrySelect = document.querySelector('select[id$="-country"]');
    // const countrySelect = document.querySelector('select[id*="country"]');
    // const countrySelect = document.getElementById('id_country');
    console.log("test")
    console.log(countrySelect)
    console.log(educationStageSelect)
    if (countrySelect && educationStageSelect) {
        // Function to update education stage options
        function updateEducationStages() {
            const countryId = countrySelect.value;
            const options = educationStageSelect.options;
            
            // First, hide all options
            for (let i = 0; i < options.length; i++) {
                options[i].style.display = 'none';
                options[i].disabled = true;
            }
            
            // Then show only options that match the selected country
            if (countryId) {
                for (let i = 0; i < options.length; i++) {
                    const option = options[i];
                    if (option.dataset.countryId === countryId || option.value === '') {
                        option.style.display = 'block';
                        option.disabled = false;
                    }
                }
            }
            
            // Trigger change event to update the select widget
            $(educationStageSelect).trigger('change');
        }
        
        // Add data-country-id attributes to options if not present
        if (educationStageSelect) {
            const options = educationStageSelect.options;
            for (let i = 0; i < options.length; i++) {
                const option = options[i];
                if (option.value && !option.dataset.countryId) {
                    // This assumes the option text contains the country ID in some way
                    // You might need to adjust this based on how your options are formatted
                    const match = option.text.match(/\(Country: (\d+)\)/);
                    if (match) {
                        option.dataset.countryId = match[1];
                    }
                }
            }
        }
        
        // Add event listener to country select
        countrySelect.addEventListener('change', updateEducationStages);
        
        // Initialize on page load
        updateEducationStages();
    }
});