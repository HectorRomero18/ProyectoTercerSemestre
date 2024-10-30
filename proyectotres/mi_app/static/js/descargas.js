function downloadPDF() {
    const { jsPDF } = window.jspdf;  
    const doc = new jsPDF();  
    doc.setFontSize(20);  
    doc.text('Personas Atendidas', 12, 20);  

    const rows = document.querySelectorAll("#data-body tr");
    let y = 30;

    rows.forEach(row => {
        const cols = row.querySelectorAll("td");
        const data = Array.from(cols).map(col => col.textContent);
        if (data.length > 0) {
            doc.text(data.join(' | '), 14, y);  
            y += 10; 
        }
    });

    doc.save('personas_atendidas.pdf');  
}
