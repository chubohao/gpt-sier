import type { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import axios from 'axios';

const service: AxiosInstance = axios.create({
  baseURL: "/",
  timeout: 1000, 
  headers: { "Content-Type": "application/json; charset=UTF-8"}
});

service.interceptors.request.use((config: AxiosRequestConfig) => {
     return config;
    }, (error) => {
    return Promise.reject(error)
});


export default service;