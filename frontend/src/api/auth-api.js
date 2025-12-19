import axios from "axios";

const BASE_URL = "http://localhost:7000/api";

export async function loginUser({ name, password }) {
  const response = await axios.post(`${BASE_URL}/login`, {
    name,
    password
  });
  return response.data;
}
