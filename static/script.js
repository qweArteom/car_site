document.addEventListener("DOMContentLoaded", () => {
    const carForm = document.getElementById("carForm");
    const carList = document.getElementById("carList");

    fetch("/cars")
        .then((res) => res.json())
        .then((cars) => {
            cars.forEach((car) => addCarToDOM(car));
        });

    carForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const make = document.getElementById("make").value;
        const model = document.getElementById("model").value;
        const year = document.getElementById("year").value;

        fetch("/cars", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ make, model, year }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.message === "Автомобіль додано!") {
                    addCarToDOM({ id: Date.now(), make, model, year });
                    carForm.reset();
                }
            });
    });
    
    carList.addEventListener("click", (e) => {
        if (e.target.tagName === "BUTTON") {
            const carId = e.target.dataset.id;

            fetch(`/cars/${carId}`, { method: "DELETE" })
                .then((res) => res.json())
                .then((data) => {
                    if (data.message === "Автомобіль видалено!") {
                        e.target.parentElement.remove();
                    }
                });
        }
    });

    function addCarToDOM(car) {
        const li = document.createElement("li");
        li.textContent = `${car.make} ${car.model} (${car.year})`;
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Видалити";
        deleteBtn.dataset.id = car.id;
        li.appendChild(deleteBtn);
        carList.appendChild(li);
    }
});
