const placeholders = {
    natural_sciences: "Ex: Researcher in Biology",
    mathematics_statistics: "Ex: Data Analyst at a financial firm",
    engineering_technology: "Ex: Software engineer at Google",
    medical_health_sciences: "Ex: Doctor specializing in Pediatrics",
    social_sciences: "Ex: Sociologist working in public policy",
    humanities: "Ex: Historian or Professor of Literature",
    arts_design: "Ex: Graphic Designer at a creative agency",
    business_management: "Ex: Marketing Manager in a tech company",
    law_legal_studies: "Ex: Corporate Lawyer in a law firm",
    education: "Ex: Elementary School Teacher",
    computer_science_information_systems: "Ex: Cybersecurity Specialist",
    environmental_agricultural_sciences: "Ex: Environmental Consultant",
    communication_media: "Ex: Journalist at a major news outlet",
    interdisciplinary_studies: "Ex: Urban Planner with a focus on sustainability",
};

document.getElementById('interest').addEventListener('change', function() {
    const selectedArea = this.value;
    const objectiveInput = document.getElementById('objective');
    
    if (placeholders[selectedArea]) {
        objectiveInput.placeholder = placeholders[selectedArea];
    } else {
        objectiveInput.placeholder = "Ex: Software engineer at Google";
    }
});