const API_URL = "http://127.0.0.1:8000";

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