let materias = [];
const listarMaterias = async (codcarrera) => {
    try {
        const response = await fetch(`./materiasf/${codcarrera}`);
        const data = await response.json();

        if (data.message === "Success") {
           materias = data.materias;
            let opciones = ``;
            materias.forEach((materia) => {
                opciones += `<option value='${materia.id}'>${materia.materia}</option>`;
            });
            cboMateria.innerHTML = opciones;
        } else {
            alert("Materias no encontradas...");
        }
    } catch (error) {
        console.log(error);
    }
};
const cargaInicial = async () => {
    listarMaterias('KTII');
    cboCarrera.addEventListener("change", (event) => {
        listarMaterias(event.target.value);
    });

};
window.addEventListener("load", async () => {
    await cargaInicial();
});