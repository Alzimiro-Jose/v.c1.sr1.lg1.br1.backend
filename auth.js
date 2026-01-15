// C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\auth.js

// Recupera o token salvo no localStorage após login
export const getToken = () => localStorage.getItem("token");

// Função para verificar se o usuário está logado e redirecionar se não estiver
export const verificarLogin = (router) => {
    const token = getToken();

    if (!token) {
        router.push("/login");
    }
};

// Configuração padrão para requisições autenticadas
export const fetchComAuth = (url, options = {}) => {
    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        ...options.headers,
        "Authorization": token ? `Bearer ${token}` : "",
    };

    return fetch(url, { ...options, headers });
};
