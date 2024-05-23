document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/data/fact');
        if (!response.ok) throw new Error('Network response was not ok');

        const factData = await response.json();

        // Ordenar los datos por Gasto Total de manera descendente
        factData.sort((a, b) => b['Gasto Total'] - a['Gasto Total']);

        const labels = factData.map(item => item['Deportista']);
        const data = factData.map(item => item['Gasto Total']);

        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Gasto Total por Deportista',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y', // Ajustar la orientación de las barras a horizontal
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching the data: ', error);
    }
});
