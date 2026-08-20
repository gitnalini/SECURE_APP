import axios from 'axios';

const api=axios.create({
 baseURL:"http://127.0.0.1:8000/api/"   
})

const publicPaths=['login/','register/','valid-license/']

api.interceptors.request.use((config) => {

    const token=localStorage.getItem("access")
    if(token && !publicPaths.includes(config.url)){
        config.headers.Authorization = 'Bearer ' + token
    }
    return config;
},
(error) =>{
    return Promise.reject(error);
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh');

      if (!refreshToken) {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        const refreshResponse = await axios.post(
          'http://127.0.0.1:8000/api/token/refresh/',
          { refresh: refreshToken }
        );

        const newAccess = refreshResponse.data.access;
        localStorage.setItem('access', newAccess);

        if (refreshResponse.data.refresh) {
          localStorage.setItem('refresh', refreshResponse.data.refresh);
        }

        originalRequest.headers.Authorization = 'Bearer ' + newAccess;
        return api(originalRequest);

      } catch (refreshError) {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;