const API_URL = "https://mini-erp-comercial-fastapi.onrender.com";

async function api(endpoint, options = {}) {

    const token = localStorage.getItem("token");

    const config = {
        headers: {
            "Content-Type": "application/json",

            ...options.headers
        },
        ...options
    };

    if (token) {
        config.headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, config);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Erro na requisição");
    }

    return data;
}