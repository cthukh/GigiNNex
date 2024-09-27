function showProfile(profile) {
    const modal = document.getElementById('fullProfile');
    const fullName = document.getElementById('fullName');
    const fullArea = document.getElementById('fullArea');
    const fullDescription = document.getElementById('fullDescription');

    // Datos de ejemplo
    const profilesData = {
        perfil1: {
            name: "Juan Pérez",
            area: "Desarrollador Web",
            description: "Juan es un desarrollador web con más de 5 años de experiencia en la creación de aplicaciones web y sitios responsivos."
        },
        perfil2: {
            name: "María López",
            area: "Diseñadora Gráfica",
            description: "María es diseñadora gráfica con un enfoque en la creación de identidades visuales y material promocional."
        }
    };

    // Mostrar datos del perfil
    fullName.textContent = profilesData[profile].name;
    fullArea.textContent = profilesData[profile].area;
    fullDescription.textContent = profilesData[profile].description;

    modal.style.display = "block";
}

function closeProfile() {
    const modal = document.getElementById('fullProfile');
    modal.style.display = "none";
}
